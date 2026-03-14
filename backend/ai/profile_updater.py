import json
from typing import List, Optional, Dict, Any

from .openai_client import chat_completion_json
from .prompts import PROFILE_UPDATE_SYSTEM_PROMPT
from .schemas import UserProfileMemory


def _format_entries(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "No recent entries."

    lines = []
    for entry in entries:
        timestamp = entry.get("timestamp", "unknown time")
        text = entry.get("text", "")
        mood_label = entry.get("mood_label", "unknown")
        intensity = entry.get("intensity", "unknown")
        lines.append(
            f"- {timestamp} | mood={mood_label} | intensity={intensity}\n  {text}"
        )

    return "\n".join(lines)


def update_user_profile_memory(
    recent_entries: List[Dict[str, Any]],
    current_memory: Optional[str] = None,
) -> UserProfileMemory:
    """
    Summarise recent user patterns into long-term profile memory.
    """

    entries_text = _format_entries(recent_entries)
    memory_text = current_memory or "No existing memory."

    user_prompt = f"""
CURRENT MEMORY:
{memory_text}

RECENT JOURNAL ENTRIES:
{entries_text}

Return JSON with:
- common_stressors
- recurring_emotions
- helpful_strategies
- support_preferences
- recent_patterns
- summary
"""

    messages = [
        {"role": "system", "content": PROFILE_UPDATE_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw_response = chat_completion_json(messages, max_tokens=400)
    parsed = json.loads(raw_response)

    return UserProfileMemory(**parsed)