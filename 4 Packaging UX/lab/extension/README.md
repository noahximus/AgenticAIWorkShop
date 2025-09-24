# Module 4 – Extensions (Solution)

This package extends the Module 4 CLI agent with:
- **News tool** (NewsAPI; requires `NEWSAPI_KEY`)
- **Translate tool** (LibreTranslate-compatible; no key needed for public instances)
- **`--json` output** (machine‑readable result)
- **`--verbose` loop logs** (show planner JSON + observations per step)
- **Transcript saving** (`--transcript run.jsonl`) with per‑step records
- Keeps **Gemini** (default) and **LM Studio** (optional) providers

> Start from Module 4. Drop these files into a new folder or alongside Module 4 and run as shown below.

---

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY; optionally add NEWSAPI_KEY
```

Examples:
```bash
# Weather vs. comparison (pretty output)
python app_ext.py "What's the weather in Tokyo and how does it compare to London?" --pretty --verbose

# News + JSON output
python app_ext.py "news about AI safety" --json

# Translate (English -> Filipino)
python app_ext.py "translate: Hello world -> tl" --pretty
```

---

## What’s New

- **Tools** (`tools_ext.py`):
  - `news(topic)` – NewsAPI.org headlines (3 by default). Requires `NEWSAPI_KEY`.
  - `translate(text, target_lang)` – calls LibreTranslate API; default base URL from `.env`.
- **Agent core** (`agent_core_ext.py`):
  - Returns both **final string** and **trace** (steps) to support `--json`.
  - Writes **transcripts** in JSONL with `--transcript file.jsonl`.
  - `--verbose` pretty‑prints each step.
- **CLI** (`app_ext.py`):
  - Adds `--json`, `--verbose`, `--transcript` flags.
  - Supports provider override like Module 4 (`--provider GEMINI|LMSTUDIO`).

---

## Environment

Copy and edit `.env.example`:
```env
GOOGLE_API_KEY=your_gemini_key

# Optional NewsAPI (https://newsapi.org/)
NEWSAPI_KEY=your_newsapi_key

# LibreTranslate public instance (or self-hosted)
TRANSLATE_BASE_URL=https://libretranslate.com

# Optional LM Studio
# LLM_PROVIDER=LMSTUDIO
# LMSTUDIO_MODEL=local-model
# LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

---

## Prompts that exercise the extensions

- `news about AI safety`
- `translate: Good morning, how are you? -> tl`
- `Who is Jose Rizal? Then translate the summary to es.`
- `Compare today’s temperature in Tokyo and London and translate the result to fr.`

---

## Files

- `app_ext.py` – CLI with `--json`, `--verbose`, `--transcript`
- `agent_core_ext.py` – RAO loop returning result + trace
- `tools_ext.py` – weather, wikipedia, calculator, **news**, **translate**
- `llm_client.py`, `config.py`, `cache.py` – shared infra
- `requirements.txt`, `.env.example`
