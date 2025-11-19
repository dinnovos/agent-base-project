import logging
from typing import Literal

from agents.basic.state import State
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, AIMessage

from .prompt import SYSTEM_PROMPT

# Configure logger for this module
logger = logging.getLogger(__name__)

# Initialize LLM
llm = init_chat_model("openai:gpt-4o-mini", temperature=1)

def chatbot(state: State) -> dict:
    """
    Node that handles the chatbot logic.
    
    Args:
        state: Current conversation state with messages
        
    Returns:
        dict: Updated state with LLM response
        
    Raises:
        Logs errors but returns graceful error message instead of raising
    """
    try:
        # Log incoming message
        message_count = len(state.get("messages", []))
        logger.debug(f"Processing chatbot node with {message_count} messages in state")
        
        # Add the system prompt to the messages
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        logger.debug(f"Total messages to send to LLM: {len(messages)}")
        
        # Invoke the LLM without structured output to allow streaming
        logger.info("Invoking LLM for response generation")
        response = llm.invoke(messages)
        
        logger.debug(f"LLM response received: {type(response).__name__}")
        logger.info("Chatbot node completed successfully")
        
        return {"messages": [response]}
        
    except Exception as e:
        logger.error(
            f"Error in chatbot node: {str(e)}",
            exc_info=True,  # Include full traceback
            extra={
                "error_type": type(e).__name__,
                "message_count": len(state.get("messages", []))
            }
        )
        
        # Return graceful error message to user
        error_message = AIMessage(
            content="I'm sorry, there was an error processing your message. Please try again."
        )

        return {"messages": [error_message]}