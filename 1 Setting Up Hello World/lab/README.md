# AI Hello Starters – Multi-Provider Quick Start

This bundle includes **five** self-contained “Hello, World!” starters so participants can choose any AI platform for the workshop.

## 📦 What’s Inside

- **openai_hello/** — OpenAI SDK (uses `OPENAI_API_KEY`)
- **gemini_hello/** — Google Gemini (uses `GOOGLE_API_KEY`)
- **huggingface_hello/** — Hugging Face Inference API (uses `HUGGINGFACE_API_KEY`)
- **lmstudio_hello/** — LM Studio local server (OpenAI-compatible, no cloud key)
- **ollama_hello/** — Ollama local model runner (no Python deps, no cloud key)

Each folder contains:
- `hello_world_ai.py` — minimal runnable example
- `requirements.txt` — exact dependencies
- `README.md` — setup & run steps

---

## 🚀 Quick Start (Pick One Path)

### 1) OpenAI (cloud)
- Set: `OPENAI_API_KEY`
- Install: `pip install -r openai_hello/requirements.txt`
- Run: `python openai_hello/hello_world_ai.py`

### 2) Google Gemini (cloud)
- Set: `GOOGLE_API_KEY`
- Install: `pip install -r gemini_hello/requirements.txt`
- Run: `python gemini_hello/hello_world_ai.py`

### 3) Hugging Face Inference API (cloud)
- Set: `HUGGINGFACE_API_KEY`
- Install: `pip install -r huggingface_hello/requirements.txt`
- Run: `python huggingface_hello/hello_world_ai.py`

### 4) LM Studio (local)
- In LM Studio: download a chat model → enable **Local Server** (http://localhost:1234/v1)
- Install: `pip install -r lmstudio_hello/requirements.txt`
- Run: `python lmstudio_hello/hello_world_ai.py`

### 5) Ollama (local)
- Install Ollama → `ollama run llama3` (first-time model pull)
- No Python deps required
- Run: `python ollama_hello/hello_world_ai.py`

---

## 🆓 Free vs Local Considerations

| Platform | Needs Internet? | Free Tier | Notes |
|---------|------------------|----------|------|
| OpenAI | ✅ | Trial credits (not guaranteed) | Industry standard SDK & models |
| Google Gemini | ✅ | ~1,500 req/day | Great free quota for workshops |
| Hugging Face | ✅ | ~30k input tokens/mo | Many models, simple client |
| LM Studio | ❌ (after download) | Local | OpenAI-compatible local server |
| Ollama | ❌ (after install) | Local | Fast CLI, very simple to script |

> Tip: If budget or network is a concern, start with **Ollama** or **LM Studio**.

---

## 🔑 Environment Variable Names (cloud options)

- OpenAI → `OPENAI_API_KEY`
- Google Gemini → `GOOGLE_API_KEY`
- Hugging Face → `HUGGINGFACE_API_KEY`

On Windows (PowerShell):
```powershell
setx NAME "value"
# restart terminal after setting
```

On macOS/Linux (bash/zsh):
```bash
export NAME="value"
# add to ~/.bashrc or ~/.zshrc to persist
```

---

## ❗ Troubleshooting

- `ModuleNotFoundError` → Install requirements from the correct folder.
- “API key not set” → Export the right env var name for your chosen path.
- LM Studio connection errors → Verify **Local Server** is enabled and the model is running.
- Ollama errors → Run `ollama run llama3` once to pull the model locally, then re-run the script.

Happy hacking! ✨
