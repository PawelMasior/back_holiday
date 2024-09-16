from uvicorn import run
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException, File, UploadFile  # , Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('settings',f'ai-agents-project-key.json')
from dotenv import load_dotenv
load_dotenv()

# with open(os.path.join(os.getcwd(), 'initialize.py')) as f:
#     exec(f.read(), globals())
import autogen
import numpy as np
import random
import json
import shutil
import pandas as pd
from typing import Annotated, Literal
from datetime import datetime
from prompts.definitions import *
from tools.web import web_search
from tools.firecrawl import web_page
from tools.twilio import sms_send, sms_inbox
from tools.info import *
from tools.excel import save_excel
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()

from settings.func import *
from review.func import dbname, log_report
from agents.agents import *

import warnings
seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
clean_memory()

Reports = []
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
# =============================================================================
# Agents
# =============================================================================
agent_planner = autogen.ConversableAgent(
    name="Planner",
    system_message = """
    # You are the Planner monitoring the progress of the task to complete it.

    ### Responsibilities
    **Plan Development and Execution:**
    - **Create Plan:** Outline specific steps needed to complete the research.
    - **Monitor Progress:** Track the progress of each step and verify completion or if additional steps are required.
    - **Make Decisions:** Make high-level decisions based on info from agents.
    **Error Handling:**
    - **Handle Errors:** Develop a new plan or adjust actions if errors occur or if responses are incorrect.
    - **Guide Adjustments:** Direct agents on necessary changes to achieve task goals.

    ### Reply 'TERMINATE' when the whole task is completed.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=3,
    human_input_mode="NEVER",
)

agent_researcher = autogen.ConversableAgent(
    name="Researcher",
    system_message="""
    # You are the Researcher collecting information from the web.

    ### Responsibilities
    - **Provide Tools Output:** Return results from executed tools to other agents.
    - **Deep dive:** Adjust research to gather precise information as needed.
    - **Save report:** Save collected info from research into report.
    

    ### Reply 'TERMINATE' when the whole task is completed.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
)

@app.get("/")
def home(): return 'tripoplan'
            
@app.get("/job/")#, tags=["APIs"], response_model=str)
def _stream(
        name_city: str = Query("Napoli"),
        desc_user: str = Query("local specialities,low budget,adventure"),
        date_fr: str = Query("07-12-2024"),
        date_to: str = Query("14-12-2024"),
        bool_restaurants: bool = Query(False),
        bool_events: bool = Query(False),
        # bool_museums: bool = Query(True),
        # bool_local: bool = Query(True),
        # bool_avoid: bool = Query(True),
        ):
    # Reports = []
    # =============================================================================
    # Tools
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
    # =============================================================================
    queue=[
        {"recipient": agent_researcher, "sender": executor, "summary_method": "last_msg"},
        {"recipient": agent_planner, "sender": agent_researcher, "summary_method": "reflection_with_llm"},
        ]
    agent_researcher.register_nested_chats(trigger=agent_planner, chat_queue=queue)
    # =============================================================================

    # =============================================================================
    Plan = []
    Plan = [prompt_start(name_city, desc_user, date_fr, date_to)]
    if bool_restaurants: 
        Plan += [prompt_food(name_city, desc_user)]
    if bool_events: 
        Plan += [prompt_events(name_city, desc_user, date_fr, date_to)]
        
    # =============================================================================

    logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
    chat_results = agent_planner.initiate_chats([{
                "recipient": agent_researcher,
                "message": f"""
                {t}

                # Additional intructions:
                - Focuse on the task and perform only necessary steps.                
                - Finalize task with saving collected information into the report! 
                """,
                "max_turns": 10,
                "max_round": 30,
                "summary_method": "reflection_with_llm",
            } for t in Plan])
    autogen.runtime_logging.stop()

    # =============================================================================
    # log_report(dbname, logging_session_id, 'plan', Plan, chat_results)
    # =============================================================================
    # =============================================================================
    df_info = pd.DataFrame(Reports).sort_values(by='time')
    info = '\n\n'.join(df_info['content'])
    prompt_report = f"""{prompt_final(name_city, desc_user, date_fr, date_to, bool_restaurants, bool_events)}
    Collected information:
        {info}
    """

    response = client_openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [{ "type": "text", "text": prompt_report,},],
        }
    ],
    max_tokens=5000,
    temperature=0.
    )
    final_report = response.choices[0].message.content
    return HTMLResponse(content=final_report)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    run(app, host="0.0.0.0", port=port)

