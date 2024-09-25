# %reset -f
import os
from dotenv import load_dotenv
load_dotenv()
import autogen

from tools.tavily import tavily_search
from tools.firecrawl import firecrawl_page
from formats.attractions import *
from prompts.func import *
from agents.func import *

def get_conv(query, desc, agent_planner, save_func, name, get_prompt):
    prompt = get_prompt(query, desc)
    agent_f = get_agent_researcher(f"{name}")
    executor_f = get_executor(f"{name}")
    
    autogen.register_function(tavily_search, caller=agent_f, executor=executor_f,
        name="tavily_search",
        description="""Searches internet with query, providing concise or detailed content as needed."""
    )
    autogen.register_function(firecrawl_page, caller=agent_f, executor=executor_f,
        name="firecrawl_page",
        description="""Retrieves website content by scraping URL."""
    )
    autogen.register_function(save_func, caller=agent_f, executor=executor_f,
        name="save_func",
        description=f"""Saves final report of {name} from markdown format."""
    )
    queue = [
        {"recipient": agent_f, "sender": executor_f, "summary_method": "last_msg"},
        {"recipient": agent_planner, "sender": agent_f, "summary_method": "reflection_with_llm"},
        ]
    agent_f.register_nested_chats(trigger=agent_planner, chat_queue=queue)
    
    conv = {
            "recipient": agent_f,
            "message": f"""{prompt}""",
            "max_turns": 10,
            "max_round": 30,
            "summary_method": "reflection_with_llm",
            }
    return conv, agent_planner, agent_f, executor_f