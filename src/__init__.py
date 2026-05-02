# tools/__init__.py


# Why this matters: This file declares what the outside world can import from your agent package. 
# Anyone using your code does from agent import build_graph and gets exactly what they need — 
# without poking into internals.
# This is called encapsulation. Internals (nodes, edges, tools) are implementation details. 
# The public API is build_graph() and AgentState. You can refactor everything inside without breaking 
# external code, as long as the public API stays stable.