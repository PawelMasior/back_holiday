import os
import openai
import json
import pandas as pd
from openai import OpenAI
from typing import Annotated, Literal
# from pydantic import BaseModel
# from typing import Dict, List
# from dotenv import load_dotenv
# from pprint import pprint
# load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI()

folder = 'temporary'
def csv_save(name_k, data_v):
    msg_csv = ""
    # if isinstance(value, list) and all(isinstance(item, dict) for item in value):        
    if isinstance(data_v, list):
        df = pd.DataFrame(data_v)
        df.to_csv(os.path.join(folder, f"{name_k}.csv"), index=False, sep='\t',  encoding='utf-16')
        msg_csv = f"""Success: Saved data to '{name_k}.csv':\n"""
        msg_csv+= f"""\t{df}\n\n""" if df.shape[0]<=3 else f"""\t{df.iloc[:3,:]}\n...\n\n"""
    return msg_csv

def save_excel(
        input_text: Annotated[str, "Markdown string to save collected information into csv."],
        ) -> str:
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
             "content": """
    You are an expert at structured data extraction. 
    You will be given text and prepare json data to be aggregated in table formats.
    Each data element will be used directly for pd.DataFrame(element) function.
    Try not to provide nested data format. 
    """},
            {"role": "user", 
             "content": f"{input_text}"}
        ],
        response_format={"type": "json_object"},
    )
    msg = ""
    try:
        response_text = response.choices[0].message.content
        data_dict = json.loads(response_text)
        for k0,v0 in data_dict.items():
            msg += csv_save(k0,v0)
            if isinstance(v0, dict):#type(v0) == dict:
                for k1,v1 in v0.items():
                    msg += csv_save(k1,v1)
                    if isinstance(v1, dict):#type(v1) == dict:
                        for k2,v2 in v1.items():
                            msg += csv_save(k2,v2)
                            if isinstance(v2, dict):#type(v2) == dict:
                                for k3,v3 in v2.items():
                                    msg += csv_save(k3,v3)                    
    except json.JSONDecodeError:
        msg = "Error: Failed to decode JSON from response"
    except Exception as e:
        msg = f"Error: An error occurred: {e}"
    if not len(msg):
        msg = f"Error: Did not save the data: try again or update input_text."
    return msg