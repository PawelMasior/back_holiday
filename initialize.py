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

from tools.selenium import *
from tools.web import web_search, web_page
from tools.twilio import sms_send, sms_inbox
from tools.info import *
from tools.excel import save_excel
from tools.capcha import solve_recapcha

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

autogen.register_function(save_excel, caller=agent_secretary, executor=executor,
    name="save_excel",
    description="""
    Saves data in csv format.
    """
)
