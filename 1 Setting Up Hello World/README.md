# Module 1 – Setup Guide & Hello World

Welcome to the **Agentic AI Workshop**! 🎉  
This README will guide you through installing the required tools, creating your Google AI account, setting up your environment, and running your first **Hello World AI script** with **Google Gemini**.

---

## 🔧 Tools You Need
- **Python 3.10+**
- **pip** (comes with Python, used to install packages)
- **Visual Studio Code (VS Code)** – [Download here](https://code.visualstudio.com/Download)
- **Google Generative AI SDK** (installed via pip)
- **Google AI Studio Account** (to generate your API key)

---

## 📝 Create a Google AI Studio Account

1. Go to [Google AI Studio](https://aistudio.google.com/)  
2. Sign up or log in with your Google account.  
3. Generate an API key from the dashboard.  
4. Copy the key and keep it safe.

⚠️ Free Tier: Google Gemini provides **1,500 requests/day** and **15 requests/minute** on the free plan. Perfect for workshops!

---

## 🪟 Windows Setup

1. **Install Python**
   - Download from [python.org](https://www.python.org/downloads/)
   - Choose **Python 3.11 or 3.12 (64-bit)**
   - Run installer → **Check 'Add Python to PATH'** → Install Now
   - Verify installation:
     ```powershell
     python --version
     pip --version
     ```

2. **Install VS Code**
   - Download from [VS Code](https://code.visualstudio.com/Download)
   - Install and check “Add to PATH”
   - Open terminal inside VS Code with **Ctrl+`**

3. **Install Google Generative AI SDK**
   ```powershell
   pip install google-generativeai
   ```

4. **Set API Key**
   ```powershell
   setx GOOGLE_API_KEY "your_api_key_here"
   ```

---

## 🍏 Mac Setup

1. **Install Homebrew (recommended)**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew --version
   ```

2. **Install Python**
   - Option A: [Download installer](https://www.python.org/downloads/)
   - Option B (preferred):
     ```bash
     brew install python
     ```
   - Verify installation:
     ```bash
     python3 --version
     pip3 --version
     ```

3. **Install VS Code**
   - Download from [VS Code](https://code.visualstudio.com/Download)
   - Open `.dmg` and drag **Visual Studio Code** to Applications
   - Open terminal in VS Code with **Ctrl+`** (or ⌃ + `)

4. **Install Google Generative AI SDK**
   ```bash
   pip3 install google-generativeai
   ```

5. **Set API Key**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

---

## 🐍 Hello World Script (Google Gemini)

Save this as **hello_world_ai.py**:

```python
import os
import google.generativeai as genai

# Get API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set!")

genai.configure(api_key=api_key)

# Simple "Hello World" demo with Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello world in a fun way!")

print("AI says:", response.text)
```

Run it with:
```bash
python hello_world_ai.py
```

---

## 📦 Requirements

Create a `requirements.txt` with:
```txt
google-generativeai>=0.5.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🛠 Troubleshooting

Here are some common issues you may encounter:

### 1. `ModuleNotFoundError: No module named 'google'`
- Cause: The SDK is not installed.  
- Fix:
  ```bash
  pip install google-generativeai
  ```

### 2. `ValueError: GOOGLE_API_KEY environment variable not set!`
- Cause: API key not configured.  
- Fix:
  - Ensure you generated a key from [Google AI Studio](https://aistudio.google.com/).  
  - Set it again using `setx` (Windows) or `export` (Mac/Linux).  

### 3. Rate limits exceeded
- Cause: More than 1,500 requests/day or 15 requests/minute.  
- Fix: Wait until the limit resets or upgrade your Google AI plan.

---

## ✅ Lab 1 Recap

At this point, you should have:
- Python installed and working
- VS Code ready as your editor
- Google AI Studio account created and API key set
- Google Generative AI SDK installed
- Your **first AI-powered script running with Gemini!** 🎉

You're now ready to dive into building Agentic AI applications 🚀

