import json
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model settings
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

# File paths
ARTIFACTS_FOLDER = os.path.join(os.getcwd(), "artifacts")
INPUT_FOLDER = os.path.join(ARTIFACTS_FOLDER, "inputs")
PROCESSED_FOLDER = os.path.join(ARTIFACTS_FOLDER, "processed_data")

# Response structure template
RESPONSE_STRUCTURE = json.dumps(
    {
        "title": "",
        "author": "",
        "content": [],
    },
    indent=2,
)
