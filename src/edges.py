# src/edges.py
from langgraph.graph import END

from src.logger import get_logger
from src.state import AgentState

log = get_logger(__name__)


def should_continue(state: AgentState) -> str:
    """Router: decide whether to call tools or finish."""
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        log.info("Routing to: execute_tools")
        return "execute_tools"

    log.info("Routing to: END")
    return END