from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.user import User
from src.schemas.profile import ProfileRead, ProfileUpdate
from src.services.profile_service import get_profile_by_user_id, update_profile
from src.dependencies import get_current_user
from src.db.checkpoint import lifespan, CheckpointerDep

from agents.basic.agent import make_graph
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chatbot", tags=["Chatbot"], lifespan=lifespan)

class Message(BaseModel):
    message: str

@router.post("/")
async def chat(item: Message, checkpointer: CheckpointerDep):

    config = {
        "configurable": {
            "thread_id": "1",
        }
    }

    agent = make_graph(config={"checkpointer": checkpointer})

    state = {"messages": [HumanMessage(content=item.message)]}
    response = await agent.ainvoke(state, config=config)

    message = response["messages"][-1]

    return message.content

@router.post("/stream")
async def stream_chat(item: Message, checkpointer: CheckpointerDep):

    config = {
        "configurable": {
            "thread_id": "2",
        }
    }

    human_message = HumanMessage(content=item.message)

    async def generate_response():
        agent = make_graph(config={"checkpointer": checkpointer})

        async for message_chunk, metadata in agent.astream({"messages": [human_message]}, stream_mode="messages", config=config):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"

    return StreamingResponse(generate_response(), media_type="text/event-stream")