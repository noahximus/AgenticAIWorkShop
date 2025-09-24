import json
import re
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from llm_client import generate_text
from travel_tools import TOOL_REGISTRY

SYS = """
You are a **Travel Planner**. Respond with STRICT JSON ONLY.

Choose ONE of:
1) An action:
   {"tool":"<weather|wikipedia|distance|translate|parse_meta>","args":{...}}
2) Or finalize:
   {"final":true,"answer":"... friendly, practical, day-by-day itinerary ..."}

Rules:
- Output must be a single-line JSON object with double quotes.
- No extra text outside JSON.
- Prefer short iterative actions; finalize when sufficient.
- When finalizing, include: a brief overview, daily plan, weather note(s), 
  distances if relevant, and 2-4 must-try foods/experiences.
- If user asked to translate, you may call translate at the end.
- Use parse_meta when helpful to extract days/budget signal from the query.
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

def run_travel(query: str, max_steps: int = 6, translate_lang: Optional[str] = None, verbose: bool=False) -> Tuple[str, List[Dict[str, Any]]]:
    trace: List[Dict[str, Any]] = []
    context = f"User: {query}\n"

    def record(role: str, data: Dict[str, Any]):
        trace.append({"ts": datetime.utcnow().isoformat() + "Z", "role": role, "data": data})

    record("user", {"query": query})

    # Optionally hint the model if translation requested
    if translate_lang:
        context += f"Hint: user requested final translation to '{translate_lang}'.\n"

    for step in range(1, max_steps + 1):
        prompt = f"""{SYS}

Conversation so far:
{context}

Your JSON:
"""
        text = generate_text(prompt, temperature=0.3)
        try:
            decision = parse_json(text)
        except Exception:
            # Fallback: try parse_meta then wikipedia on first city found in query
            decision = {"tool": "parse_meta", "args": {"query": query}}
        record("planner", {"step": step, "decision": decision})

        if decision.get("final"):
            answer = decision.get("answer", "(no answer)")
            if translate_lang:
                # Final translation pass via tool if asked
                t = call_tool("translate", {"text": answer, "target_lang": translate_lang})
                if "translated" in t:
                    answer = t["translated"]
                    record("observation", {"step": step, "tool": "translate", "args": {"target_lang": translate_lang}, "observation": t})
            record("final", {"answer": answer})
            return answer, trace

        tool = decision.get("tool")
        args = decision.get("args", {})
        obs = call_tool(tool, args) if tool else {"error": "No tool specified"}
        record("observation", {"step": step, "tool": tool, "args": args, "observation": obs})
        context += f"Planner: {json.dumps(decision)}\nObservation: {json.dumps(obs)}\n"

        finalize = f"""{SYS}
Latest observation: {json.dumps(obs)}
If you can answer now, return {{"final":true,"answer":"..."}}
Otherwise, return the next {{"tool":...,"args":...}}.
"""
        text2 = generate_text(finalize, temperature=0.3)
        try:
            decision2 = parse_json(text2)
        except Exception:
            answer = f"Based on the observation: {obs}. (Planner could not finalize.)"
            record("final", {"answer": answer})
            return answer, trace
        record("planner", {"step": step, "decision": decision2})

        if decision2.get("final"):
            answer = decision2.get("answer", "(no answer)")
            if translate_lang:
                t = call_tool("translate", {"text": answer, "target_lang": translate_lang})
                if "translated" in t:
                    answer = t["translated"]
                    record("observation", {"step": step, "tool": "translate", "args": {"target_lang": translate_lang}, "observation": t})
            record("final", {"answer": answer})
            return answer, trace
        else:
            context += f"Planner: {json.dumps(decision2)}\n"

    answer = "I reached the step limit. Try a more specific travel request (cities, days, month, budget)."
    record("final", {"answer": answer})
    return answer, trace
