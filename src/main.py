from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from .agent import build_agent

load_dotenv()
app = FastAPI()
agent = build_agent()

class MessageContext(BaseModel):
    user_id: int
    chat_id: int
    message_text: str
    is_admin: bool
    sfw: bool

@app.post("/process_message")
async def process_message(message_context: MessageContext):
    initial_state = {
        "user_id": message_context.user_id,
        "chat_id": message_context.chat_id,
        "message_text": message_context.message_text,
        "is_admin": message_context.is_admin,
        "sfw": message_context.sfw,
        "response": None,
        "tool_output": None,
        "web_search_results": None,
        "denial_message": None,
        "retrieved_context": None,
        "user_profile": None,
        "group_settings": None,
        "intent": None,
    }
    final_state = agent.invoke(initial_state)
    return {"response": final_state.get("response")}

@app.get("/")
async def root():
    return {"message": "CookieBaker AI 2.0"}
