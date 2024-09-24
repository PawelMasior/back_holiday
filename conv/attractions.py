# %reset -f
import os
from dotenv import load_dotenv
load_dotenv()
import autogen

from tools.web import web_search
from tools.firecrawl import web_page

from formats.attractions import *
from prompts.func import *
from agents.func import *

def get_conv_restaurants(query, desc_restaurants, agent_planner, save_restaurants):
    
    prompt_restaurants = get_prompt_restaurants(query, desc_restaurants)
    
    agent_restaurants = get_agent_researcher('restaurants')
    executor_restaurants = get_executor()
    
    autogen.register_function(web_search, caller=agent_restaurants, executor=executor_restaurants,
        name="web_search",
        description="""Searches internet with query, providing concise or detailed content as needed."""
    )
    autogen.register_function(web_page, caller=agent_restaurants, executor=executor_restaurants,
        name="web_page",
        description="""Retrieves website content by scraping URL."""
    )
    autogen.register_function(save_restaurants, caller=agent_restaurants, executor=executor_restaurants,
        name="save_restaurants",
        description="""Saves final report of restaurants from markdown format. """
    )
    queue = [
        {"recipient": agent_restaurants, "sender": executor_restaurants, "summary_method": "last_msg"},
        {"recipient": agent_planner, "sender": agent_restaurants, "summary_method": "reflection_with_llm"},
        ]
    agent_restaurants.register_nested_chats(trigger=agent_planner, chat_queue=queue)
    
    conv_restaurants = {
            "recipient": agent_restaurants,
            "message": f"""{prompt_restaurants}""",
            "max_turns": 10,
            "max_round": 30,
            "summary_method": "reflection_with_llm",
            }
    return conv_restaurants, agent_planner, agent_restaurants, executor_restaurants