# %reset -f
import os
from dotenv import load_dotenv
load_dotenv()
import autogen
import numpy as np
import random
import json
import shutil
import pandas as pd
from typing import Annotated, Literal
from datetime import datetime

from agents.func import *
from prompts.func import *
from settings.func import *
from review.func import dbname, log_report

from tools.web import web_search
from tools.firecrawl import web_page
from tools.twilio import sms_send, sms_inbox
from tools.excel import save_excel
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()

import warnings
seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
clean_memory()

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
name_city = "Napoli, Italy"
desc_user = "local specialities,low budget,adventure"
date_fr = "07-12-2024"
date_to = "14-12-2024"
bool_eating = False
bool_events = False

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
# log_report(dbname, logging_session_id, 'task', Plan, chat_results)
# =============================================================================

with open(os.path.join('temporary', 'report_final.md'), 'w', encoding='utf-8') as f:
    f.write(report_final)

# =============================================================================
# log_report(dbname, logging_session_id, 'plan', Plan, chat_results)
# =============================================================================
# =============================================================================
# =============================================================================
# df_info = pd.DataFrame(Reports).sort_values(by='time')
# info = '\n\n'.join(df_info['content'])
# prompt_final = f"""{}
# Collected information:
#     {info}
# """
# 
# response = client_openai.chat.completions.create(
#   model="gpt-4o-mini",
#   messages=[
#     {
#         "role": "user",
#         "content": [{ "type": "text", "text": prompt_final,},],
#     }
#   ],
#   max_tokens=5000,
#   temperature=0.
# )
# final_report = response.choices[0].message.content
# 
# with open(os.path.join('temporary', 'final_report.md'), 'w', encoding='utf-8') as f:
#     f.write(final_report)
# =============================================================================









