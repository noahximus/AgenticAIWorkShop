# Agentic AI Workshop – Main README

Welcome to the **Agentic AI Workshop** 🎉  
In this hands-on program, you’ll learn step by step how to build **agents** powered by Large Language Models (LLMs) that can **reason, take actions, and adapt** to achieve goals.

This document introduces the workshop, explains **what Agentic AI is**, walks through the **concepts and terminologies** you need to know, and gives you a roadmap of the **six modules** that make up this training.

---

## 🤖 What is Agentic AI?

Traditional LLMs (like GPT or Gemini) generate text responses to a prompt, but they are passive: they don’t take initiative or interact with tools.  

**Agentic AI** takes the next step by turning an LLM into an **agent** that can:
- **Reason** about what needs to be done.  
- **Act** by calling external tools (APIs, functions, calculators, databases).  
- **Observe** the results of actions.  
- **Loop** this cycle until a final solution is reached.  

This pattern is called the **Reason–Act–Observe (RAO) loop**, and it’s at the heart of most agent frameworks (LangChain, AutoGPT, etc.).

---

## 🗝️ Key Concepts and Terminologies

Here are the essential ideas you’ll encounter and practice:

1. **LLM (Large Language Model)**  
   The engine that generates text. Examples: OpenAI GPT, Google Gemini, Anthropic Claude.  
   *Used in Module 1 for Hello World, and in every module afterward.*

2. **Agent**  
   A structured wrapper around the LLM that enforces goal-directed behavior.  
   *Introduced in Module 2, expanded in Modules 3–5.*

3. **Tools / Actions**  
   External functions the agent can call (weather, Wikipedia, calculator, translation).  
   *Added in Module 2 and used heavily in all later modules.*

4. **Planner**  
   The logic layer that asks the LLM to respond in **strict JSON**: either an action or a final answer.  
   *Built in Module 3.*

5. **RAO Loop (Reason–Act–Observe)**  
   The iterative cycle: reason → act → observe → repeat.  
   *Implemented in Module 3, enhanced in Module 4.*

6. **Memory**  
   Agents can reuse past results within a session.  
   *Introduced in Module 3 Extensions.*

7. **Configuration & Packaging**  
   Managing API keys, dependencies, CLI flags, caching, and retries.  
   *Taught in Module 4.*

8. **User Experience (UX)**  
   Making agents user-friendly with pretty outputs, JSON mode, verbose traces, and transcripts.  
   *Added in Module 4.*

9. **Domain-Specific Agents**  
   Tailoring an agent to a problem area (e.g., travel planning).  
   *Built in Module 5.*

10. **Showcase & Reflection**  
    Practicing, demoing, and reflecting on how agents work.  
    *Done in Module 6.*

---

## 🛣️ Workshop Roadmap (Modules 1–6)

### **Module 1 – Setup & Hello World (15 min)**
- Install tools, create accounts, get API keys.  
- Run your first LLM “Hello World” script.  
- Learn: LLM basics, environment setup, API usage.

### **Module 2 – First Tools (30 min)**
- Add tools like weather, Wikipedia, calculator.  
- See how LLM + tools = more powerful agent.  
- Learn: tools, actions, API integration.

### **Module 3 – Reason–Act–Observe Loop (45 min)**
- Build a loop where the agent plans in JSON.  
- Agent decides next step, executes, observes, repeats.  
- Learn: RAO loop, planner, observations, memory.

### **Module 4 – Packaging & UX (45 min)**
- Package the agent as a CLI app.  
- Add caching, retries, environment config.  
- Improve UX with `--pretty`, `--json`, `--verbose`.  
- Learn: config, packaging, caching, debugging.

### **Module 5 – Travel Planner Agent (45 min)**
- Capstone project: build a domain-specific agent.  
- Uses weather, wiki, distance, translation.  
- Produces a day-by-day itinerary.  
- Learn: domain agents, combining tools, structured planning.

### **Module 6 – Showcase & Wrap-Up (30 min)**
- Recap key lessons.  
- Participants demo their agents.  
- Reflect on applications of Agentic AI.  
- Provide feedback.  

---

## 🌟 By the End of This Workshop, You Will…
- Understand the **core concepts** of Agentic AI.  
- Be able to build your own **RAO loop agent** with tools.  
- Know how to **package** an agent as a CLI app.  
- Build a **domain-specific agent** (Travel Planner).  
- Have ideas for how to apply Agentic AI in school, work, or projects.  

---

## 🚀 Next Steps After the Workshop
- Add more tools (news, finance, maps, databases).  
- Experiment with advanced memory (vector stores, long-term).  
- Try other LLMs (Claude, Ollama, LM Studio).  
- Explore safety, ethics, and production readiness of agents.  
