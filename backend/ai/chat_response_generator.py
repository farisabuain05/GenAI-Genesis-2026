import json
from typing import List, Dict, Optional

from .openai_client import chat_completion
from .prompts import CHAT_RESPONSE_SYSTEM_PROMPT


def generate_chat_response(
    user_message: str,
    chat_history: List[Dict],
    similar_entries: List[Dict],
    user_profile_memory: Optional[str] = None,
) -> dict:
    history_text = "\n".join(
        f"{msg.get('role', 'user')}: {msg.get('content', '')}"
        for msg in chat_history[-6:]
    ) if chat_history else "No recent chat history."

    similar_text = "\n".join(
        f"- {entry.get('timestamp', 'unknown time')}: {entry.get('text', '')}"
        for entry in similar_entries
    ) if similar_entries else "No similar journal entries found."

    memory_text = user_profile_memory or "No memory yet."

    user_prompt = f"""
    USER MEMORY:
    {memory_text}

    SIMILAR PAST JOURNAL ENTRIES:
    {similar_text}

    RECENT CHAT HISTORY:
    {history_text}

    LATEST USER MESSAGE:
    {user_message}

    Respond in a way that feels human and natural.
    Do not sound clinical, preachy, overly polished, or condescending.
    Avoid generic therapy phrases like "It sounds like..." unless truly needed.
    Prefer simple, emotionally warm language.

    Return only valid JSON.
    Do not include markdown.
    Do not include backticks.
    Do not include reasoning.

    Use exactly this structure:
    {{
      "reply": "string",
      "open_question": "string",
      "used_similar_entries": true
    }}
    """

    messages = [
        {"role": "system", "content": CHAT_RESPONSE_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    for _ in range(2):
        raw_response = chat_completion(messages, max_tokens=800, temperature=0.4)

        print("Raw chat response output:")
        print(raw_response)

        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            print("Retrying chat response generation due to JSON error...")

    raise ValueError("Model repeatedly returned invalid JSON for chat response generation.")