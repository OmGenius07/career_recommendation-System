import os
import asyncio
import random
import httpx

# Read Gemini API key from environment
API_KEY = ""

RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

async def get_career_recommendations(prompt: str, max_retries: int = 5) -> str:
    if not API_KEY:
        raise RuntimeError("Missing GOOGLE_API_KEY or GEMINI_API_KEY environment variable")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent?key=" + API_KEY
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {"temperature": 0.7}
    }

    async with httpx.AsyncClient(timeout=60) as client:
        attempt = 0
        while True:
            try:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                data = resp.json()
                # Extract text from candidates → content.parts[*].text
                candidates = data.get("candidates", [])
                if not candidates:
                    return ""
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                texts = [p.get("text", "") for p in parts if isinstance(p, dict)]
                return "\n".join([t for t in texts if t])
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if status in RETRY_STATUS_CODES and attempt < max_retries:
                    delay = (2 ** attempt) + random.uniform(0, 0.5)
                    attempt += 1
                    await asyncio.sleep(delay)
                    continue
                raise RuntimeError(f"LLM API error {status}: {exc.response.text}") from exc
            except (httpx.RequestError, httpx.TimeoutException) as exc:
                if attempt < max_retries:
                    delay = (2 ** attempt) + random.uniform(0, 0.5)
                    attempt += 1
                    await asyncio.sleep(delay)
                    continue
                raise RuntimeError(f"LLM API request failed: {exc}") from exc
