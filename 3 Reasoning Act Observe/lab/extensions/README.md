# 📰 README for `planner_agent_ext.py`

## Module 3 – Extensions (Supercharged Agent)

Now we take our detective and give them **superpowers** 🦸:
- 📰 **Reads the news** (NewsAPI).  
- 🧠 **Remembers past queries** (memory.json).  
- 🔌 **Can swap brains** (Gemini by default, LM Studio if you prefer local).

---

## 🗺️ Big Picture
```
You → Planner → Tools (weather/wiki/calculator/news) → Memory
                                   ↑
                             Can recall last city/topic
```

It’s like playing an RPG:
- Planner = Dungeon Master  
- Tools = spells in your spellbook  
- Memory = the adventurer’s notebook  
- You = the player giving quests  

---

## 🧩 What’s New
- **News Tool** → fetches live headlines.  
- **Memory** → remembers last city/topic so you can say “What’s the weather today?” and it knows you meant Tokyo.  
- **Pluggable Brain** → use Gemini 🌩️ or LM Studio 🖥️ by flipping an environment variable.

---

## 🚀 Run It
1. Install:
   ```bash
   pip install -r requirements.txt
   ```
2. Env vars:
   ```bash
   export GOOGLE_API_KEY="your_gemini_key"
   export NEWSAPI_KEY="your_newsapi_key"   # if you want news
   export LLM_PROVIDER=LMSTUDIO            # optional brain swap
   ```
3. Play:
   ```bash
   python planner_agent_ext.py
   ```
   Try:
   - `news about AI safety`
   - `weather in Tokyo`
   - `Tell me about Mount Mayon`
   - `What is 12.5 + 8.75?`

---

## 🧠 JSON Flow
Planner → JSON instruction:
```json
{"tool": "news", "args": {"topic": "AI safety"}}
```

Tool → Observation:
```json
{"topic": "AI safety", "headlines": ["...", "..."]}
```

Planner → Final Answer:
```json
{"final": true, "answer": "AI safety is a hot topic, with headlines about ..."}
```

---

## 📝 Memory Example
After:
```
What's the weather in Tokyo?
```
Memory saves:
```json
{"last_city": "tokyo"}
```
Next time you just ask:
```
What's the weather today?
```
The agent remembers → Tokyo.

---

## 🎯 Why This is Cool
- Agents now **combine tools and memory** → feels more human.  
- You can **hot-swap the brain** → cloud or local.  
- Easy to extend: add Spotify, NASA, or your own APIs.

---

## 🔧 Challenges
- Add a Translate Tool.  
- Save multiple memories (last 3 cities).  
- Teach it to chain tools (e.g., weather + calculator to compute average temps).  
