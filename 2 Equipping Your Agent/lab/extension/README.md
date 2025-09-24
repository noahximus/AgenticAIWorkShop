# Module 2 – Extensions (Optional): Tool‑Choosing Agent

This extension builds a tiny **agent** that picks a **tool** based on the user's query:
- If the query mentions **weather** → call the **Open‑Meteo** API.
- Otherwise → fetch a **Wikipedia summary** for the topic.
- Then ask **Google Gemini** to explain the result in a friendly way.

No additional API keys are required (beyond your Gemini key from Module 1).

---

## 📦 Install
```bash
pip install -r requirements.txt
```

---

## ▶️ Run
```bash
python agent_tool_chooser.py
```
Then type a query, e.g.:
- `What's the weather in Tokyo?`
- `Tell me about Mount Mayon`
- `Who is Jose Rizal?`

---

## 🧠 How It Works
1. **Intent detection (very simple):** looks for the word “weather” in the input.
2. **Weather tool:** calls Open‑Meteo (no key) using coordinates from a tiny built‑in city map.
3. **Wiki tool:** calls Wikipedia’s REST API (no key) to get a plain summary.
4. **LLM explain:** sends the raw data to **Gemini** to produce a concise, friendly answer.
5. **Output:** prints both the raw snippet and the LLM’s explanation.

---

## 🗺️ Adding Cities
Add your city and coordinates inside `CITY_COORDS` in the script.

---

## 💡 Optional: Add a News Tool
If you want a third tool:
- Create a free key at https://newsapi.org/ (or another news provider).
- Add `NEWSAPI_KEY` to your environment.
- Write a `get_news(topic)` function and route queries containing “news” to it.

A stub is provided in comments inside the script.

---

## 🛠 Troubleshooting
- `ValueError: GOOGLE_API_KEY environment variable not set!` → set it again and restart your terminal.
- Network errors → ensure you can reach `https://api.open-meteo.com` and `https://en.wikipedia.org`.
- Empty Wikipedia results → try a different search term.

Enjoy! 🚀
