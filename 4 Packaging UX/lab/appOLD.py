import argparse
from rich.console import Console
from rich.panel import Panel

from agent_core import run
from config import MAX_STEPS_DEFAULT

def main():
    parser = argparse.ArgumentParser(description="Agentic AI – Module 4 (CLI)")
    parser.add_argument("query", nargs="?", help="Your question for the agent")
    parser.add_argument("--max-steps", type=int, default=MAX_STEPS_DEFAULT, help="Max reasoning steps")
    parser.add_argument("--provider", choices=["GEMINI","LMSTUDIO"], help="Override LLM provider for this run")
    parser.add_argument("--pretty", action="store_true", help="Pretty print the final answer")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return

    # Optional provider override (per-run)
    if args.provider:
        import os
        os.environ["LLM_PROVIDER"] = args.provider

    answer = run(args.query, max_steps=args.max_steps)

    console = Console()
    if args.pretty:
        console.print(Panel.fit(answer, title="Agent Answer", border_style="bold green"))
    else:
        print(answer)

if __name__ == "__main__":
    main()
