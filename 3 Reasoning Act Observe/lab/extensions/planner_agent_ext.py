import json
import os
import re
from typing import Dict, Any

from llm_client import generate_json
from tools import TOOL_REGISTRY

SYS_INSTRUCTIONS = """
You are a planner for a small agent. You must respond with STRICT JSON ONLY.
Decide either:
1) The next ACTION to take by choosing one tool from: weather, wikipedia, calculator, news,
   and provide the required 'args' object.
   - Example: {"tool":"wikipedia","args":{"topic":"Jose Rizal"}}
   - Example: {"tool":"calculator","args":{"expression":"12.5 + 8.75"}}
   - Example: {"tool":"weather","args":{"city":"Tokyo"}}
   - Example: {"tool":"news","args":{"topic":"AI safety"}}
2) Or FINALIZE the answer:
   - Example: {"final":true,"answer":"... concise helpful answer ..."}

Rules:
- Output must be a single-line JSON object with double quotes.
- Do not include reasoning or extra text outside JSON.
- Prefer at most ONE action at a time.
- If you already have enough info to answer, finalize.
"""

def call_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    spec = TOOL_REGISTRY.get(tool_name)
    if not spec:
        return {"error": f"Unknown tool '{tool_name}'"}
    fn = spec["fn"]
    try:
        return fn(**args)
    except TypeError as e:
        return {"error": f"Bad args for {tool_name}: {e}"}
    except Exception as e:
        return {"error": f"Tool {tool_name} failed: {e}"}

def parse_json(s: str) -> Dict[str, Any]:
    s = (s or "").strip()
    m = re.search(r"\{.*\}", s, flags=re.S)
    if m:
        s = m.group(0)
    return json.loads(s)

def plan(context: str) -> Dict[str, Any]:
    prompt = f"""{SYS_INSTRUCTIONS}

Conversation so far:
{context}

Your JSON:
"""
    text = generate_json(prompt)
    return parse_json(text)

def run_agent(user_query: str, max_steps: int = 3) -> str:
    context = f"User: {user_query}\n"
    for step in range(1, max_steps + 1):
        try:
            decision = plan(context)
        except Exception:
            # Fallback: simple routing
            if "weather" in user_query.lower():
                decision = {"tool": "weather", "args": {"city": user_query}}
            elif "news" in user_query.lower():
                topic = re.sub(r".*news about ", "", user_query, flags=re.I).strip() or "technology"
                decision = {"tool": "news", "args": {"topic": topic}}
            elif any(k in user_query.lower() for k in ["who is", "what is", "about", "tell me"]):
                topic = re.sub(r"^(who is|what is|about|tell me about)\s*", "", user_query, flags=re.I)
                decision = {"tool": "wikipedia", "args": {"topic": topic or user_query}}
            else:
                decision = {"tool": "wikipedia", "args": {"topic": user_query}}

        if decision.get("final"):
            return decision.get("answer", "(no answer)")

        tool = decision.get("tool")
        args = decision.get("args", {})
        obs = call_tool(tool, args) if tool else {"error": "No tool specified"}
        context += f"Planner: {json.dumps(decision)}\nObservation: {json.dumps(obs)}\n"

        finalize_prompt = f"""{SYS_INSTRUCTIONS}
Here is the latest observation from your last action: {json.dumps(obs)}

If you can answer now, return {{"final":true,"answer":"..."}}
Otherwise, return the next {{"tool":...,"args":...}}.
"""
        try:
            decision = parse_json(generate_json(finalize_prompt))
        except Exception:
            return f"Based on the observation: {obs}. (The planner could not finalize.)"

        if decision.get("final"):
            return decision.get("answer", "(no answer)")
        else:
            context += f"Planner: {json.dumps(decision)}\n"

    return "I reached the step limit. Please ask again with more details."

def main():
    print("RAO Agent – Extensions (type 'quit' to exit)")
    while True:
        try:
            q = input("\nYour question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not q or q.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        answer = run_agent(q, max_steps=3)
        print("\n[Agent]:", answer)

if __name__ == "__main__":
    main()
