from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.db.session import get_db
from src.models.user import User
from src.schemas.profile import ProfileRead, ProfileUpdate
from src.services.profile_service import get_profile_by_user_id, update_profile
from src.dependencies import get_current_user
from src.db.checkpoint import lifespan, CheckpointerDep

from agents.basic.agent import make_graph
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chatbot", tags=["Chatbot"], lifespan=lifespan)

# Create limiter instance (will be configured in main.py)
limiter = Limiter(key_func=get_remote_address)

class Message(BaseModel):
    message: str = Field(
        min_length=1, 
        max_length=2000,
        description="Query message for the chatbot"
    )

@router.post("/")
@limiter.limit("10/minute")
async def chat(request: Request, item: Message, checkpointer: CheckpointerDep, current_user: User = Depends(get_current_user)):

    config = {
        "configurable": {
            "thread_id": f"thread-{current_user.id}",
        }
    }

    agent = make_graph(config={"checkpointer": checkpointer})

    state = {"messages": [HumanMessage(content=item.message)]}
    response = await agent.ainvoke(state, config=config)

    message = response["messages"][-1]

    return message.content

@router.post("/stream")
@limiter.limit("10/minute")
async def stream_chat(request: Request, item: Message, checkpointer: CheckpointerDep, current_user: User = Depends(get_current_user)):

    config = {
        "configurable": {
            "thread_id": f"thread-{current_user.id}",
        }
    }

    human_message = HumanMessage(content=item.message)

    async def generate_response():
        agent = make_graph(config={"checkpointer": checkpointer})

        async for message_chunk, metadata in agent.astream({"messages": [human_message]}, stream_mode="messages", config=config):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"

    return StreamingResponse(generate_response(), media_type="text/event-stream")