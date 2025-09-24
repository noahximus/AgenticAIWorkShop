# Module 4 Agent Core (Patched)
# - Normalizes weather tool args (accepts 'location'/'city_name' -> 'city')
# - Stronger JSON-only planner prompt
# - Safe JSON parsing + visible loop logs

import json
import re
from typing import Dict, Any, List
from datetime import datetime

from llm_client import generate_text  # must exist in your Module 4
from tools import TOOL_REGISTRY       # patched tools.py in this folder

SYS = """
You are a strict planner for a CLI agent. Reply with STRICT JSON ONLY.
Choose EXACTLY one of:
1) An action:
   {"tool":"<weather|wikipedia|calculator>","args":{...}}
2) A final answer:
   {"final":true,"answer":"..."}

Rules:
- Respond with a SINGLE JSON object (one line), no markdown/prose.
- If the user asks for weather, you MUST call {"tool":"weather","args":{"city":"Tokyo"}}.
  (do NOT use keys like "location" or "city_name").
- For tasks needing facts (Wikipedia) or math (calculator), call a tool before finalizing.
- For multi-city weather, call weather once per city, then calculator to combine.
- If parameters are missing, return a FINAL answer asking a concise clarification question.
"""

def _extract_json(s: str) -> Dict[str, Any]:
    s = (s or "").strip()
    try:
        return json.loads(s)
    except Exception:
        pass
    m = re.search(r"\{.*\}", s, flags=re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return {}

def _valid(d: Dict[str, Any]) -> bool:
    if "tool" in d and isinstance(d.get("args"), dict):
        return True
    if d.get("final") is True and isinstance(d.get("answer"), str):
        return True
    return False

def _reprompt_fix(msg: str) -> Dict[str, Any]:
    out = generate_text(f"Fix the structure. {msg}. Return ONE valid JSON object only.")
    return _extract_json(out)

def call_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    # --- normalize common mistakes from the model ---
    if tool_name == "weather" and isinstance(args, dict):
        if "city" not in args:
            if "location" in args:
                args["city"] = args.pop("location")
            elif "city_name" in args:
                args["city"] = args.pop("city_name")
    # ------------------------------------------------
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

def run(query: str, max_steps: int = 6) -> Dict[str, Any]:
    trace: List[Dict[str, Any]] = []
    context = f"User: {query}\n"

    def record(role: str, data: Dict[str, Any]):
        trace.append({"ts": datetime.utcnow().isoformat() + "Z", "role": role, "data": data})

    record("user", {"query": query})

    for step in range(1, max_steps + 1):
        prompt = f"""{SYS}

Conversation so far:
{context}

Your JSON:"""
        out = generate_text(prompt)
        decision = _extract_json(out)
        if not _valid(decision):
            decision = _reprompt_fix("Missing 'tool' or 'final'. Either choose a tool with args, or finalize with an answer.")
        record("planner", {"step": step, "decision": decision})

        if decision.get("final"):
            ans = decision.get("answer", "(no answer)")
            record("final", {"answer": ans})
            return {"answer": ans, "trace": trace}

        tool = decision.get("tool")
        args = decision.get("args", {}) or {}
        obs = call_tool(tool, args) if tool else {"error": "No tool specified"}
        record("observation", {"step": step, "tool": tool, "args": args, "observation": obs})
        context += f"Planner: {json.dumps(decision)}\nObservation: {json.dumps(obs)}\n"

        finalize = f"""{SYS}
Latest observation: {json.dumps(obs, ensure_ascii=False)}
If you can answer now, return {{"final":true,"answer":"..."}}
Otherwise, return the next {{"tool":...,"args":...}}.
Your JSON:"""
        out2 = generate_text(finalize)
        decision2 = _extract_json(out2)
        if not _valid(decision2):
            decision2 = _reprompt_fix("Finalize with answer or pick the next tool. JSON only.")
        record("planner", {"step": step, "decision": decision2})

        if decision2.get("final"):
            ans = decision2.get("answer", "(no answer)")
            record("final", {"answer": ans})
            return {"answer": ans, "trace": trace}
        else:
            context += f"Planner: {json.dumps(decision2)}\n"

    ans = "I reached the step limit. Try a more specific query."
    record("final", {"answer": ans})
    return {"answer": ans, "trace": trace}