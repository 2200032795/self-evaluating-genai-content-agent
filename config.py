import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Validate API key
if not API_KEY:
    raise ValueError("Gemini API key not found. Check your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

print("Gemini configuration loaded successfully!")
