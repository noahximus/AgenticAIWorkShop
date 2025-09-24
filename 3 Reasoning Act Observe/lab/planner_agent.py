
import os, re, json
from typing import Dict, Any, List

# ==== LLM (Gemini) for FINAL NARRATION ONLY ====
import google.generativeai as genai
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")
genai.configure(api_key=API_KEY)
_model = genai.GenerativeModel("gemini-1.5-flash")

# ==== Tools ====
import requests

CITY_COORDS = {
    "manila": (14.5995, 120.9842),
    "tokyo": (35.6762, 139.6503),
    "singapore": (1.3521, 103.8198),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "sydney": (-33.8688, 151.2093),
    "kyoto": (35.0116, 135.7681),
    "osaka": (34.6937, 135.5023),
}

def tool_weather(city: str) -> Dict[str, Any]:
    target = (city or "").lower().strip()
    if target not in CITY_COORDS:
        for k in CITY_COORDS:
            if k in target:
                target = k
                break
    if target not in CITY_COORDS:
        return {"error": f"Unknown city '{city}'"}
    lat, lon = CITY_COORDS[target]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    temps = data.get("hourly", {}).get("temperature_2m", [])
    now_c = temps[0] if temps else None
    return {"city": target.title(), "temp_now_c": now_c, "source": "Open-Meteo hourly temperature_2m"}

def tool_wikipedia(topic: str) -> Dict[str, Any]:
    topic = (topic or "").strip()
    if not topic:
        return {"topic": topic, "summary": None, "error": "empty topic"}
    title = topic.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    headers = {"User-Agent": "AgenticAIWorkshop/1.0 (https://example.com/; contact@example.com)"}
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code in (400, 404):
        return {"topic": topic, "summary": None, "error": "not found"}
    r.raise_for_status()
    data = r.json()
    return {"topic": topic, "summary": data.get("extract")}

_ARITH_PATTERN = re.compile(r'^[0-9\.\s\+\-\*\/\(\)]+$')
def tool_calculator(expression: str) -> Dict[str, Any]:
    expr = (expression or "").strip()
    if not expr or not _ARITH_PATTERN.match(expr):
        return {"expression": expression, "error": "invalid expression"}
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        return {"expression": expr, "result": float(result)}
    except Exception as e:
        return {"expression": expression, "error": str(e)}

# ==== Helpers / Intent ====
def detect_cities(query: str) -> List[str]:
    q = (query or "").lower()
    found = []
    for name in CITY_COORDS:
        if name in q:
            found.append(name)
    # preserve order
    seen, ordered = set(), []
    for n in found:
        if n not in seen:
            ordered.append(n); seen.add(n)
    return ordered

def extract_numbers(query: str) -> List[float]:
    nums = re.findall(r'[-+]?(?:\d+\.\d+|\d+)', query)
    out = []
    for n in nums:
        try:
            out.append(float(n))
        except:
            pass
    return out

def is_weather_avg_intent(q: str) -> bool:
    ql = q.lower()
    city_count = len(detect_cities(q))
    return ("weather" in ql or "temperature" in ql or "average" in ql) and city_count >= 2

def is_wiki_intent(q: str) -> bool:
    ql = q.lower()
    return any(k in ql for k in ["who is", "who was", "what is", "tell me who", "tell me about", "wikipedia", "wiki"])

def extract_topic_for_wiki(q: str) -> str:
    # normalize common phrasings
    qq = re.sub(r"^tell me (who|about)\s+", "", q, flags=re.I).strip()
    m = re.search(r"(who\s+(is|was)\s+)(?P<t>.+?)([\,\?]|$)", qq, flags=re.I)
    if m:
        return m.group("t").strip()
    m = re.search(r"(what\s+is\s+)(?P<t>.+?)([\,\?]|$)", qq, flags=re.I)
    if m:
        return m.group("t").strip()
    # fallback: take leading Title-Case tokens
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-']+", qq) if w[0].isupper()]
    if words:
        return " ".join(words[:3])
    return qq

def find_years(q: str) -> List[int]:
    years = [int(y) for y in re.findall(r"\b(1[5-9]\d{2}|20\d{2})\b", q)]
    return years[:2]

def is_math_with_weather_intent(q: str) -> bool:
    return (len(extract_numbers(q)) >= 1) and (len(detect_cities(q)) == 1) and any(k in q.lower() for k in ["sum", "add", "plus", "+"])

def is_pure_calc_intent(q: str) -> bool:
    # if it looks like a math request without cities
    return (len(detect_cities(q)) == 0) and (len(extract_numbers(q)) >= 1) and any(k in q.lower() for k in ["sum", "add", "plus", "+", "-", "*", "/", "compute", "calculate"])

# ==== Narration ====
def narrate_final(context: Dict[str, Any]) -> str:
    prompt = (
        "Using ONLY the provided data, write a short, clear answer. "
        "Do not invent numbers or facts. Keep it to 2-5 sentences.\n"
        f"DATA: {json.dumps(context, ensure_ascii=False)}"
    )
    resp = _model.generate_content(prompt)
    return (resp.text or "").strip()

# ==== Controllers ====
def handle_weather_average(query: str) -> str:
    cities = detect_cities(query)
    temps: Dict[str, float] = {}
    print("")
    if len(cities) < 2:
        print('Planner: {"final": true, "answer": "Please include at least two cities for an average (e.g., Tokyo and London)."}')
        return "Please include at least two cities for an average (e.g., Tokyo and London)."

    for c in cities:
        decision = {"tool": "weather", "args": {"city": c}}
        print(f"Planner: {json.dumps(decision, ensure_ascii=False)}")
        obs = tool_weather(c)
        print(f"Observation: {json.dumps(obs, ensure_ascii=False)}")
        if "temp_now_c" in obs and isinstance(obs["temp_now_c"], (int, float)):
            temps[obs["city"]] = float(obs["temp_now_c"])

    if not temps:
        print('Planner: {"final": true, "answer": "No temperatures could be fetched. Try again."}')
        return "No temperatures could be fetched. Try again."

    expr = "(" + "+".join(str(v) for v in temps.values()) + f")/{len(temps)}"
    decision_calc = {"tool": "calculator", "args": {"expression": expr}}
    print(f"Planner: {json.dumps(decision_calc, ensure_ascii=False)}")
    obs_calc = tool_calculator(expr)
    print(f"Observation: {json.dumps(obs_calc, ensure_ascii=False)}")
    avg = obs_calc.get("result")

    context = {
        "task": "weather_average",
        "query": query,
        "temperatures_c": temps,
        "average_c": avg,
        "region_hint": "Tokyo is Asia; London is Europe; Sydney is Oceania."
    }
    final_text = narrate_final(context)
    print(f'Planner (final): {{"final": true, "answer": {json.dumps(final_text, ensure_ascii=False)}}}')
    return final_text

def handle_wiki_plus_calc(query: str) -> str:
    print("")
    topic = extract_topic_for_wiki(query)
    decision = {"tool": "wikipedia", "args": {"topic": topic}}
    print(f"Planner: {json.dumps(decision, ensure_ascii=False)}")
    obs_wiki = tool_wikipedia(topic)
    print(f"Observation: {json.dumps(obs_wiki, ensure_ascii=False)}")

    years = find_years(query)
    age = None
    if len(years) == 2:
        born, died = years[0], years[1]
        expr = f"{died}-{born}"
        decision_calc = {"tool": "calculator", "args": {"expression": expr}}
        print(f"Planner: {json.dumps(decision_calc, ensure_ascii=False)}")
        obs_calc = tool_calculator(expr)
        print(f"Observation: {json.dumps(obs_calc, ensure_ascii=False)}")
        age = obs_calc.get("result")

    context = {
        "task": "wiki_plus_calc",
        "query": query,
        "topic": topic,
        "summary": obs_wiki.get("summary"),
        "age_years": age,
        "years_detected": years
    }
    final_text = narrate_final(context)
    print(f'Planner (final): {{"final": true, "answer": {json.dumps(final_text, ensure_ascii=False)}}}')
    return final_text

def handle_math_with_weather(query: str) -> str:
    print("")
    cities = detect_cities(query)
    nums = extract_numbers(query)
    if len(cities) != 1 or len(nums) == 0:
        return "Please provide one city and at least one number (e.g., sum 23.45 and the temperature in Manila)."
    city = cities[0]

    # fetch weather
    decision = {"tool": "weather", "args": {"city": city}}
    print(f"Planner: {json.dumps(decision, ensure_ascii=False)}")
    obs = tool_weather(city)
    print(f"Observation: {json.dumps(obs, ensure_ascii=False)}")
    if "temp_now_c" not in obs or not isinstance(obs["temp_now_c"], (int, float)):
        print('Planner: {"final": true, "answer": "Could not fetch the temperature."}')
        return "Could not fetch the temperature."

    # build sum expression
    terms = nums + [float(obs["temp_now_c"])]
    expr = "+".join(str(t) for t in terms)
    decision_calc = {"tool": "calculator", "args": {"expression": expr}}
    print(f"Planner: {json.dumps(decision_calc, ensure_ascii=False)}")
    obs_calc = tool_calculator(expr)
    print(f"Observation: {json.dumps(obs_calc, ensure_ascii=False)}")

    context = {
        "task": "math_plus_weather",
        "query": query,
        "numbers": nums,
        "city": obs["city"],
        "city_temp_c": obs["temp_now_c"],
        "expression": expr,
        "sum_result": obs_calc.get("result")
    }
    final_text = narrate_final(context)
    print(f'Planner (final): {{"final": true, "answer": {json.dumps(final_text, ensure_ascii=False)}}}')
    return final_text

def handle_pure_calc(query: str) -> str:
    print("")
    nums = extract_numbers(query)
    if len(nums) >= 2 and any(k in query.lower() for k in ["sum", "add", "plus", "+"]):
        expr = "+".join(str(n) for n in nums)
    else:
        # attempt to extract a simple arithmetic expression from the text
        expr = "".join(ch for ch in query if ch in "0123456789.+-*/() ")
        expr = re.sub(r"\s+", "", expr)
        if not expr:
            return "Please provide a numeric expression (e.g., 12.5+8.75*2)."
    decision_calc = {"tool": "calculator", "args": {"expression": expr}}
    print(f"Planner: {json.dumps(decision_calc, ensure_ascii=False)}")
    obs_calc = tool_calculator(expr)
    print(f"Observation: {json.dumps(obs_calc, ensure_ascii=False)}")

    context = {
        "task": "pure_calc",
        "query": query,
        "expression": expr,
        "result": obs_calc.get("result")
    }
    final_text = narrate_final(context)
    print(f'Planner (final): {{"final": true, "answer": {json.dumps(final_text, ensure_ascii=False)}}}')
    return final_text

def run_query(query: str) -> str:
    if is_weather_avg_intent(query):
        return handle_weather_average(query)
    if is_wiki_intent(query):
        return handle_wiki_plus_calc(query)
    if is_math_with_weather_intent(query):
        return handle_math_with_weather(query)
    if is_pure_calc_intent(query):
        return handle_pure_calc(query)
    return "I can help with multi-city weather averages, Wikipedia + simple math, math + one city's temperature, and pure calculator. Try asking about those!"

def repl():
    print("Reason–Act–Observe Agent (STRICT JSON). Type 'quit' to exit.\n")
    while True:
        try:
            q = input("Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q or q.lower() in {"quit","exit"}:
            break
        try:
            answer = run_query(q)
            print(f"\n[Agent]: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    repl()
