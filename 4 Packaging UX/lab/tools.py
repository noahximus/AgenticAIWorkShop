# Module 4 Tools (Patched)
# - weather: flexible args (city/location/city_name), Open-Meteo
# - wikipedia: adds proper User-Agent header
# - calculator: safe arithmetic
# - TOOL_REGISTRY map

import re
import requests
from typing import Dict, Any

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

def tool_weather(city: str = None, **kwargs) -> Dict[str, Any]:
    # Accept common aliases from the model
    if not city:
        city = kwargs.get("location") or kwargs.get("city_name")

    if not city:
        return {"error": "Missing 'city' argument for weather."}

    target = city.lower().strip()
    # naive fuzzy match
    chosen = None
    for name in CITY_COORDS:
        if name in target:
            chosen = name
            break
    if not chosen:
        return {"error": f"Unknown city '{city}'"}

    lat, lon = CITY_COORDS[chosen]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m"}

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        return {"error": f"weather request failed: {e}"}

    temps = data.get("hourly", {}).get("temperature_2m", [])
    now_c = temps[0] if temps else None
    return {"city": chosen.title(), "temp_now_c": now_c, "source": "Open-Meteo hourly temperature_2m"}

def tool_wikipedia(topic: str) -> Dict[str, Any]:
    topic = (topic or "").strip()
    if not topic:
        return {"topic": topic, "summary": None, "error": "empty topic"}
    title = topic.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    headers = {
        "User-Agent": "AgenticAIWorkshop/1.0 (https://example.com/; contact@example.com)"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code in (400, 404):
            return {"topic": topic, "summary": None, "error": "not found"}
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        return {"topic": topic, "summary": None, "error": f"wiki request failed: {e}"}
    return {"topic": topic, "summary": data.get("extract")}

_ARITH_PATTERN = re.compile(r'^[0-9\.\s\+\-\*\/\(\)]+$')
def tool_calculator(expression: str) -> Dict[str, Any]:
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