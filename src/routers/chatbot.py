from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from slowapi import Limiter
from slowapi.util import get_remote_address

from src.db.session import get_db
from src.models.user import User
from src.schemas.profile import ProfileRead, ProfileUpdate
from src.services.profile_service import get_profile_by_user_id, update_profile
from src.dependencies import get_current_user, verify_chatbot_rate_limit
from src.db.checkpoint import lifespan, CheckpointerDep
from src.db.database import SessionLocal

from src.services.usage_log_service import create_usage_log, check_chatbot_rate_limit
from src.schemas.usage_log import UsageLogCreate
from src.core.config import settings

from agents.basic.agent import make_graph
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse

import uuid

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
async def chat(
    request: Request, 
    item: Message, 
    checkpointer: CheckpointerDep, 
    current_user: User = Depends(verify_chatbot_rate_limit)
):
    """Endpoint de chat con rate limiting de 5 consultas cada 24 horas por usuario."""
    
    user_id = current_user.id
    agent = make_graph(config={"checkpointer": checkpointer})

    state = {
        "messages": [HumanMessage(content=item.message)],
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    config = {
        "configurable": {
            "thread_id": f"thread-{user_id}",
        },
        "user_id": user_id,
        "main_call_tid": f"parent-{uuid.uuid4()}",
    }

    response = await agent.ainvoke(state, config=config)

    message = response["messages"][-1]

    return message.content

@router.post("/stream")
@limiter.limit("10/minute")
async def stream_chat(
    request: Request, 
    item: Message, 
    checkpointer: CheckpointerDep, 
    current_user: User = Depends(verify_chatbot_rate_limit)
):
    """Endpoint de chat streaming con rate limiting de 5 consultas cada 24 horas por usuario."""
    
    user_id = current_user.id
    
    config = {
        "configurable": {
            "thread_id": f"thread-{user_id}",
        },
        "user_id": user_id,
        "main_call_tid": f"parent-{uuid.uuid4()}",
    }

    human_message = HumanMessage(content=item.message)

    async def generate_response():
        agent = make_graph(config={"checkpointer": checkpointer})

        async for message_chunk, metadata in agent.astream({"messages": [human_message]}, stream_mode="messages", config=config):
            if message_chunk.content:
                yield f"data: {message_chunk.content}\n\n"

    return StreamingResponse(generate_response(), media_type="text/event-stream")


@router.get("/usage")
async def get_usage(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el uso actual de consultas del usuario al chatbot.
    
    Retorna:
    - used: Número de consultas realizadas en las últimas 24 horas
    - remaining: Número de consultas restantes
    - limit: Límite total de consultas por ventana de tiempo
    - window_hours: Ventana de tiempo en horas
    """
    can_query, used, remaining = check_chatbot_rate_limit(db, current_user.id)
    
    return {
        "used": used,
        "remaining": remaining,
        "limit": settings.CHATBOT_QUERY_LIMIT,
        "window_hours": settings.CHATBOT_QUERY_WINDOW_HOURS,
        "can_query": can_query
    }