# Claude Multi-Tool Agent

A production-ready AI agent built with **Anthropic Claude** and **LangGraph** — supports multi-tool reasoning, graceful error recovery, and full observability via structured logging. Ships with a CLI for single queries, interactive chat, and verbose debugging.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green)
![Anthropic](https://img.shields.io/badge/Claude-Opus%204.5-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## Overview

Most LLM tutorials show you how to call an API. Few show you how to build an agent that handles failure gracefully, routes between multiple tools intelligently, and produces structured logs you can debug in production.

This project is a from-scratch implementation of a multi-tool agent using Anthropic's Claude API and LangGraph. It demonstrates the core patterns — **tool routing via descriptions**, **errors-as-conversation**, **graph-based state management**, and **modular code structure** — that production agent systems are built on.

The agent currently supports two tools (calculator and date) but the architecture is designed so that adding a new tool is a 4-line change, with no modifications to the agent loop, the graph, or the CLI.

---

## Architecture

![Architecture](assets/architecture.png)

The agent is a LangGraph state machine with two nodes and one router:


- **`call_model`** sends the conversation to Claude with bound tool schemas
- **`execute_tools`** is LangGraph's built-in `ToolNode`, wired to a tool registry
- **`should_continue`** is the router — checks the last message for tool calls, routes to either `execute_tools` or `END`

State flows through the graph as a typed `messages` list, using `add_messages` as a reducer so updates append rather than replace.

---

## Tech Stack

- **Language** — Python 3.10+
- **LLM** — Anthropic Claude (Opus 4.5)
- **Framework** — LangGraph for state machine, LangChain Anthropic for model binding
- **CLI** — argparse (standard library)
- **Logging** — Python `logging` module with module-named loggers
- **Config** — python-dotenv for environment variable loading

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/claude-multi-tool-agent.git
cd claude-multi-tool-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp .env.example .env
# Open .env and paste your ANTHROPIC_API_KEY

# 4. Run a single query
python main.py --query "what is 25 * 4 and what's today's date"

# Or start an interactive chat session
python main.py --interactive

# Or run with verbose mode to see every step
python main.py -q "what is 12 * 12" -v
```

---

## CLI Reference

```bash
python main.py --help
```

| Flag | Short | Description |
|---|---|---|
| `--query "..."` | `-q` | Run a single query and exit |
| `--interactive` | `-i` | Start an interactive chat session |
| `--verbose` | `-v` | Stream intermediate steps (every node execution) |
| `--help` | `-h` | Show usage docs |

---

## Project Structure

Each file has a single responsibility. The dependency arrow flows one way: `main → src → tools`. Adding a new tool is a 4-line change — one new file in `tools/`, three lines in `tools/__init__.py`. No agent or graph code changes.

---

## How Tool Routing Works

There is **no `if/else` routing logic in this codebase.** Claude reads the `description` field on each tool's JSON schema and decides which tool to call. Sharp descriptions = correct routing. Vague descriptions = wrong tool calls.

Each description follows a "use when / do NOT use when" pattern:

```python
"description": (
    "Performs mathematical calculations. Use this when the user asks to compute, "
    "add, subtract, multiply, divide, or evaluate any math expression. "
    "Do NOT use for date or text questions."
)
```

The "Do NOT use for…" clause measurably improves routing accuracy, especially on ambiguous queries.

---

## Error Handling Philosophy

Errors are not crashes — they are **conversational turns**. When a tool fails, it returns the error as a string instead of raising an exception. Claude reads the error message in the next turn and reasons about what to do — retry with different input, ask the user for clarification, or apologise and stop.

This means the agent loop never breaks on tool failures. It just continues with new context.

```python
try:
    result = eval(expression)
    return f"{expression} = {result}"
except Exception as e:
    log.error(f"calculator failed: {e}")
    return f"Error: {str(e)}"   # returned as a string, not raised
```

---

## Logging

Every tool call, model invocation, and routing decision is logged with a timestamp, severity level, and module name:

This is the agent's nervous system — debugging without it is impossible. Severity levels: `INFO` for normal flow, `WARNING` for unusual inputs (rejected expressions, empty results), `ERROR` for failures.

---

## What I Learned

- **Tool descriptions are the routing layer.** Claude picks tools by reading text, not running code. Sharpening descriptions with explicit "use when / do NOT use when" clauses dramatically improves routing accuracy.
- **Errors are conversational turns, not crashes.** Returning errors as strings (instead of raising) lets the agent self-correct on the next turn. The loop never dies.
- **Graphs replace loops once complexity grows.** A `while True` loop works for one tool. With multiple tools, conditional routing, and future human-in-the-loop, LangGraph's State + Nodes + Edges scales where loops break.
- **Modular structure matters more than line count.** Splitting a 200-line script into 12 small files with single responsibilities makes the same code dramatically easier to extend, test, and explain.
- **Centralised config + structured logging are not optional.** They cost 30 minutes to set up and save hours later. Every production codebase has them — there's a reason.

---

## Future Work

- [ ] Add a `web_search` tool with DuckDuckGo or Tavily
- [ ] Add memory / multi-turn conversation persistence (LangGraph `MemorySaver` → SQLite)
- [ ] Build a Streamlit UI for non-technical users
- [ ] Add human-in-the-loop interrupts before destructive tool calls
- [ ] Write unit tests for each tool (`pytest`)
- [ ] Add automated evals to score agent responses against a fixed test set
- [ ] Deploy to Render or Railway with proper secret management

---

## License

MIT — see [LICENSE](LICENSE) file.

---

## Author

Built by **Ashish** as part of a 30-day journey to AI Engineer.

🔗 [LinkedIn](https://www.linkedin.com/in/ashish-srimal-95605698/?skipRedirect=true) · [GitHub](https://github.com/SpearHead07)
