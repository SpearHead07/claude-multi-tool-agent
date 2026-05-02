# main.py
import argparse
from src.agent import run_agent
from src.logger import get_logger

log = get_logger(__name__)


def interactive_mode(verbose: bool):
    """Run an interactive chat session."""
    print("Multi-tool agent ready. Type 'exit' or 'quit' to leave.\n")
    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        try:
            response = run_agent(query, verbose=verbose)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            log.error(f"Agent failed: {e}")
            print(f"Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-tool AI agent powered by Claude + LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --query "what is 25 * 4"
  python main.py --interactive
  python main.py -q "today's date" -v
        """,
    )
    parser.add_argument("--query", "-q", type=str, help="Single query to run")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive chat")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show intermediate steps")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode(verbose=args.verbose)
    elif args.query:
        response = run_agent(args.query, verbose=args.verbose)
        print(response)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()