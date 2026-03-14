import json
from typing import List, Optional, Dict, Any

from .openai_client import chat_completion_json
from .prompts import RESPONSE_GENERATION_SYSTEM_PROMPT
from .schemas import GeneratedResponse


def _format_recent_entries(recent_entries: List[Dict[str, Any]]) -> str:
    if not recent_entries:
        return "No recent entries."

    lines = []
    for entry in recent_entries:
        timestamp = entry.get("timestamp", "unknown time")
        text = entry.get("text", "")
        lines.append(f"- {timestamp}: {text}")

    return "\n".join(lines)


def generate_reflective_response(
    today_entry: str,
    recent_entries: List[Dict[str, Any]],
    user_profile_memory: Optional[str] = None,
) -> GeneratedResponse:
    """
    Generate a supportive motivational interviewing style response.
    """

    recent_entries_text = _format_recent_entries(recent_entries)
    memory_text = user_profile_memory or "No saved user profile memory yet."

    user_prompt = f"""
USER PROFILE MEMORY:
{memory_text}

RECENT ENTRIES:
{recent_entries_text}

TODAY'S ENTRY:
{today_entry}

Return JSON with:
- reflection
- open_question
- coping_suggestion
"""

    messages = [
        {"role": "system", "content": RESPONSE_GENERATION_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw_response = chat_completion_json(messages, max_tokens=350)
    parsed = json.loads(raw_response)

    return GeneratedResponse(**parsed)