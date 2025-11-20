"""Chatbot router."""

from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/chat", tags=["chat"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/message")
@limiter.limit("10/minute")
def send_message(message: str):
    """Send a message to the chatbot."""
    return {"response": "Hello!"}
