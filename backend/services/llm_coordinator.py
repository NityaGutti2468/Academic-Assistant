import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from services.agent_registry import list_agent_capabilities


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BACKEND_ROOT / ".env", override=True)

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"


def is_llm_enabled():
    return bool(get_llm_api_key())


def get_llm_provider():
    return os.getenv("LLM_PROVIDER", "openai").lower()


def get_llm_model():
    provider = get_llm_provider()
    if provider == "groq":
        return os.getenv("LLM_MODEL") or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_llm_api_key():
    provider = get_llm_provider()
    if provider == "groq":
        return os.getenv("GROQ_API_KEY")
    return os.getenv("OPENAI_API_KEY")


def _extract_text(payload):
    if payload.get("output_text"):
        return payload["output_text"]

    chunks = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                chunks.append(text)
    return "\n".join(chunks).strip()


def _call_openai(prompt):
    api_key = get_llm_api_key()
    model = get_llm_model()

    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": prompt,
        },
        timeout=20,
    )
    response.raise_for_status()
    return _extract_text(response.json())


def _call_groq(prompt):
    api_key = get_llm_api_key()
    model = get_llm_model()

    response = requests.post(
        GROQ_CHAT_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def _call_llm(prompt):
    provider = get_llm_provider()
    if provider == "groq":
        return _call_groq(prompt)
    return _call_openai(prompt)


def _parse_json_object(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(text[start:end + 1])


def choose_tool_with_llm(query):
    capabilities = list_agent_capabilities()
    prompt = f"""
You are the LLM Planner Agent for a college academic assistant.

Choose exactly one tool for the user query from the available tools.
Return only JSON with these keys:
- tool: selected tool name, or null
- agent: selected agent name, or "Coordinator Agent"
- reasoning: one short sentence

Available tools:
{json.dumps(capabilities, indent=2)}

User query:
{query}
"""
    raw_text = _call_llm(prompt)
    return _parse_json_object(raw_text)


def summarize_tool_result_with_llm(query, tool_result):
    prompt = f"""
You are an academic assistant. Explain the tool result clearly to the student.
Be concise, supportive, and do not invent facts.

Original user query:
{query}

Tool result JSON:
{json.dumps(tool_result, default=str, indent=2)}
"""
    return _call_llm(prompt)
