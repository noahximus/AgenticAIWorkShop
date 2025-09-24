import json
import re
from typing import Dict, Any

from llm_client import generate_text
from tools import TOOL_REGISTRY

SYS = """
You are a planner for a small agent. Respond with STRICT JSON ONLY.
Choose ONE of:
- An action: {"tool":"<weather|wikipedia|calculator>","args":{...}}
- A final answer: {"final":true,"answer":"..."}

Rules:
- Output must be a single-line JSON object with double quotes.
- Do not include reasoning or extra text outside JSON.
- If you already have enough info to answer, finalize.
"""

def parse_json(s: str) -> Dict[str, Any]:
    s = (s or "").strip()
    m = re.search(r"\{.*\}", s, flags=re.S)
    if m:
        s = m.group(0)
    return json.loads(s)

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

def step(context: str) -> Dict[str, Any]:
    prompt = f"""{SYS}

Conversation so far:
{context}

Your JSON:
"""
    text = generate_text(prompt, temperature=0.2)
    return parse_json(text)

def run(user_query: str, max_steps: int = 4) -> str:
    context = f"User: {user_query}\n"
    for _ in range(max_steps):
        try:
            decision = step(context)
        except Exception:
            decision = {"tool": "wikipedia", "args": {"topic": user_query}}

        if decision.get("final"):
            return decision.get("answer", "(no answer)")

        tool = decision.get("tool")
        args = decision.get("args", {})
        obs = call_tool(tool, args) if tool else {"error": "No tool specified"}
        context += f"Planner: {json.dumps(decision)}\nObservation: {json.dumps(obs)}\n"

        finalize = f"""{SYS}
Latest observation: {json.dumps(obs)}
If you can answer now, return {{"final":true,"answer":"..."}}
Otherwise, return the next {{"tool":...,"args":...}}.
"""
        try:
            decision = parse_json(generate_text(finalize, temperature=0.2))
        except Exception:
            return f"Based on the observation: {obs}. (Planner could not finalize.)"

        if decision.get("final"):
            return decision.get("answer", "(no answer)")
        else:
            context += f"Planner: {json.dumps(decision)}\n"

    return "I reached the step limit. Try a more specific query."
