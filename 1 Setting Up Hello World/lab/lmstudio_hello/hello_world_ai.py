# Requires LM Studio running a local server (OpenAI-compatible) on http://localhost:1234/v1
# In LM Studio: enable "Local Server" and start a model (e.g., Mistral or Llama 3).

import openai

client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

resp = client.chat.completions.create(
    model="local-model",  # LM Studio will route to the loaded model
    messages=[{"role": "user", "content": "Say hello world in a fun way!"}]
)
print("AI says:", resp.choices[0].message.content)
