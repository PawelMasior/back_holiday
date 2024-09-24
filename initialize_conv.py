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
import openai
import warnings
from typing import Annotated, Literal
from datetime import datetime
from copy import deepcopy

from settings.func import *
from tools.web import web_search
from tools.firecrawl import web_page
from tools.info import *
from prompts.func import *
from agents.func import *
from formats.restaurants import Restaurants
from formats.attractions import Attractions
from conv.func import *
from review.func import dbname, log_report

openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()
seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
clean_memory()

# =============================================================================
name_city = "Montpellier, France"
date_fr = "15-11-2024"
date_to = "22-11-2024"
query = {
    'name_city': name_city,
    'date_fr': date_fr,
    'date_to': date_to,
    }
# =============================================================================

# =============================================================================

Data = {}
def save_restaurants(
        text: Annotated[str, "Markdown information about restaurants"],                
        ) -> str:
    return save_data(text, 'restaurants', Restaurants, Data)

def save_attractions(
        text: Annotated[str, "Markdown information about attractions"],                
        ) -> str:
    return save_data(text, 'attractions', Attractions, Data)

# =============================================================================
Conv = []

# =============================================================================
# bool_restaurants = True
# desc_restaurants = """🥣 Local Cuisine, ✨ Low budget"""
# conv_restaurants, agent_planner, agent_restaurants, executor_restaurants = get_conv(
#     query, desc_restaurants, agent_planner, save_restaurants, 'restaurants', get_prompt_restaurants)
# Conv += [conv_restaurants]
# =============================================================================

bool_attractions = True
desc_attractions = """🛍️ Shopping, 📸 Scenic Spots"""
conv_attractions, agent_planner, agent_attractions, executor_attractions = get_conv(
    query, desc_attractions, agent_planner, save_attractions, 'attractions', get_prompt_attractions)
Conv += [conv_attractions]

# =============================================================================
# =============================================================================

logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
chat_results = agent_planner.initiate_chats(Conv)
autogen.runtime_logging.stop()


# =============================================================================
# =============================================================================
# def get_prompt_restaurants(query, desc) -> str:  
#     prompt = f"""
#     Provide a curated list of restaurants in {query['name_city']} tailored for tourists.
#     
#     Focus on: {desc}.
#     
#     Requirements:
#     - Specify the type of cuisine offered (e.g., Italian, Japanese).
#     - Highlight each restaurant's unique feature (e.g., atmosphere, view).
#     - Include each restaurant's specialty or signature dish.
#     - Include the average price range with currency (e.g., "$$$").
#     - Include each restaurant's address.
#     - Include the opening hours of the restaurant.
#     - Include detailed contact information: phone number and website URL.
#     - Clearly indicate whether reservations are required ('Yes', 'No', 'No data').
#     
#     After you collectcted all data, save the data of the best ones (no duplicates) and finish the task.
#     """
#     return prompt
# 
# def get_conv_restaurants(query, desc_restaurants, agent_planner, save_restaurants):
# 
#     prompt_restaurants = get_prompt_restaurants(query, desc_restaurants)
#     
#     agent_restaurants = get_agent_researcher('restaurants')
#     executor_restaurants = get_executor()
#     
#     autogen.register_function(web_search, caller=agent_restaurants, executor=executor_restaurants,
#         name="web_search",
#         description="""Searches internet with query, providing concise or detailed content as needed."""
#     )
#     autogen.register_function(web_page, caller=agent_restaurants, executor=executor_restaurants,
#         name="web_page",
#         description="""Retrieves website content by scraping URL."""
#     )
#     autogen.register_function(save_restaurants, caller=agent_restaurants, executor=executor_restaurants,
#         name="save_restaurants",
#         description="""Saves final report of restaurants from markdown format. """
#     )
#     queue = [
#         {"recipient": agent_restaurants, "sender": executor_restaurants, "summary_method": "last_msg"},
#         {"recipient": agent_planner, "sender": agent_restaurants, "summary_method": "reflection_with_llm"},
#         ]
#     agent_restaurants.register_nested_chats(trigger=agent_planner, chat_queue=queue)
#     
#     conv_restaurants = {
#             "recipient": agent_restaurants,
#             "message": f"""{prompt_restaurants}""",
#             "max_turns": 10,
#             "max_round": 30,
#             "summary_method": "reflection_with_llm",
#             }
#     return conv_restaurants, agent_planner, agent_restaurants, executor_restaurants
# =============================================================================


# =============================================================================

# =============================================================================







