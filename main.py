from uvicorn import run
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException, File, UploadFile  # , Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import os
# from dotenv import load_dotenv
# load_dotenv()

# with open(os.path.join(os.getcwd(), 'initialize.py')) as f:
#     exec(f.read(), globals())
import autogen
import numpy as np
import random
import json
import shutil
import pandas as pd
import warnings
from typing import Annotated, Literal
from datetime import datetime

from agents.func import *
from prompts.func import *
from settings.func import *
# from review.func import dbname, log_report
from tools.web import web_search
from tools.firecrawl import web_page

seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
# clean_memory()

# =============================================================================
Reports = []
report_final = ''
def save_report(
        name: Annotated[str, "Report name"],
        content: Annotated[str, "Markdown content of report"],
        ) -> str:
    global Reports
    r = {
        'name': name,
        'content': content,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    Reports.append(r)  # Use append() instead of +=
    return f"Success: Report {name} saved."

def get_info() -> str:
    df_info = pd.DataFrame(Reports).sort_values(by='time')
    info = '\n\n'.join(df_info['content'])
    return info

def save_report_final(
        content: Annotated[str, "Markdown content of the full report"],
        ) -> str:
    global report_final
    report_final = content
    return f"Success: Final report is prepared and saved. TERMINATE"
# =============================================================================
# =============================================================================
# FastAPI
# =============================================================================
app = FastAPI(
    title="My Holiday Planner",
    description='Plan my holiday trip',
    version="0.0.1",
    terms_of_service="<link>",
    contact={
        "name": "contact",
        # "url": "https://geekforce.io",
        "email": "pawel.masior@lotangroup.com",
    },
    license_info={
        "name": "Samlpe licence",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    #"https://domain.com",
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(): return 'holiday'
            
@app.get("/report/")#, tags=["APIs"], response_model=str)
def _report(
        name_city: str = Query("Napoli"),
        desc_user: str = Query("local specialities,low budget,adventure"),
        date_fr: str = Query("07-12-2024"),
        date_to: str = Query("14-12-2024"),
        bool_eating: bool = Query(False),
        bool_events: bool = Query(False),
        # bool_museums: bool = Query(True),
        # bool_local: bool = Query(True),
        # bool_avoid: bool = Query(True),
        ):
    # =============================================================================
    query = {
        'name_city': name_city,
        'desc_user': desc_user,
        'date_fr': date_fr,
        'date_to': date_to,
        }
    scope = {
        'eating': bool_eating,
        'events': bool_events,
        'museums': False,
        'safety': False,
        'health': False,
        'shopping': False,
        'around': False,
        'accomodation': False,
        'attractions': False,
        'transportation': False,
        'nightlife': False,
        'wellness': False,
        }
    # =============================================================================
    autogen.register_function(web_search, caller=agent_researcher, executor=executor,
        name="web_search",
        description="""Searches internet with query, providing concise or detailed content as needed."""
    )
    autogen.register_function(web_page, caller=agent_researcher, executor=executor,
        name="web_page",
        description="""Retrieves website content by scraping URL."""
    )
    autogen.register_function(save_report, caller=agent_researcher, executor=executor,
        name="save_report",
        description="""Saves report in markdown format."""
    )

    autogen.register_function(get_info, caller=agent_secretary, executor=executor,
        name="get_info",
        description="""Get all collected informations on destination place."""
    )
    autogen.register_function(save_report_final, caller=agent_secretary, executor=executor,
        name="save_report_final",
        description="""Prepare aggregated report for the user."""
    )
    # =============================================================================
    queue_researcher = [
        {"recipient": agent_researcher, "sender": executor, "summary_method": "last_msg"},
        {"recipient": agent_planner, "sender": agent_researcher, "summary_method": "reflection_with_llm"},
        ]
    agent_researcher.register_nested_chats(trigger=agent_planner, chat_queue=queue_researcher)

    queue_secretary = [
        {"recipient": agent_secretary, "sender": executor, "summary_method": "last_msg"},
        {"recipient": agent_planner, "sender": agent_secretary, "summary_method": "reflection_with_llm"},
        ]
    agent_secretary.register_nested_chats(trigger=agent_planner, chat_queue=queue_secretary)
    # =============================================================================
    Plan = []
    Plan = [prompt_start(query)]
    if scope['eating']: Plan += [prompt_eating(query)]
    if scope['events']: Plan += [prompt_events(query)]
    # =============================================================================
    Conv = [{
                "recipient": agent_researcher,
                "message": f"""
                {t}
                
                Focuse on the task and perform only necessary steps.                
                Finalize task with saving collected information into the report!
                """,
                "max_turns": 10,
                "max_round": 30,
                "summary_method": "reflection_with_llm",
            } for t in Plan]
    Conv += [{
                "recipient": agent_secretary,
                "message": f"""
                1. Get all collected informations on destination place.
                2. {prompt_final(query, scope)} 
                
                Focuse on the task and perform only necessary steps.                
                Finalize task with saving collected information into the report! 
                """,
                "max_turns": 10,
                "max_round": 30,
                "summary_method": "reflection_with_llm",
            }]
    # =============================================================================
    logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
    chat_results = agent_planner.initiate_chats(Conv)
    autogen.runtime_logging.stop()
    # =============================================================================

    # with open(os.path.join('temporary', 'report_final.md'), 'w', encoding='utf-8') as f:
    #     f.write(report_final)

    return HTMLResponse(content=report_final)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)

