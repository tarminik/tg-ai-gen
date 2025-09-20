"""
DeepSeek API lightweight async client.

This module provides a small, self-contained async function to request
text generation from DeepSeek using its OpenAI-compatible
`/chat/completions` endpoint.

We keep the surface area tiny and document choices for clarity.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional
import json

import aiohttp

from config import config


async def generate_text(
    prompt: str,
    *,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    request_timeout_seconds: int = 60,
) -> str:
    """
    Call DeepSeek's chat completions API and return the assistant content string.

    - Uses values from `config.deepseek` for base URL, API key, and model.
    - Sends a simple 1-2 message chat with optional system message.
    - Returns first choice content as plain text.

    We choose aiohttp directly to avoid heavy SDKs and keep dependencies lean.
    """

    # Build endpoint and headers using env-configured values.
    # The DeepSeek API is OpenAI-compatible.
    base_url: str = config.deepseek.ds_base_url.rstrip("/")
    # If version is not included in base_url, default to /v1 path (DeepSeek default)
    if "/v" in base_url.split("/")[-1]:
        # base_url already ends with a version-like suffix (e.g., /v1)
        endpoint: str = f"{base_url}/chat/completions"
    else:
        endpoint = f"{base_url}/v1/chat/completions"
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {config.deepseek.ds_api_key}",
        "Content-Type": "application/json",
    }

    # Prepare messages: optional system message + user prompt.
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload: Dict[str, Any] = {
        "model": config.deepseek.ds_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    timeout = aiohttp.ClientTimeout(total=request_timeout_seconds)

    # Make the HTTP request with proper timeout and error handling.
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(endpoint, headers=headers, json=payload) as resp:
            # Read response body first to provide clearer error messages on failure
            raw_text: str = await resp.text()
            if resp.status >= 400:
                # Try to decode structured error message if available
                err_message = raw_text
                try:
                    err_json = json.loads(raw_text)
                    # Common OpenAI-compatible error shapes
                    err_message = (
                        err_json.get("error", {}).get("message")
                        or err_json.get("message")
                        or raw_text
                    )
                except Exception:
                    pass
                raise RuntimeError(f"DeepSeek API error {resp.status}: {err_message}")

            try:
                data: Dict[str, Any] = json.loads(raw_text)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"DeepSeek returned non-JSON response: {raw_text}") from exc

    # Defensive parsing with clear errors in case API shape changes.
    try:
        choices = data["choices"]
        first = choices[0]
        message = first["message"]
        content: str = message["content"]
    except Exception as exc:  # Keep narrow scope; raise a readable error.
        raise RuntimeError(f"Unexpected DeepSeek response format: {data}") from exc

    return content.strip()


async def _demo() -> None:
    """Small local demo helpful during development. Not used in production run."""
    text = await generate_text("Кратко: что такое aiogram?")
    print(text)


if __name__ == "__main__":
    asyncio.run(_demo())


