import json
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from llm_client import generate_text
from tools_ext import TOOL_REGISTRY

SYS = """
You are a planner for a small agent. Respond with STRICT JSON ONLY.
Choose ONE of:
- An action: {"tool":"<weather|wikipedia|calculator|news|translate>","args":{...}}
- A final answer: {"final":true,"answer":"..."}

Rules:
- Output must be a single-line JSON object with double quotes.
- Do not include reasoning or extra text outside JSON.
- If you already have enough info to answer, finalize.
- For translate: args must include {"text":"...","target_lang":"<lang-code>"} (e.g., "tl","es","fr").
- For news: args must include {"topic":"..."}.
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

def _record(trace: List[Dict[str, Any]], role: str, data: Dict[str, Any]):
    trace.append({"ts": datetime.utcnow().isoformat() + "Z", "role": role, "data": data})

def run(user_query: str, max_steps: int = 5, verbose=False, transcript_file: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]]]:
    trace: List[Dict[str, Any]] = []
    context = f"User: {user_query}\n"
    _record(trace, "user", {"query": user_query})

    for step in range(1, max_steps + 1):
        prompt = f"""{SYS}

Conversation so far:
{context}

Your JSON:
"""
        text = generate_text(prompt, temperature=0.2)
        try:
            decision = parse_json(text)
        except Exception:
            # Fallback: route to wikipedia by default
            decision = {"tool": "wikipedia", "args": {"topic": user_query}}
        _record(trace, "planner", {"step": step, "decision": decision})

        if decision.get("final"):
            answer = decision.get("answer", "(no answer)")
            _record(trace, "final", {"answer": answer})
            if transcript_file:
                with open(transcript_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(trace[-1]) + "\n")
            return answer, trace

        tool = decision.get("tool")
        args = decision.get("args", {})
        obs = call_tool(tool, args) if tool else {"error": "No tool specified"}
        _record(trace, "observation", {"step": step, "tool": tool, "args": args, "observation": obs})
        context += f"Planner: {json.dumps(decision)}\nObservation: {json.dumps(obs)}\n"

        finalize = f"""{SYS}
Latest observation: {json.dumps(obs)}
If you can answer now, return {{"final":true,"answer":"..."}}
Otherwise, return the next {{"tool":...,"args":...}}.
"""
        text2 = generate_text(finalize, temperature=0.2)
        try:
            decision2 = parse_json(text2)
        except Exception:
            answer = f"Based on the observation: {obs}. (Planner could not finalize.)"
            _record(trace, "final", {"answer": answer})
            if transcript_file:
                with open(transcript_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(trace[-1]) + "\n")
            return answer, trace
        _record(trace, "planner", {"step": step, "decision": decision2})

        if decision2.get("final"):
            answer = decision2.get("answer", "(no answer)")
            _record(trace, "final", {"answer": answer})
            if transcript_file:
                with open(transcript_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(trace[-1]) + "\n")
            return answer, trace
        else:
            context += f"Planner: {json.dumps(decision2)}\n"

        if transcript_file:
            with open(transcript_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(trace[-1]) + "\n")

    # Step cap reached
    answer = "I reached the step limit. Try a more specific query."
    _record(trace, "final", {"answer": answer})
    if transcript_file:
        with open(transcript_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace[-1]) + "\n")
    return answer, trace
