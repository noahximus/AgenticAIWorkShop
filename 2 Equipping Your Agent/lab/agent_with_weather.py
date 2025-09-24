import os
import requests
import google.generativeai as genai

# Read API key for Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_weather(lat=14.5995, lon=120.9842):
    """Fetch hourly temperature for Manila using Open-Meteo (no API key required)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m"
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def main():
    data = get_weather()
    temps = data.get("hourly", {}).get("temperature_2m", [])
    if not temps:
        print("Could not find temperature data in response.")
        return
    temp_now = temps[0]
    prompt = f"The temperature in Manila right now is {temp_now}°C. Describe this in a fun, friendly way for a workshop participant."
    resp = model.generate_content(prompt)
    print("AI Agent says:", resp.text)

if __name__ == "__main__":
    main()
