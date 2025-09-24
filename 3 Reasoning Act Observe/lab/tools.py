import re
import requests

CITY_COORDS = {
    "manila": (14.5995, 120.9842),
    "tokyo": (35.6762, 139.6503),
    "singapore": (1.3521, 103.8198),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "sydney": (-33.8688, 151.2093),
}

def tool_weather(city: str):
    target = city.lower().strip() if city else "manila"
    chosen = None
    for name in CITY_COORDS.keys():
        if name in target:
            chosen = name
            break
    if not chosen:
        chosen = "manila"
    lat, lon = CITY_COORDS[chosen]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m"}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    temps = data.get("hourly", {}).get("temperature_2m", [])
    now_c = temps[0] if temps else None
    return {"city": chosen.title(), "temp_now_c": now_c, "source": "Open-Meteo hourly temperature_2m"}

def tool_wikipedia(topic: str):
    if not topic:
        return {"topic": topic, "summary": None, "error": "empty topic"}
    title = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
    if r.status_code in (400, 404):
        return {"topic": topic, "summary": None, "error": "not found"}
    r.raise_for_status()
    data = r.json()
    return {"topic": topic, "summary": data.get("extract")}

_ARITH_PATTERN = re.compile(r'^[0-9\.\s\+\-\*\/\(\)]+$')

def tool_calculator(expression: str):
    expr = (expression or "").strip()
    if not expr or not _ARITH_PATTERN.match(expr):
        return {"expression": expression, "error": "invalid expression"}
    try:
        result = eval(expr, {"__builtins__": {}}, {})
        if isinstance(result, (int, float)):
            return {"expression": expr, "result": float(result)}
        return {"expression": expr, "error": "non-numeric result"}
    except Exception as e:
        return {"expression": expression, "error": str(e)}

TOOL_REGISTRY = {
    "weather": {"fn": tool_weather, "args": {"city": "str"}},
    "wikipedia": {"fn": tool_wikipedia, "args": {"topic": "str"}},
    "calculator": {"fn": tool_calculator, "args": {"expression": "str"}},
}
