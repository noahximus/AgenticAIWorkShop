import math
import re
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from cache import JsonCache
from config import CACHE_FILE, CACHE_TTL_SEC, HTTP_TIMEOUT, TRANSLATE_BASE_URL

cache = JsonCache(CACHE_FILE, ttl_sec=CACHE_TTL_SEC)

# Approximate coordinates for a starter set
CITY_COORDS = {
    "manila": (14.5995, 120.9842),
    "cebu": (10.3157, 123.8854),
    "baguio": (16.4023, 120.5960),
    "tokyo": (35.6762, 139.6503),
    "kyoto": (35.0116, 135.7681),
    "osaka": (34.6937, 135.5023),
    "singapore": (1.3521, 103.8198),
    "london": (51.5074, -0.1278),
    "paris": (48.8566, 2.3522),
    "new york": (40.7128, -74.0060),
    "sydney": (-33.8688, 151.2093),
}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def _http_get(url, params=None, headers=None):
    from config import HTTP_TIMEOUT
    return requests.get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def _http_post(url, json_data=None, headers=None):
    from config import HTTP_TIMEOUT
    return requests.post(url, json=json_data, headers=headers, timeout=HTTP_TIMEOUT)

def tool_weather(city: str):
    target = (city or "manila").lower().strip()
    chosen = None
    for name in CITY_COORDS:
        if name in target:
            chosen = name
            break
    if not chosen:
        chosen = "manila"
    lat, lon = CITY_COORDS[chosen]
    cache_key = f"weather:{chosen}"
    cached = cache.get(cache_key)
    if cached:
        return {"city": chosen.title(), **cached, "cached": True}
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "hourly": "temperature_2m"}
    r = _http_get(url, params=params)
    r.raise_for_status()
    data = r.json()
    temps = data.get("hourly", {}).get("temperature_2m", [])
    now_c = temps[0] if temps else None
    value = {"temp_now_c": now_c, "source": "Open-Meteo hourly temperature_2m"}
    cache.set(cache_key, value)
    return {"city": chosen.title(), **value, "cached": False}

def tool_wikipedia(topic: str):
    topic = (topic or "").strip()
    if not topic:
        return {"topic": topic, "summary": None, "error": "empty topic"}
    title = topic.replace(" ", "_")
    cache_key = f"wiki:{title.lower()}"
    cached = cache.get(cache_key)
    if cached:
        return {"topic": topic, **cached, "cached": True}
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    r = _http_get(url, headers={"Accept": "application/json"})
    if r.status_code in (400, 404):
        return {"topic": topic, "summary": None, "error": "not found"}
    r.raise_for_status()
    data = r.json()
    value = {"summary": data.get("extract")}
    cache.set(cache_key, value)
    return {"topic": topic, **value, "cached": False}

def haversine_km(a, b):
    R = 6371.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def tool_distance(city_a: str, city_b: str):
    a = CITY_COORDS.get((city_a or "").lower())
    b = CITY_COORDS.get((city_b or "").lower())
    if not a or not b:
        return {"from": city_a, "to": city_b, "error": "unknown city (update CITY_COORDS)"}
    km = round(haversine_km(a, b), 1)
    return {"from": city_a.title(), "to": city_b.title(), "km": km}

def tool_translate(text: str, target_lang: str):
    base = TRANSLATE_BASE_URL.rstrip("/")
    url = f"{base}/translate"
    payload = {"q": text or "", "source": "auto", "target": (target_lang or "en"), "format": "text"}
    r = _http_post(url, json_data=payload, headers={"Accept": "application/json"})
    r.raise_for_status()
    data = r.json()
    translated = data.get("translatedText")
    return {"text": text, "target_lang": target_lang, "translated": translated, "source": "LibreTranslate-compatible"}

def parse_days_and_budget(query: str):
    q = (query or "").lower()
    days = None
    budget = None
    # days: look for "3-day", "5 days", "weekend"
    m = re.search(r"(\d+)\s*-?\s*day", q)
    if m:
        try:
            days = int(m.group(1))
        except:
            pass
    if "weekend" in q and not days:
        days = 2
    # budget
    if any(k in q for k in ["tight budget", "modest budget", "budget trip", "budget-friendly", "cheap"]):
        budget = "budget"
    elif any(k in q for k in ["mid", "moderate"]):
        budget = "mid"
    elif any(k in q for k in ["luxury", "splurge", "high-end", "5-star"]):
        budget = "luxury"
    return {"days": days, "budget": budget}

TOOL_REGISTRY = {
    "weather": {"fn": tool_weather, "args": {"city": "str"}},
    "wikipedia": {"fn": tool_wikipedia, "args": {"topic": "str"}},
    "distance": {"fn": tool_distance, "args": {"city_a": "str", "city_b": "str"}},
    "translate": {"fn": tool_translate, "args": {"text": "str", "target_lang": "str"}},
    "parse_meta": {"fn": parse_days_and_budget, "args": {"query": "str"}},  # helper, no external calls
}
