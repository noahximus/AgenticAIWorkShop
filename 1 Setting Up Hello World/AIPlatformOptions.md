# AI Platform Options for the Agentic AI Workshop

Not everyone may want (or be able) to use the same AI provider.  
This guide provides several **options** (both free and paid) so you can follow along in the workshop.  
Choose **one option** below based on your preference and setup.

---

## 1. 🔑 OpenAI (Cloud)

**What it is:** Industry-leading models such as GPT-4o, GPT-4o-mini.  
**Free tier:** Sometimes new accounts get trial credits (e.g., $5), but not guaranteed. Credits usually expire within 3 months.  
**Why use it:** Most widely used, industry standard, supports advanced features.

### Setup
1. Sign up at [OpenAI Signup](https://platform.openai.com/signup)  
2. Verify email and phone.  
3. Log in to the [Dashboard](https://platform.openai.com/).  
4. Create an API key at [API Keys](https://platform.openai.com/account/api-keys).  
5. Set your API key in your system environment:  

   - **Windows (PowerShell):**
     ```powershell
     setx OPENAI_API_KEY "your_api_key_here"
     ```
     (Restart your terminal after running this.)  

   - **Mac/Linux (Terminal):**
     ```bash
     export OPENAI_API_KEY="your_api_key_here"
     ```
     (This only lasts for the session; to persist, add it to `~/.bashrc` or `~/.zshrc`.)  

6. Install the SDK:
   ```bash
   pip install openai
   ```

### Hello World Example (Python)
```python
import os
from openai import OpenAI

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

client = OpenAI(api_key=api_key)

# Simple "Hello World" demo
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hello world in a fun way!"}]
)

print("AI says:", response.choices[0].message.content)
```

---

## 2. 🚀 Ollama (Local – Mac/Linux, Windows Preview)

**What it is:** A local runner for open-source LLMs like Llama 3, Mistral, Gemma, Phi-3.  
**Why use it:** Runs completely free on your computer, no internet or API key required.

### Setup
1. Download Ollama: [https://ollama.com/download](https://ollama.com/download)  
2. Install and open your terminal.  
3. Run a model for the first time (e.g., Llama 3):
   ```bash
   ollama run llama3
   ```

### Hello World Example (Python)
```python
import subprocess

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

print(ask_ollama("Say hello world in a fun way!"))
```

---

## 3. 🖥 LM Studio (Mac & Windows)

**What it is:** A desktop app with a GUI to run models locally.  
**Why use it:** Beginner-friendly, lets you “see” and interact with models easily.

### Setup
1. Download LM Studio: [https://lmstudio.ai/](https://lmstudio.ai/)  
2. Install and open the app.  
3. Choose a model (e.g., Mistral or Llama 3) and download it.  
4. Optionally enable **local server mode** (LM Studio provides an OpenAI-compatible API).

### Hello World Example (Python, using server mode)
```python
import openai

client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

response = client.chat.completions.create(
    model="mistral",
    messages=[{"role": "user", "content": "Say hello world in a fun way!"}]
)

print("AI says:", response.choices[0].message.content)
```

---

## 4. 🤗 Hugging Face Inference API (Cloud)

**What it is:** Cloud-hosted models via Hugging Face.  
**Free tier:** 30,000 input tokens/month.  
**Why use it:** Quick access to many open-source models without heavy installs.

### Setup
1. Create a free account: [https://huggingface.co/join](https://huggingface.co/join)  
2. Get your API token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
3. Install Hugging Face client:
   ```bash
   pip install huggingface_hub
   ```

### Hello World Example (Python)
```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2")

response = client.text_generation("Say hello world in a fun way!")
print(response)
```

---

## 5. 🌐 Google Gemini API (Cloud)

**What it is:** Google’s Gemini models (like Gemini 1.5 Flash).  
**Free tier:** 1,500 requests/day, 15 requests/minute.  
**Why use it:** Reliable free access to high-quality models.

### Setup
1. Sign up at [Google AI Studio](https://aistudio.google.com/)  
2. Generate an API key.  
3. Install Google Generative AI SDK:
   ```bash
   pip install google-generativeai
   ```

### Hello World Example (Python)
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello world in a fun way!")

print(response.text)
```

---

# ⚖️ Comparison Table

| Platform          | Free Tier              | Setup Effort | Offline? | Best For |
|-------------------|------------------------|--------------|----------|----------|
| **OpenAI**        | Trial credits (not guaranteed) | Easy | ❌ | Industry-standard |
| **Ollama**        | Unlimited (local)      | Easy         | ✅ | Offline/local demos |
| **LM Studio**     | Unlimited (local)      | Easy (GUI)   | ✅ | Beginners, visual learners |
| **Hugging Face**  | 30k tokens/month       | Medium       | ❌ | Cloud API demo |
| **Google Gemini** | 1,500 requests/day     | Medium       | ❌ | Free cloud access |

---

✅ Choose whichever path works best for you.  
If you’re worried about cost, start with **Ollama (local)** or **Google Gemini (free API)**.  
