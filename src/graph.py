from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.nodes import call_model, tool_node
from src.edges import should_continue


def build_graph():
    """Construct and compile the agent graph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("call_model", call_model)
    workflow.add_node("execute_tools", tool_node)

    workflow.set_entry_point("call_model")

    workflow.add_conditional_edges(
        "call_model",
        should_continue,
        {
            "execute_tools": "execute_tools",
            END: END,
        },
    )

    workflow.add_edge("execute_tools", "call_model")

    return workflow.compile()
