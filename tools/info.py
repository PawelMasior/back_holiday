import json
import os
import pandas as pd
from typing import Annotated, Literal
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = openai.OpenAI()

def save_data(markdown_content, name, Format):
    try:
        prompt = f"""
        You extract {name} data based on markdown content.
        Keep all {name} from the markdown content.
        """
        response = client_openai.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"RAW_CONTENT: {markdown_content}"},
            ],
            response_format=Format,
        )
        json_extract = json.loads(response.choices[0].message.content)
        df = pd.DataFrame(json_extract['data'])
        df.to_csv(os.path.join(folder, f"{name}.csv"), index=False, sep='\t',  encoding='utf-16')
        msg = f"Success: Saved {df.shape[0]} {name} into the report."
    except Exception as e:
        msg = f"Error: {str(e)[:200]}"
    return msg

folder = 'temporary'
report_name = 'report.md'
def save_report(
        markdown_content: Annotated[str, "Markdown content of report"],
        report_name: Annotated[str, "Report name"],
        ) -> str:
    try:
      with open(os.path.join(folder, report_name+'.md'), 'w') as f:
          f.write(markdown_content)
      return f"Success: saved report to '{report_name+'.md'}'"
    except Exception as e:
        return f"Error: {str(e)[:200]}"
# print(save_report(markdown_content))

def read_report(
        report_name: Annotated[str, "Markdown report name"],        
        ) -> str:
    try:
        folder = 'temporary'
        report_name = 'report.md'
        with open(os.path.join(folder, report_name), 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)[:200]}"
# print(read_report(report_name))