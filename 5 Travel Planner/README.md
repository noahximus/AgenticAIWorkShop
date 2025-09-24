# Module 5 – Travel Planner Agent (Capstone, with Walkthrough)

This module builds a **Travel Planner Agent** on top of Module 4’s agentic stack.  
It demonstrates how to combine multiple tools (weather, Wikipedia, distance, translation) in a loop to create a practical itinerary.

---

## 🧭 Architecture Overview

```
CLI (app_travel.py)
   └─> Agent Core (travel_agent_core.py)
         ├─ uses LLM Client (llm_client.py)
         ├─ calls Tools (travel_tools.py)
         └─ follows JSON Reason–Act–Observe loop
Config (config.py) ──> environment variables
Cache (cache.py)  ───> memoize results
```

The workflow:
1. User asks: *“Plan a 3-day trip to Manila in November with a modest budget”*  
2. Agent core sends a structured planning prompt to the LLM.  
3. LLM decides what tool to call first (e.g., weather or parse_meta).  
4. Tool runs, returns an observation.  
5. Observation is added to context, loop continues.  
6. Eventually, LLM outputs `{ "final": true, "answer": "..." }` with an itinerary.  
7. If `--translate` is set, final answer is translated.  

---

## 📂 Files and Walkthrough

### `app_travel.py` — CLI entry
- Parses command-line arguments:
  - `--pretty`: display answer in styled panel.  
  - `--json`: return JSON with answer + trace.  
  - `--verbose`: show step-by-step planning/observations.  
  - `--translate`: translate the final itinerary to a given language code (e.g., `tl`, `es`, `fr`).  
- Calls `run_travel(query, ...)` from `travel_agent_core.py`.

### `travel_agent_core.py` — Agent loop
- Defines a **system prompt** instructing the model to always return JSON.  
- Each loop iteration:
  - Sends context to the LLM.  
  - Parses JSON → either an **action** (`tool + args`) or a **final answer**.  
  - If action: calls the tool from `travel_tools.py`, appends observation.  
  - If final: stops and returns the plan (with optional translation).  
- Records every step in a trace list (used for `--verbose` or `--json`).  

### `travel_tools.py` — Travel-specific tools
- **Weather**: fetches temperature via Open-Meteo (no API key).  
- **Wikipedia**: fetches a short summary via REST API.  
- **Distance**: computes km between two known cities (haversine formula).  
- **Translate**: sends text to LibreTranslate (default `https://libretranslate.com`).  
- **Parse_meta**: extracts hints (days, budget) from the query text.  

### `llm_client.py`
- Supports **Gemini** (via `google-generativeai`) and **LM Studio** (OpenAI-compatible local server).  
- Controlled by `.env` and flags (`--provider GEMINI|LMSTUDIO`).  

### `config.py` and `cache.py`
- `config.py`: loads API keys and settings from `.env`.  
- `cache.py`: JSON-based TTL cache, prevents repeated identical requests.  

---

## ▶️ Running the Agent

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure `.env`:
```bash
cp .env.example .env
# add your GOOGLE_API_KEY or set LM Studio vars
```

3. Run examples:
```bash
# Manila 3-day plan, verbose trace
python app_travel.py "Plan a 3-day trip to Manila in November with a modest budget" --pretty --verbose

# Multi-city Tokyo + Kyoto
python app_travel.py "Plan 5 days across Tokyo and Kyoto in April; include must-eat food and top sights" --pretty

# Cebu weekend, translated to Filipino
python app_travel.py "Plan a weekend in Cebu for food and beaches" --translate tl --pretty
```

---

## 🔄 Example Flow

Query:
```
Plan 5 days across Tokyo and Kyoto in April; include must-eat food and top sights
```

Possible loop:
1. Planner → `{"tool":"parse_meta","args":{"query":"Plan 5 days..."}}`  
   - Observation: `{ "days": 5 }`  
2. Planner → `{"tool":"weather","args":{"city":"Tokyo"}}`  
   - Observation: `{ "city":"Tokyo","temp_now_c":17 }`  
3. Planner → `{"tool":"wikipedia","args":{"topic":"Tokyo"}}`  
   - Observation: `{ "summary":"Tokyo is Japan's capital..." }`  
4. Planner → `{"tool":"wikipedia","args":{"topic":"Kyoto"}}`  
   - Observation: `{ "summary":"Kyoto is known for shrines..." }`  
5. Planner → `{"tool":"distance","args":{"city_a":"Tokyo","city_b":"Kyoto"}}`  
   - Observation: `{ "km": 370.8 }`  
6. Planner → `{"final": true, "answer":"5-day plan with weather note, city highlights, must-eat ramen and matcha sweets, Kyoto temples..."}`  

---

## 🛠️ Extending the Planner

- Add more cities and coordinates to `CITY_COORDS`.  
- Add a `budget_recommendations` tool to suggest hotels/hostels.  
- Add `events` tool pulling festivals or seasonal highlights.  
- Refine `parse_meta` to better detect travel duration and budget.  

---

## 🩹 Troubleshooting

- **`GOOGLE_API_KEY not set`** → configure `.env`.  
- **Network errors** → the tools retry automatically. Check your connection.  
- **Non-JSON outputs** → rerun; the strict prompt usually keeps the model in JSON.  

---

This capstone module shows how small, focused tools can be composed into a loop to solve a complex, realistic task: **planning a multi-city trip**.
