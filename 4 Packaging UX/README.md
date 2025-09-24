# Module 4 – Packaging & UX (Integrated Walkthrough)

This module refactors the Reason–Act–Observe agent from Module 3 into a polished **command‑line application**.  
It adds configuration, caching, retries, and a better user experience (UX), making the agent ready for workshop demos or real use.

---

## 🧭 Architecture

```
CLI (app.py)
   └─> Agent Core (agent_core.py)
         ├─ uses LLM Client (llm_client.py)
         ├─ calls Tools (tools.py)
         └─ enforces JSON Reason–Act–Observe loop
Config (config.py) ──> environment variables
Cache (cache.py)  ───> memoize results
```

The flow is:
1. **User query** comes from CLI.  
2. **Agent Core** asks the LLM to decide: either call a tool or finalize.  
3. **Tools** run (weather, Wikipedia, calculator), return observations.  
4. Observations are fed back, loop repeats.  
5. Final answer is returned to the CLI, displayed in plain, pretty, or JSON format.

---

## 📂 File Guide

### `app.py`
- Entry point for the CLI.  
- Parses flags like `--pretty`, `--json`, `--verbose`, `--max-steps`.  
- Calls `agent_core.run()` and formats the output for users.  

### `agent_core.py`
- Implements the **RAO loop** with strict JSON responses.  
- Each step: send prompt → parse JSON → call tool → record observation → repeat.  
- Has a safeguard if the LLM outputs invalid JSON.  

### `llm_client.py`
- Abstracts away the model provider.  
- Defaults to **Gemini** (needs `GOOGLE_API_KEY`).  
- Can switch to **LM Studio** with `LLM_PROVIDER=LMSTUDIO`.  

### `tools.py`
- Provides 3 tools:  
  - **Weather** (Open‑Meteo API, no key).  
  - **Wikipedia** (REST API summary).  
  - **Calculator** (safe arithmetic).  
- Tools are retried on failure (Tenacity) and cached (cache.py).  

### `cache.py`
- JSON‑based cache with TTL (default 10 minutes).  
- Avoids hitting the same API repeatedly during a demo.  

### `config.py`
- Loads environment variables from `.env`.  
- Sets defaults: timeouts, cache file, maximum steps.  

---

## ▶️ Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy and edit `.env`:
```bash
cp .env.example .env
# add your GOOGLE_API_KEY
```

---

## ▶️ Running the Agent

Example 1 – Weather comparison:
```bash
python app.py "What's the weather in Tokyo and how does it compare to London?" --pretty
```

Example 2 – Wikipedia + calculator:
```bash
python app.py "Who is Jose Rizal? Also, compute 12.5 + 8.75." --verbose
```

Example 3 – Calculator only:
```bash
python app.py "What is (3.5 + 2.1) * 4?" --json
```

---

## 🔄 Example Loop (Tokyo vs. London weather)

1. Planner: `{ "tool": "weather", "args": {"city": "Tokyo"} }`  
   → Observation: `{ "city":"Tokyo","temp_now_c":27 }`  
2. Planner: `{ "tool": "weather", "args": {"city": "London"} }`  
   → Observation: `{ "city":"London","temp_now_c":20 }`  
3. Planner: `{ "tool": "calculator", "args": {"expression":"27-20"} }`  
   → Observation: `{ "result":7 }`  
4. Planner: `{ "final": true, "answer":"Tokyo is about 7°C warmer than London today." }`  

---

## 🛠️ Extending the Agent

- Add new tools (e.g., news, translation, finance).  
- Improve CLI flags (`--save-trace`, `--json-only`).  
- Support more providers (Ollama, Anthropic).  

---

## 🩹 Troubleshooting

- **`GOOGLE_API_KEY not set`** → edit `.env`.  
- **Network errors** → tools will retry; check your internet.  
- **Non‑JSON outputs** → re‑run; prompt enforces JSON, but fallback is in place.  

---

This module shows how to evolve a prototype agent into a **packaged, user‑friendly CLI tool** that’s robust enough for workshops and small projects.
