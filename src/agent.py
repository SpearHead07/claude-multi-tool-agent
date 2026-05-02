# src/agent.py
from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.nodes import call_model, tool_node
from src.edges import should_continue
from src.logger import get_logger

log = get_logger(__name__)


def build_agent():
    """Construct and compile the LangGraph agent."""
    log.info("Building agent graph")

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("call_model", call_model)
    workflow.add_node("execute_tools", tool_node)

    # Entry point
    workflow.set_entry_point("call_model")

    # Edges
    workflow.add_conditional_edges(
        "call_model",
        should_continue,
        {
            "execute_tools": "execute_tools",
            END: END,
        },
    )
    workflow.add_edge("execute_tools", "call_model")

    agent = workflow.compile()
    log.info("Agent compiled successfully")
    return agent


def run_agent(query: str, verbose: bool = False) -> str:
    """Run a single query through the agent. Returns the final answer."""
    agent = build_agent()

    initial_state: AgentState = {
        "messages": [{"role": "user", "content": query}]
    }

    if verbose:
        messages = []
        for chunk in agent.stream(initial_state):
            for node_name, node_output in chunk.items():
                print(f"\n[{node_name}]")
                for msg in node_output.get("messages", []):
                    print(f"  {msg}")
                    messages.append(msg)
        return messages[-1].content
    else:
        final_state = agent.invoke(initial_state)
        return final_state["messages"][-1].content