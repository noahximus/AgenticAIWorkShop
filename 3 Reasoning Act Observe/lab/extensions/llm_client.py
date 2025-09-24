import os
from typing import Dict

# Default to Gemini; switchable to LM Studio via env
PROVIDER = os.getenv("LLM_PROVIDER", "GEMINI").upper()

if PROVIDER == "LMSTUDIO":
    # Use OpenAI-compatible client pointed at local LM Studio server
    from openai import OpenAI
    BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    MODEL_NAME = os.getenv("LMSTUDIO_MODEL", "local-model")
    _client = OpenAI(base_url=BASE_URL, api_key="lm-studio")

    def generate_json(prompt: str) -> str:
        # We ask the model to produce JSON; we get .message.content back
        resp = _client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content

else:
    # GEMINI default
    import google.generativeai as genai
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set!")
    genai.configure(api_key=API_KEY)
    _model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_json(prompt: str) -> str:
        resp = _model.generate_content(prompt)
        return resp.text
