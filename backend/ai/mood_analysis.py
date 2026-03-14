import json

from .openai_client import chat_completion_json
from .prompts import MOOD_ANALYSIS_SYSTEM_PROMPT
from .schemas import MoodAnalysisResult

def analyse_mood(entry_text: str) -> MoodAnalysisResult:
    """
    Analyse a single journal entry and return structured mood data.
    """

    user_prompt = f"""
Journal entry:
{entry_text}

Return JSON with:
- emotion
- intensity
- themes
- risk_level
- needs_followup
- reasoning_summary
"""

    messages = [
        {"role": "system", "content": MOOD_ANALYSIS_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw_response = chat_completion_json(messages, max_tokens=250)
    parsed = json.loads(raw_response)

    return MoodAnalysisResult(**parsed)