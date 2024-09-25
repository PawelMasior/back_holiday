import os
import re
import json
from settings.func import * 
from firecrawl import FirecrawlApp
import openai
from openai import OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI()
firecrawl = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])
from typing import Annotated, Literal

def firecrawl_page(
        url: Annotated[str, "Url"],
        context: Annotated[str, "Information you want to identify."],
    ) -> str:
    
    page_content = firecrawl.scrape_url(
        url=url,
        params={
            "pageOptions":{
                "onlyMainContent": True
            }
        })
    web_content = page_content['markdown']
    if nr_tokens(web_content) > 3000:
        web_prompt = f"""Task: {context} 
        Concise page information into the report in a clear and organized manner.
        Keep URLs where applicable.
        
        Page content: 
        {web_content}
        """
        response = client_openai.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {
                "role": "user",
                "content": [{ "type": "text", "text": web_prompt,},],
            }
          ],
          max_tokens=4000,
          temperature=0.
        )
        web_content = response.choices[0].message.content
    return web_content


def firecrawl_page_raw(
        url: Annotated[str, "Url"],
    ) -> str:
    
    page_content = firecrawl.scrape_url(
        url=url,
        params={
            "pageOptions":{
                "onlyMainContent": True
            }
        })
    web_content = page_content['markdown']
    return web_content