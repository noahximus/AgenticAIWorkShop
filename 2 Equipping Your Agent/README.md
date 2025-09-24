# Module 2 – Equipping Your Agent (30 mins)

**Goal:** Connect your LLM to an external tool (a public API) so your agent can fetch real data, then explain it.

We’ll use **Google Gemini** (from Module 1) and the **Open‑Meteo Weather API** (no API key needed).

---

## ✅ What You’ll Build
- A Python script that fetches **Manila’s weather** (temperature) using HTTP.
- Sends the result to Gemini and prints a **fun explanation**.

---

## 🧰 Prerequisites
- Completed Module 1 (Python + VS Code + `GOOGLE_API_KEY` set).
- Internet access.

---

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` – Google Gemini SDK
- `requests` – for calling web APIs

---

## 🧪 Run the Lab
```bash
python agent_with_weather.py
```

**Expected:** The script prints a friendly summary like “It’s X°C in Manila…” with a fun twist from Gemini.

---

## 🧠 How It Works
1. `requests` calls **Open‑Meteo** with Manila coordinates.  
2. We parse the first hourly temperature value.  
3. We prompt **Gemini** to explain it in plain language.

---

## 🛠 Troubleshooting
- **`ValueError: GOOGLE_API_KEY environment variable not set!`**  
  Set your key again:  
  - Windows (PowerShell): `setx GOOGLE_API_KEY "your_api_key"` then restart terminal  
  - macOS/Linux: `export GOOGLE_API_KEY="your_api_key"`

- **`ModuleNotFoundError`**  
  Install dependencies: `pip install -r requirements.txt`

- **HTTP/network errors**  
  Ensure you have internet access and can open https://api.open-meteo.com/

---

## 🧗 Extensions (Optional)
- Add a **news** tool (e.g., use a free news API or Wikipedia).  
- Condition on user query: if it contains “weather” → call weather tool; if “news” → call news tool.  
- Print both raw data & Gemini’s explanation.

Happy building! 🚀
