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
from tools.firecrawl import web_page, web_page_raw
from tools.twilio import sms_send, sms_inbox
from tools.excel import save_excel
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()


from pydantic import BaseModel, Field
from collections.abc import MutableMapping
from textwrap import dedent
import json

class RestaurantDetails(BaseModel):
    name: str = Field(..., description="Restaurant name")
    cuisine: str = Field(..., description="Main cuisine type")
    price: str = Field(..., description="Average price range with currency")
    unique_feature: str = Field(..., description="What makes the restaurant unique")
    specialty: str = Field(..., description="Signature dish or cuisine specialty")
    phone: str = Field(..., description="Contact phone number")
    address: str = Field(..., description="Restaurant address")
    website: str = Field(..., description="Website URL")
    opening_hours: str = Field(..., description="Opening hours of the restaurant")
    reservation: str = Field(..., description="Reservation requirement ('Yes', 'No', 'No data')")

class Restaurants(BaseModel):
    data: list[RestaurantDetails]

# =============================================================================
# url = "https://www.tripadvisor.com/Restaurants-g274812-Wroclaw_Lower_Silesia_Province_Southern_Poland.html"
# txt_md = web_page_raw(url)
# print(txt_md)
# =============================================================================

# =============================================================================
# def save_data(markdown_content, name, Format):
#     try:
#         prompt = f"""
#         You extract {name} data based on markdown content.
#         Keep all {name} from the markdown content.
#         """
#         response = client_openai.beta.chat.completions.parse(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": prompt},
#                 {"role": "user", "content": f"RAW_CONTENT: {markdown_content}"},
#             ],
#             response_format=Format,
#         )
#         json_extract = json.loads(response.choices[0].message.content)
#         df = pd.DataFrame(json_extract['data'])
#         df.to_csv(os.path.join('temporary', f"{name}.csv"), index=False, sep='\t',  encoding='utf-16')
#         msg = f"Success: Saved {df.shape[0]} {name} into the report."
#     except Exception as e:
#         msg = f"Error: {str(e)[:200]}"
#     return msg
# 
# msg = save_data(txt_md, 'restaurants', Restaurants)
# =============================================================================




# =============================================================================
# def flatten_json_array(json_data):
#     flattened_data = []
#     
#     for item in json_data:
#         arrays_found = False
# 
#         # Split the key-value pairs into those with lists and those without
#         single_entries = {}
#         array_entries = {}
# 
#         for key, value in item.items():
#             if isinstance(value, list):
#                 array_entries[key] = value
#                 arrays_found = True
#             else:
#                 single_entries[key] = value
#         
#         if arrays_found:
#             for key, value_list in array_entries.items():
#                 for entry in value_list:
#                     flattened_entry = flatten_json(entry)
#                     combined_entry = {**single_entries, **flattened_entry}
#                     flattened_data.append(combined_entry)
#         else:
#             flattened_data.append(single_entries)
# 
#     return flattened_data
# =============================================================================


