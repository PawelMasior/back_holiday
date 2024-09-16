from uvicorn import run
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException, File, UploadFile  # , Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('settings',f'ai-agents-project-key.json')
from dotenv import load_dotenv
load_dotenv()

with open(os.path.join(os.getcwd(), 'initialize.py')) as f:
    exec(f.read(), globals())

# =============================================================================
# FastAPI
# =============================================================================
app = FastAPI(
    title="My Holiday Planner",
    description='Plan my holiday trip',
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
def home(): return 'hello'
            
@app.get("/job/")#, tags=["APIs"], response_model=str)
def _stream(
        name_city: str = Query("Napoli"),
        desc_preferences: str = Query("I like discovering local specialities"),
        date_fr: str = Query("07-12-2024"),
        date_to: str = Query("14-12-2024"),
        bool_restaurants: bool = Query(True),
        bool_museums: bool = Query(True),
        bool_events: bool = Query(True),
        bool_local: bool = Query(True),
        bool_avoid: bool = Query(True),
        ):

    agents_tool = [agent_researcher] #filter here
    #agents_tool = [agent_researcher] #filter here
    agents_const = [agent_planner, agent_secretary]
    agents_chat = agents_const + agents_tool
    agents_transitions = {
        agent_planner: [agent_researcher, agent_secretary],
        agent_researcher: [agent_secretary],
        agent_secretary: [agent_planner],
    }
    group_chat = autogen.GroupChat(
        agents=agents_chat,
        messages=[],
        max_round=20,
        allowed_or_disallowed_speaker_transitions=agents_transitions,
        speaker_transitions_type="allowed",        
    )
    group_chat_manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_config,
        #{"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
    )
    for i, agent in enumerate(agents_chat): 
        if agent.name == 'Planner': pass
        else:
            agents_other = [a for i_a, a in enumerate(agents_chat) if i!=i_a]
            queue=[
                {"recipient": agent, "sender": executor, "summary_method": "last_msg"},
                {"recipient": group_chat_manager, "sender": agent, "summary_method": "reflection_with_llm"},
                ] + [{"recipient": a, "sender": agent, "summary_method": "reflection_with_llm"} for a in agents_other]
            agent.register_nested_chats(trigger=group_chat_manager, chat_queue=queue)
    # executor.register_nested_chats(
    #     trigger=agent_browser, 
    #     chat_queue=[{"recipient": agent_browser_assistant, 
    #                  "sender": agent_browser, 
    #                  "summary_method": "last_msg",
    #                  "max_turns": 1}])

    logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
    chat_results = agent_planner.initiate_chats([{
                "recipient": group_chat_manager,
                "message": f"""
                Complete Milestone: {t}

                # Additional intructions:
                    - Focuse on the Milestone and perform only necessary steps.                
                    - Go to next Milestone when previous Milestone is completed.
                    - Continue work untill Milestone goal is completed. 
                """,
                "max_turns": 20,
                "max_round": 60,
                "summary_method": "reflection_with_llm",
            } for t in Plan])
    autogen.runtime_logging.stop()

    # if not 'chat_results' in globals(): chat_results = [[]]
    # log_report(dbname, logging_session_id, task, Plan, chat_results)
    return 'Check conversation report'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    run(app, host="0.0.0.0", port=port)

