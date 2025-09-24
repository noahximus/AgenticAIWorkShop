import os
import google.generativeai as genai


# 👇 Paste your Gemini API key directly here
# api_key = "YOUR_GEMINI_API_KEY"
api_key = os.getenv("GOOGLE_API_KEY")


if not api_key or api_key == "YOUR_GEMINI_API_KEY":
    raise ValueError("Please update the script with your actual Gemini API key!")

# Configure Gemini with the key
genai.configure(api_key=api_key)

# Create the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Run Hello World
resp = model.generate_content("Say hello world in a fun way!")
print("AI says:", resp.text)