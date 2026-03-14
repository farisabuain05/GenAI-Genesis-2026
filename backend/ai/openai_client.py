import os
from openai import OpenAI
MODEL_NAME = "openai/gpt-oss-120b"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "test")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY not found. Make sure the .env is set up correctly"
    )


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://handles-virtual-creating-introduced.trycloudflare.com/v1",
)


def chat_completion(messages, max_tokens=400, temperature=0.3):
    """
    Basic chat completion helper.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content


def chat_completion_json(messages, max_tokens=400):
    """
    Forces JSON output for structured tasks like mood classification.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.2,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content