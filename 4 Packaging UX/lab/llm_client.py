from config import GOOGLE_API_KEY, LLM_PROVIDER, LMSTUDIO_BASE_URL, LMSTUDIO_MODEL

if LLM_PROVIDER == "LMSTUDIO":
    # OpenAI-compatible local server
    from openai import OpenAI
    _client = OpenAI(base_url=LMSTUDIO_BASE_URL, api_key="lm-studio")

    def generate_text(prompt: str, temperature: float = 0.2) -> str:
        resp = _client.chat.completions.create(
            model=LMSTUDIO_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return resp.choices[0].message.content
else:
    import google.generativeai as genai
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Put it in .env or export it.")
    genai.configure(api_key=GOOGLE_API_KEY)
    _model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_text(prompt: str, temperature: float = 0.2) -> str:
        resp = _model.generate_content(prompt)
        return resp.text
