import os
from huggingface_hub import InferenceClient

# You can use any compatible instruct model; this is a good default
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise ValueError("HUGGINGFACE_API_KEY environment variable not set! "
                     "Create one at https://huggingface.co/settings/tokens")

client = InferenceClient(model=MODEL_ID, token=api_key)
resp = client.text_generation("Say hello world in a fun way!")
print("AI says:", resp)
