import os
from dotenv import load_dotenv
from google import genai

from prompts import BUILDER_PROMPT, EDITOR_PROMPT

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

MODEL = "gemini-3-flash-preview"


def generate_website(user_request):
    prompt = f"""
{BUILDER_PROMPT}

USER REQUEST:
{user_request}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


def edit_website(existing_code, edit_request):
    prompt = f"""
{EDITOR_PROMPT}

EXISTING WEBSITE:
-----------------
{existing_code}

USER REQUESTED CHANGE:
----------------------
{edit_request}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text