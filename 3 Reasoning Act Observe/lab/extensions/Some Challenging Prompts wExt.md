# 📰 Sample Inputs for `planner_agent_ext.py`

These inputs are designed to make the extended RAO agent (with news + memory) loop several times, often requiring 4–7+ tool calls.

## 10 Challenging Prompts

1. **News + math**  
   “Give me today’s top 3 news about artificial intelligence, then tell me how many letters are in the first headline.”

2. **Weather comparison with memory**  
   “What’s the weather in Tokyo today? Now, based on that, tell me if it’s hotter or colder than the average of New York and London.”

3. **News + Wikipedia**  
   “Find me news about climate change, then summarize the topic ‘Global warming’ from Wikipedia, then compare which is more alarming.”

4. **Wiki + news + math**  
   “Tell me about Elon Musk from Wikipedia, then fetch the latest news about him, and finally count how many words are in the second headline.”

5. **Math + weather**  
   “What is the sum of 45.2, the temp in Singapore, and the number of characters in the word ‘AgenticAI’?”

6. **News + weather + check**  
   “Get me the news about AI ethics, then also tell me if today’s Manila weather is warmer than 28°C.”

7. **Wiki + multiple cities with memory**  
   “Explain the Eiffel Tower from Wikipedia, then add the temperature of London and Paris together (use London + memory fallback).”

8. **News + Wikipedia + logic**  
   “Find news about robotics, then summarize Wikipedia on ‘Robot’, then tell me if the word ‘Robot’ has more letters than the number of news headlines returned.”

9. **Memory-based weather**  
   “What’s the weather today? (relies on memory: last city asked) Then check the temperature in New York, then compute their difference.”

10. **News + Wikipedia + math + explanation**  
   “Get me news about renewable energy, Wikipedia summary of ‘Solar power’, then compute 2025 - 1977, and explain why that year matters for solar.”
