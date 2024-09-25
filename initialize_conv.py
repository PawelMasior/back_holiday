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

from review.func import dbname, log_report
from settings.func import clean_memory
from tools.tavily import tavily_search
from tools.firecrawl import firecrawl_page
from tools.save import save_data

from codes.prompts import *
from codes.agents import *
from codes.formats import *
from codes.conv import get_conv

# =============================================================================
# openai.api_key = os.getenv('OPENAI_API_KEY')
# client_openai = openai.OpenAI()
# seed = 123
# np.random.seed(seed)
# random.seed(seed)
# warnings.filterwarnings("ignore")
# clean_memory()
# =============================================================================

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

def save_activities(
        text: Annotated[str, "Markdown information about activities"],                
        ) -> str:
    return save_data(text, 'activities', Activities, Data)

def save_beyondthecity(
        text: Annotated[str, "Markdown information about outdoor and cultural activities beyond the city"],                
        ) -> str:
    return save_data(text, 'beyond the city activities', BeyondTheCity, Data)

def save_facilities(
        text: Annotated[str, "Markdown information about facilities"],                
        ) -> str:
    return save_data(text, 'facilities', Facilities, Data)

# =============================================================================
Conv = []

# =============================================================================
# bool_restaurants = True
# desc_restaurants = """🥣 Local Cuisine, ✨ Low budget"""
# conv_restaurants, agent_planner, agent_restaurants, executor_restaurants = get_conv(
#     query, desc_restaurants, agent_planner, save_restaurants, 'restaurants', get_prompt_restaurants)
# Conv += [conv_restaurants]
# 
# bool_attractions = True
# desc_attractions = """🛍️ Shopping"""
# conv_attractions, agent_planner, agent_attractions, executor_attractions = get_conv(
#     query, desc_attractions, agent_planner, save_attractions, 'attractions', get_prompt_attractions)
# Conv += [conv_attractions]
# 
# bool_activities = True
# desc_activities = """🕵️‍♀️ Escape Rooms"""
# conv_activities, agent_planner, agent_activities, executor_activities = get_conv(
#     query, desc_activities, agent_planner, save_activities, 'activities', get_prompt_activities)
# Conv += [conv_activities]
# =============================================================================

bool_beyondthecity = True
desc_beyondthecity = """🏖️ Beach"""
conv_beyondthecity, agent_planner, agent_beyondthecity, executor_beyondthecity = get_conv(
    query, desc_beyondthecity, agent_planner, save_beyondthecity, 'beyond the city activities', get_prompt_beyondthecity)
Conv += [conv_beyondthecity]

# =============================================================================
# bool_facilities = True
# desc_facilities = """💻 Digital Nomad"""
# conv_facilities, agent_planner, agent_facilities, executor_facilities = get_conv(
#     query, desc_facilities, agent_planner, save_facilities, 'facilities', get_prompt_facilities)
# Conv += [conv_facilities]
# =============================================================================


# =============================================================================

logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
chat_results = agent_planner.initiate_chats(Conv)
autogen.runtime_logging.stop()

# =============================================================================












