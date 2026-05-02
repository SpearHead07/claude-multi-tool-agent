# src/nodes.py
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode

from src.config import MODEL_NAME, ANTHROPIC_API_KEY, TEMPERATURE
from src.logger import get_logger
from src.state import AgentState
from tools import ALL_SCHEMAS, REGISTRY

log = get_logger(__name__)

# Initialise model once at module load
_model = ChatAnthropic(  # type: ignore[call-arg]
        model_name=MODEL_NAME,
        api_key=ANTHROPIC_API_KEY,
        temperature=TEMPERATURE,
).bind_tools(ALL_SCHEMAS)


def call_model(state: AgentState) -> dict:
    """Send conversation to Claude. Returns the model's response."""
    log.info(f"call_model invoked with {len(state['messages'])} messages")
    response = _model.invoke(state["messages"])

    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_names = [tc["name"] for tc in response.tool_calls]
        log.info(f"Claude requested tools: {tool_names}")
    else:
        log.info("Claude returned final answer")

    return {"messages": [response]}


# LangGraph's built-in tool executor
tool_node = ToolNode(list(REGISTRY.values()))