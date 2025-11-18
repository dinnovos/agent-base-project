from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.basic.state import State

from agents.basic.nodes.chatbot.node import chatbot

def make_graph(config: TypedDict):

    checkpointer = config.get("checkpointer")
    # build the graph
    workflow = StateGraph(State)
    workflow.add_node("chatbot", chatbot)

    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)

    # compile the graph with checkpointer for state persistence
    # Using PostgreSQL for persistent checkpoints

    return workflow.compile(checkpointer=checkpointer)
