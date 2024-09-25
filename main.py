from uvicorn import run
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException, File, UploadFile  # , Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
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

# from review.func import dbname, log_report
from settings.func import clean_memory
from tools.tavily import tavily_search
from tools.firecrawl import firecrawl_page
from tools.save import save_data
from codes.prompts import *
from codes.agents import *
from codes.formats import *
from codes.conv import get_conv

seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
# clean_memory()
# dbname = os.path.join('review',f"logs.db")

app = FastAPI(
    title="🧭 Dalongo",
    description='🗺️ Plan Less, Explore More.',
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
        date_fr: str = Query("07-12-2024"),
        date_to: str = Query("14-12-2024"),
        desc_attractions: str = Query("""🏛️ Museums, 🛍️ Shopping, ⛩️ Historical Sites"""),
        desc_restaurants: str = Query("""🥣 Local Cuisine, ✨ Low budget"""),
        desc_activities: str = Query("""🕵️‍♀️ Escape Rooms, 💆‍♀️ Spa"""),
        desc_beyondthecity: str = Query("""🏔️ Hiking, 🍷 Wine Tours"""),
        desc_facilities: str = Query("""💻 Digital Nomad, 🚴 Bike Rental"""),
        ):
    query = {
        'name_city': name_city,
        'date_fr': date_fr,
        'date_to': date_to,
        }
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
    agent_planner = get_agent_planner()
    Conv = []

    if len(desc_beyondthecity):
        conv_restaurants, agent_planner, agent_restaurants, executor_restaurants = get_conv(
            query, desc_restaurants, agent_planner, save_restaurants, 'restaurants', get_prompt_restaurants)
        Conv += [conv_restaurants]
    
    if len(desc_attractions):
        conv_attractions, agent_planner, agent_attractions, executor_attractions = get_conv(
            query, desc_attractions, agent_planner, save_attractions, 'attractions', get_prompt_attractions)
        Conv += [conv_attractions]
    
    if len(desc_activities):
        conv_activities, agent_planner, agent_activities, executor_activities = get_conv(
            query, desc_activities, agent_planner, save_activities, 'activities', get_prompt_activities)
        Conv += [conv_activities]

    if len(desc_beyondthecity):
        conv_beyondthecity, agent_planner, agent_beyondthecity, executor_beyondthecity = get_conv(
            query, desc_beyondthecity, agent_planner, save_beyondthecity, 'beyond the city activities', get_prompt_beyondthecity)
        Conv += [conv_beyondthecity]

    if len(desc_facilities):
        conv_facilities, agent_planner, agent_facilities, executor_facilities = get_conv(
            query, desc_facilities, agent_planner, save_facilities, 'facilities', get_prompt_facilities)
        Conv += [conv_facilities]

    # =============================================================================

    # logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
    chat_results = agent_planner.initiate_chats(Conv)
    # autogen.runtime_logging.stop()
    # =============================================================================
    with open(os.path.join('reports',f'{name_city}.json'), 'w') as f: json.dump(Data, f)

    # with open(os.path.join('temporary', 'report_final.md'), 'w', encoding='utf-8') as f:
    #     f.write(report_final)
    result = {
        "chat_results": "\n\n".join(c.summary for c in chat_results),
        "guidebook": Data,#json.dumps(Data, indent = 4),
    }
    return JSONResponse(content=result) #HTMLResponse(content=report_final)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)

# # =============================================================================
# Reports = []
# report_final = ''
# def save_report(
#         name: Annotated[str, "Report name"],
#         content: Annotated[str, "Markdown content of report"],
#         ) -> str:
#     global Reports
#     r = {
#         'name': name,
#         'content': content,
#         'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }
#     Reports.append(r)  # Use append() instead of +=
#     return f"Success: Report {name} saved."

# def get_info() -> str:
#     df_info = pd.DataFrame(Reports).sort_values(by='time')
#     info = '\n\n'.join(df_info['content'])
#     return info

# def save_report_final(
#         content: Annotated[str, "Markdown content of the full report"],
#         ) -> str:
#     global report_final
#     report_final = content
#     return f"Success: Final report is prepared and saved. TERMINATE"
# # =============================================================================