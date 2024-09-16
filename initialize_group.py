# %reset -f
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('settings',f'ai-agents-project-key.json')
from dotenv import load_dotenv
load_dotenv()
import autogen
import numpy as np
import random
import json
import shutil
from typing import Annotated, Literal

from prompts.definitions import *
from tools.web import web_search
from tools.firecrawl import web_page
from tools.twilio import sms_send, sms_inbox
from tools.info import *
from tools.excel import save_excel

from agents.agents import *
agents_const = [agent_planner, agent_secretary]
agents_hire = [agent_researcher]
agents_all = agents_const + agents_hire

from settings.func import *
from review.func import dbname, log_report

import warnings
seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
clean_memory()




# =============================================================================
name_city = "Napoli, Italy"
desc_user = "local specialities,low budget,adventure"
date_fr = "07-12-2024"
date_to = "14-12-2024"
bool_restaurants = True
bool_museums = True
bool_events = True
bool_avoid = True


# =============================================================================
# Tools register
# =============================================================================
autogen.register_function(web_search, caller=agent_researcher, executor=executor,
    name="web_search",
    description="""
    Searches internet with query, providing concise or detailed content as needed.
    """
)

autogen.register_function(web_page, caller=agent_researcher, executor=executor,
    name="web_page",
    description="""
    Retrieves website content by scraping URL. 
    Efficient and effective to collect public information.
    """
)

autogen.register_function(save_report, caller=agent_secretary, executor=executor,
    name="save_report",
    description="""
    Saves report in markdown format.
    """
)

autogen.register_function(read_report, caller=agent_secretary, executor=executor,
    name="read_report",
    description="""
    Reads markdown report.
    """
)

# =============================================================================
agents_const = [agent_planner, agent_secretary]
agents_tool = [agent_researcher] #filter here
agents_chat = agents_const + agents_tool
agents_transitions = {
    agent_planner: [agent_researcher, agent_secretary],
    agent_researcher: [agent_secretary],
    agent_secretary: [agent_planner],
}
group_chat = autogen.GroupChat(
    agents=agents_chat,
    messages=[],
    max_round=20,
    allowed_or_disallowed_speaker_transitions=agents_transitions,
    speaker_transitions_type="allowed",        
)
group_chat_manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
    #{"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
)
for i, agent in enumerate(agents_chat): 
    if agent.name == 'Planner': pass
    else:
        agents_other = [a for i_a, a in enumerate(agents_chat) if i!=i_a]
        queue=[
            {"recipient": agent, "sender": executor, "summary_method": "last_msg"},
            {"recipient": group_chat_manager, "sender": agent, "summary_method": "reflection_with_llm"},
            ] + [{"recipient": a, "sender": agent, "summary_method": "reflection_with_llm"} for a in agents_other]
        agent.register_nested_chats(trigger=group_chat_manager, chat_queue=queue)
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
            "recipient": group_chat_manager,
            "message": f"""
            {t}

            # Additional intructions:
                - Focuse on the task and perform only necessary steps.                
                - Finalize task with the report. 
            """,
            "max_turns": 10,
            "max_round": 30,
            "summary_method": "reflection_with_llm",
        } for t in Plan])
autogen.runtime_logging.stop()


# =============================================================================
# log_report(dbname, logging_session_id, 'plan', Plan, chat_results)
# 
# =============================================================================
Markdowns = os.listdir('temporary')
data_content = []
for f in os.listdir('temporary'):
    with open(os.path.join('temporary', f), 'r') as f: 
        content = f.read()
        data_content += [content]






