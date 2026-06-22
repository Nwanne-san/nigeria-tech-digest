"""Gemini-powered digest generation with tiered lore."""

from __future__ import annotations

import json
import logging
import os

from google import genai
from google.genai import types

from src.config import (
    DIGEST_PROMPT_TEMPLATE,
    FALLBACK_HEADLINES_TEMPLATE,
    GEMINI_MODEL,
    MAX_OUTPUT_TOKENS,
)
from src.fetcher import Article, format_headlines_fallback

logger = logging.getLogger(__name__)


class GeminiRateLimitError(Exception):
    """Raised when Gemini returns a rate-limit response."""


def generate_digest(articles: list[Article]) -> tuple[str, bool]:
    """
    Generate markdown digest via Gemini.

    Returns (markdown_content, used_ai).
    """
    if not articles:
        return "# Nigeria & Tech Brief\n\nNo major updates in this window.", True

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not set; using headline fallback")
        return _headline_fallback(articles), False

    try:
        client = genai.Client(api_key=api_key)
        articles_json = json.dumps([a.to_compact_dict() for a in articles], indent=2)
        prompt = DIGEST_PROMPT_TEMPLATE.format(articles_json=articles_json)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=MAX_OUTPUT_TOKENS,
                temperature=0.4,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise ValueError("Empty response from Gemini")
        return text, True
    except Exception as exc:
        error_msg = str(exc).lower()
        if "429" in error_msg or "quota" in error_msg or "rate" in error_msg or "resource_exhausted" in error_msg:
            logger.warning("Gemini rate limit hit: %s", exc)
            raise GeminiRateLimitError(str(exc)) from exc
        logger.warning("Gemini failed, using headline fallback: %s", exc)
        return _headline_fallback(articles), False


def _headline_fallback(articles: list[Article]) -> str:
    headlines = format_headlines_fallback(articles)
    return FALLBACK_HEADLINES_TEMPLATE.format(headlines=headlines)
