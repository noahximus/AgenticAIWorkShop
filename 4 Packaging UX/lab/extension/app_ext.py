import argparse, json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_core_ext import run
from config import MAX_STEPS_DEFAULT

def main():
    parser = argparse.ArgumentParser(description="Agentic AI – Module 4 Extensions")
    parser.add_argument("query", nargs="?", help="Your question for the agent")
    parser.add_argument("--max-steps", type=int, default=MAX_STEPS_DEFAULT, help="Max reasoning steps")
    parser.add_argument("--provider", choices=["GEMINI","LMSTUDIO"], help="Override LLM provider for this run")
    parser.add_argument("--pretty", action="store_true", help="Pretty print the final answer")
    parser.add_argument("--json", action="store_true", help="Output a JSON object (answer + trace)")
    parser.add_argument("--verbose", action="store_true", help="Show step-by-step decisions and observations")
    parser.add_argument("--transcript", type=str, help="Write transcript JSONL to this file")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        return

    if args.provider:
        import os
        os.environ["LLM_PROVIDER"] = args.provider

    answer, trace = run(args.query, max_steps=args.max_steps, verbose=args.verbose, transcript_file=args.transcript)

    console = Console()

    if args.json:
        print(json.dumps({"answer": answer, "trace": trace}, ensure_ascii=False, indent=2))
        return

    if args.verbose:
        table = Table(title="Reason–Act–Observe Trace")
        table.add_column("Step/Role", style="bold cyan")
        table.add_column("Data")
        for rec in trace:
            role = rec.get("role","")
            data = rec.get("data",{})
            table.add_row(role, json.dumps(data, ensure_ascii=False)[:2000])
        console.print(table)

    if args.pretty:
        console.print(Panel.fit(answer, title="Agent Answer", border_style="bold green"))
    else:
        print(answer)

if __name__ == "__main__":
    main()
