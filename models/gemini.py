import os
import json
from google import genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)


def _load_system_prompt():
    try:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(this_dir, "system_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def _strip_code_fences(text: str) -> str:
    if not isinstance(text, str):
        return text
    trimmed = text.strip()
    # Remove opening fence with optional language tag
    if trimmed.startswith("```"):
        first_newline = trimmed.find("\n")
        if first_newline != -1:
            trimmed = trimmed[first_newline + 1 :]
        # Remove trailing fence
        if trimmed.endswith("```"):
            trimmed = trimmed[:-3]
    return trimmed.strip()


def generate(query: str):
    system_prompt = _load_system_prompt()
    user_block = f"USER QUERY: {query}"
    prompt = f"{system_prompt}\n\n{user_block}" if system_prompt else user_block

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Model returned empty response.")

    stripped = _strip_code_fences(text)
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        # Fallback: extract the first JSON-like list region
        start = stripped.find("[")
        end = stripped.rfind("]")
        if start != -1 and end != -1 and end > start:
            candidate = stripped[start : end + 1]
            parsed = json.loads(candidate)
        else:
            raise

    if not isinstance(parsed, list):
        raise ValueError("Expected a list of shapes from the model.")

    return parsed
    