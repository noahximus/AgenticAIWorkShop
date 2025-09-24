# 🎮 README for `planner_agent.py`

## Module 3 – Reasoning & Acting Loop (Core Agent)

Welcome to the **Agent Brain Gym** 🧠💪!  
Here we teach our AI how to **think, pick a tool, try it out, see what happens, and repeat** — just like a curious human solving a puzzle.

---

## 🗺️ Big Picture
The cycle looks like this:

```
User (you) → Planner (Gemini) → Tool (weather/wiki/calculator)
       ↑                                      ↓
       ←----------- Observation --------------
```

Think of it like a detective:
- 🕵️ **Planner** = decides which clue to follow.  
- 🔧 **Tools** = magnifying glass (weather), history book (Wikipedia), calculator (math).  
- 👀 **Observation** = what the detective sees after checking.  
- 📝 **Final Answer** = the detective’s conclusion.

---

## 🔧 What’s Inside
- `planner_agent.py` – the detective’s brain.  
- `tools.py` – the detective’s gadgets.  
- `requirements.txt` – stuff to install.  

---

## 🚀 Run It
1. Install:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your Gemini key:
   ```bash
   export GOOGLE_API_KEY="your_api_key"
   ```
3. Play:
   ```bash
   python planner_agent.py
   ```
   Try:
   - `What's the weather in Tokyo tomorrow?`
   - `Who is Jose Rizal?`
   - `What is 12.5 + 8.75?`

---

## 🤖 JSON Speak
The planner only speaks **JSON** (like robot language). Example:
```json
{"tool": "wikipedia", "args": {"topic": "Jose Rizal"}}
```
or:
```json
{"final": true, "answer": "Jose Rizal was a Filipino nationalist..."}
```

Observations back from tools also come in JSON — so the planner always has structured info to think with.

---

## 🧠 Why This is Cool
- You’re watching an LLM *think step by step*.  
- It feels alive: reason → act → observe → repeat.  
- You can peek into the JSON and see the **inner thoughts** of the AI.

---

## 🎯 Challenge
- Add your own tool (e.g., Joke tool).  
- Teach the planner to handle missing info (like “What’s the weather?” → it should ask *where*).  
- Try swapping Gemini for LM Studio or Ollama.
