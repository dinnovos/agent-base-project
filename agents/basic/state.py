from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing import Annotated

class State(MessagesState):
    messages: Annotated[list[BaseMessage], add_messages]
    