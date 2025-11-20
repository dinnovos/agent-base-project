"""Basic agent implementation."""

from langgraph.graph import StateGraph


def make_graph():
    """Create and return the agent graph."""
    # TODO: Implement your agent graph here
    graph = StateGraph(dict)
    return graph.compile()
