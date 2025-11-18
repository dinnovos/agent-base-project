from typing import Literal

from agents.basic.state import State
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage

from .prompt import SYSTEM_PROMPT

llm = init_chat_model("openai:gpt-4o-mini", temperature=1)

def chatbot(state: State) -> dict:
    """Node that handles the chatbot logic"""

    # Add the system prompt to the messages
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    
    # Invoke the LLM without structured output to allow streaming
    response = llm.invoke(messages)
    
    return {"messages": [response]}