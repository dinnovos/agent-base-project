import logging
import uuid
from typing import Literal
from langchain_core.runnables import RunnableConfig
from agents.basic.state import State
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler
from langchain_core.messages import SystemMessage, AIMessage

from src.db.database import SessionLocal

from src.services.usage_log_service import create_usage_log
from src.schemas.usage_log import UsageLogCreate

from .prompt import SYSTEM_PROMPT

# Configure logger for this module
logger = logging.getLogger(__name__)

llm_model = "openai:gpt-4o-mini"
llm_temperature = 1

# Initialize LLM
llm = init_chat_model(llm_model, temperature=llm_temperature)

def chatbot(state: State, config: RunnableConfig) -> dict:
    """
    Node that handles the chatbot logic.
    
    Args:
        state: Current conversation state with messages
        
    Returns:
        dict: Updated state with LLM response
        
    Raises:
        Logs errors but returns graceful error message instead of raising
    """

    # Extract user_id from config
    # In LangGraph, custom context is passed at the top level of config
    user_id = config.get("user_id") if isinstance(config, dict) else None
    main_call_tid = config.get("main_call_tid") if isinstance(config, dict) else None
    
    # Fallback: try to get from configurable
    if not user_id and isinstance(config, dict):
        user_id = config.get("configurable", {}).get("user_id")
    
    if not main_call_tid and isinstance(config, dict):
        main_call_tid = config.get("configurable", {}).get("main_call_tid")
    
    logger.debug(f"Extracted user_id from config: {user_id}")
    logger.debug(f"Full config keys: {config.keys() if isinstance(config, dict) else 'Not a dict'}")

    callback = UsageMetadataCallbackHandler()

    try:
        # Log incoming message
        message_count = len(state.get("messages", []))
        logger.debug(f"Processing chatbot node with {message_count} messages in state")
        
        # Add the system prompt to the messages
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        logger.debug(f"Total messages to send to LLM: {len(messages)}")
        
        # Invoke the LLM without structured output to allow streaming
        logger.info("Invoking LLM for response generation")

        response = llm.invoke(messages, config={"callbacks": [callback]})
        
        logger.debug(f"LLM response received: {type(response).__name__}")
        logger.info("Chatbot node completed successfully")

        # Process usage logs
        totals = process_usage_logs(callback, user_id, main_call_tid)

        return {
            "messages": [response],
            "input_tokens": totals.get("input_tokens", 0),
            "output_tokens": totals.get("output_tokens", 0),
            "total_tokens": totals.get("total_tokens", 0)
        }
        
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

def process_usage_logs(callback: UsageMetadataCallbackHandler, user_id: int, main_call_tid: str) -> dict:

    input_tokens = 0
    output_tokens = 0
    total_tokens = 0

    try:

        db = SessionLocal()

        # Extract token usage from callback
        # usage_metadata structure: {"model-name": {"input_tokens": X, "output_tokens": Y, ...}}
        usage_metadata = callback.usage_metadata or {}
        
        logger.debug(f"Usage metadata: {usage_metadata}")
        
        # Iterate over each model in usage_metadata and create a log entry for each
        for model_name, model_tokens in usage_metadata.items():
            try:

                input_tokens += model_tokens.get("input_tokens", 0)
                output_tokens += model_tokens.get("output_tokens", 0)
                total_tokens += model_tokens.get("total_tokens", 0)

                usage_data = UsageLogCreate(
                    main_call_tid=str(main_call_tid),
                    node_call_tid=f"node-{str(uuid.uuid4())}",
                    description="Node chatbot",
                    model=model_name,
                    inputs=model_tokens.get("input_tokens", 0),
                    outputs=model_tokens.get("output_tokens", 0),
                    total=model_tokens.get("total_tokens", 0),
                )
                
                logger.debug(f"Creating usage log for model: {model_name}, tokens: {model_tokens}")
                
                create_usage_log(
                    db,
                    user_id=user_id,
                    usage_data=usage_data,
                )
                
            except Exception as model_error:
                logger.error(f"Error creating usage log for model {model_name}: {str(model_error)}")

    except Exception as e:
        logger.error(f"Error processing usage logs: {str(e)}")

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }