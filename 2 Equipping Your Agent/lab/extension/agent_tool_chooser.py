import os
import re
import requests
import google.generativeai as genai

# ==== Configure Gemini (uses Module 1 key) ====
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")
genai.configure(api_key=API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")

# ==== Simple city coordinate map for weather lookups ====
CITY_COORDS = {
    "manila": (14.5995, 120.9842),
    "tokyo": (35.6762, 139.6503),
    "singapore": (1.3521, 103.8198),
    "new york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "sydney": (-33.8688, 151.2093),
}

# ==== Tools ====

def get_weather_for(city_name: str):
    latlon = None
    # naive match: exact or substring
    for key, ll in CITY_COORDS.items():
        if key in city_name.lower():
            latlon = ll
            city_name = key.title()
            break
    if not latlon:
        # fallback: Manila
        city_name = "Manila"
        latlon = CITY_COORDS["manila"]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latlon[0],
        "longitude": latlon[1],
        "hourly": "temperature_2m",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    temps = data.get("hourly", {}).get("temperature_2m", [])
    temp_now = temps[0] if temps else None
    raw = {
        "city": city_name,
        "latlon": latlon,
        "temp_now_c": temp_now,
        "source": "Open-Meteo hourly temperature_2m"
    }
    return raw



def get_wikipedia_summaryNew(topic: str) -> str:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    headers = {
        "User-Agent": "AgenticAIWorkshop/1.0 (https://example.com/; contact@example.com)"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("extract", "No summary available.")

def get_wikipedia_summary(topic: str):
    # Use REST summary endpoint; it expects a page title
    # We'll try a direct title first; for spaces, replace with underscores
    title = topic.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    #r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
    r = requests.get(url, timeout=20, headers={
        "User-Agent": "AgenticAIWorkshop/1.0 (https://example.com/; contact@example.com)"
    })
    
    if r.status_code == 404 or r.status_code == 400:
        return {"topic": topic, "summary": None, "source": "Wikipedia REST summary"}
    r.raise_for_status()
    data = r.json()
    summary = data.get("extract")
    return {"topic": topic, "summary": summary, "source": "Wikipedia REST summary"}

# Optional: News tool (requires external API key). Example stub for NewsAPI:
# def get_news(topic: str):
#     import os
#     key = os.getenv("NEWSAPI_KEY")
#     if not key:
#         raise ValueError("Set NEWSAPI_KEY to use the news tool.")
#     url = "https://newsapi.org/v2/everything"
#     params = {"q": topic, "pageSize": 3, "apiKey": key, "language": "en", "sortBy": "relevancy"}
#     r = requests.get(url, params=params, timeout=20)
#     r.raise_for_status()
#     data = r.json()
#     headlines = [a.get("title") for a in data.get("articles", [])]
#     return {"topic": topic, "headlines": headlines, "source": "NewsAPI"}

# ==== Router ====

def route(query: str):
    q = query.lower().strip()
    if "weather" in q:
        # naive city extraction: last word if it's a known city, else default
        city = None
        for name in CITY_COORDS.keys():
            if name in q:
                city = name
                break
        if not city:
            # try to extract a trailing word
            m = re.search(r"weather in ([a-zA-Z\s\-]+)", q)
            city = m.group(1).strip() if m else "manila"
        raw = get_weather_for(city)
        prompt = f"""You are a friendly workshop agent.
Raw weather data: {raw}
Create a short, upbeat explanation of the current temperature in {raw['city']} (in °C), and include a practical suggestion (e.g., bring water/umbrella)."""
        resp = MODEL.generate_content(prompt)
        return {"tool": "weather", "raw": raw, "answer": resp.text}
    else:
        # default to Wikipedia
        # try a basic topic extraction (after 'about', 'who is', 'what is')
        topic = q
        for prefix in ["tell me about", "who is", "what is", "define", "explain"]:
            if q.startswith(prefix):
                topic = q[len(prefix):].strip(" ?")
                break
        raw = get_wikipedia_summary(topic.title())
        if not raw.get("summary"):
            answer = f"Sorry, I couldn't find a Wikipedia summary for '{topic}'. Try another topic."
            return {"tool": "wikipedia", "raw": raw, "answer": answer}
        prompt = f"""You are a friendly workshop agent.
Use the following Wikipedia summary to explain '{topic}' in 4-6 concise sentences for a beginner. Avoid jargon.
Summary: {raw['summary']}"""
        resp = MODEL.generate_content(prompt)
        return {"tool": "wikipedia", "raw": raw, "answer": resp.text}

def main():
    print("Agent Tool Chooser (type 'quit' to exit)")
    while True:
        try:
            q = input("\nYour question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not q or q.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        try:
            result = route(q)
            print(f"\n[Tool used]: {result['tool']}")
            print("[Raw snippet]:", result['raw'])
            print("\n[Agent]:", result['answer'])
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
