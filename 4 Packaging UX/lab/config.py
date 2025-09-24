import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env if present

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "GEMINI").upper()
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")

# Timeouts/limits
HTTP_TIMEOUT = 20
MAX_STEPS_DEFAULT = 4
CACHE_FILE = "cache.json"
CACHE_TTL_SEC = 600  # 10 minutes
