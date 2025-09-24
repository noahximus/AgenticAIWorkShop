import re
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from cache import JsonCache
from config import CACHE_FILE, CACHE_TTL_SEC, HTTP_TIMEOUT, NEWSAPI_KEY, TRANSLATE_BASE_URL

cache = JsonCache(CACHE_FILE, ttl_sec=CACHE_TTL_SEC)

CITY_COORDS = {
    "manila": (14.5995, 120.9842),
    "tokyo": (35.6762, 139.6503),
    "singapore": (1.3521, 103.8198),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "sydney": (-33.8688, 151.2093),
}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def _http_get(url, params=None, headers=None):
    return requests.get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def _http_post(url, json_data=None, headers=None):
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

def tool_news(topic: str, page_size: int = 3):
    if not NEWSAPI_KEY:
        return {"topic": topic, "error": "NEWSAPI_KEY not set (get one at https://newsapi.org/)"} 
    url = "https://newsapi.org/v2/everything"
    params = {"q": topic or "technology", "pageSize": page_size, "apiKey": NEWSAPI_KEY, "language": "en", "sortBy": "relevancy"}
    r = _http_get(url, params=params)
    r.raise_for_status()
    data = r.json()
    headlines = [a.get("title") for a in data.get("articles", []) if a.get("title")]
    if not headlines:
        return {"topic": topic, "headlines": [], "note": "no headlines found"}
    return {"topic": topic, "headlines": headlines, "source": "NewsAPI"}

def tool_translate(text: str, target_lang: str):
    base = TRANSLATE_BASE_URL.rstrip("/")
    url = f"{base}/translate"
    # LibreTranslate expects: q, source, target, format
    # We'll let server auto-detect source by passing 'auto'
    payload = {"q": text or "", "source": "auto", "target": (target_lang or "en"), "format": "text"}
    r = _http_post(url, json_data=payload, headers={"Accept": "application/json"})
    r.raise_for_status()
    data = r.json()
    translated = data.get("translatedText")
    return {"text": text, "target_lang": target_lang, "translated": translated, "source": "LibreTranslate-compatible"}

TOOL_REGISTRY = {
    "weather": {"fn": tool_weather, "args": {"city": "str"}},
    "wikipedia": {"fn": tool_wikipedia, "args": {"topic": "str"}},
    "calculator": {"fn": tool_calculator, "args": {"expression": "str"}},
    "news": {"fn": tool_news, "args": {"topic": "str"}},
    "translate": {"fn": tool_translate, "args": {"text": "str", "target_lang": "str"}},
}
