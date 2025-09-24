#!/usr/bin/env python3
# Module 4 app.py (Patched)
# - Correctly renders answer strings (avoids Rich NotRenderableError)
# - Supports --pretty, --json, --verbose
# - Graceful fallback if Rich isn't installed

import argparse
import json
import sys

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    RICH_AVAILABLE = True
except Exception:
    RICH_AVAILABLE = False

# Your patched agent core (from module4 patches)
import agent_core  # must provide run(query, max_steps=...) -> {"answer": str, "trace": [...]}

def render_pretty(result):
    """Pretty-print the agent result using Rich if available; fallback otherwise."""
    answer = result.get("answer", "")
    trace = result.get("trace", [])

    if not RICH_AVAILABLE:
        print("=== Agent Answer ===")
        print(answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False))
        if trace:
            print("\n=== Trace ===")
            print(json.dumps(trace, indent=2, ensure_ascii=False))
        return

    console = Console()

    # Answer panel
    answer_str = answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False)
    console.print(Panel.fit(answer_str, title="Agent Answer", border_style="bold green"))

    # Trace table (if any)
    if trace:
        table = Table(title="Trace", show_header=True, header_style="bold cyan")
        table.add_column("ts", no_wrap=True)
        table.add_column("role")
        table.add_column("data")
        for item in trace:
            ts = item.get("ts", "")
            role = item.get("role", "")
            data = json.dumps(item.get("data", {}), ensure_ascii=False)
            table.add_row(ts, role, data)
        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Agentic AI – Module 4 CLI")
    parser.add_argument("query", type=str, help="Your question/prompt")
    parser.add_argument("--max-steps", type=int, default=6, help="Max planner steps")
    parser.add_argument("--pretty", action="store_true", help="Pretty print with Rich")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output full JSON result")
    parser.add_argument("--verbose", action="store_true", help="Also print trace (ignored if --json)")

    args = parser.parse_args()

    # Run the agent
    result = agent_core.run(args.query, max_steps=args.max_steps)
    # result is a dict: {"answer": str, "trace": [...]}

    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.pretty:
        render_pretty(result)
        return

    # Plain stdout
    answer = result.get("answer", "")
    print(answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False))

    if args.verbose and result.get("trace"):
        print("\n--- TRACE ---")
        print(json.dumps(result["trace"], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)