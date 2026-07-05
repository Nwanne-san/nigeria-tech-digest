"""RSS fetcher: pull, normalize, rank, and filter articles."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from typing import Literal

import feedparser
import httpx

from src.config import (
    ENTRIES_PER_FEED,
    FEED_TIMEOUT_SECONDS,
    FULL_TEXT_MAX_CHARS,
    FULL_TEXT_TOP_N,
    GLOBAL_TECH_FEEDS,
    KEYWORDS,
    MAX_ARTICLES_FOR_AI,
    NIGERIAN_FEEDS,
    SUMMARY_TRUNCATE_CHARS,
    TIME_WINDOWS_HOURS,
    USER_AGENT,
)
from src.state import is_seen

logger = logging.getLogger(__name__)

Category = Literal["nigeria", "tech"]


@dataclass
class Article:
    title: str
    link: str
    published_at: str
    summary: str
    source: str
    category: Category
    score: float = 0.0
    published_dt: datetime | None = None
    full_text: str = ""

    def to_compact_dict(self, include_full_text: bool = False) -> dict:
        data = {
            "title": self.title,
            "link": self.link,
            "published_at": self.published_at,
            "summary": self.summary[:SUMMARY_TRUNCATE_CHARS],
            "source": self.source,
            "category": self.category,
        }
        if include_full_text and self.full_text:
            data["full_text"] = self.full_text
        return data


def fetch_all_articles(
    slot: str,
    state: dict,
    *,
    skip_seen: bool = True,
) -> list[Article]:
    window_hours = TIME_WINDOWS_HOURS.get(slot, 14)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
    articles: list[Article] = []

    for source, url in {**NIGERIAN_FEEDS, **GLOBAL_TECH_FEEDS}.items():
        category: Category = "nigeria" if source in NIGERIAN_FEEDS else "tech"
        try:
            entries = _fetch_feed(url, source, category)
            for entry in entries:
                if entry.published_dt and entry.published_dt < cutoff:
                    continue
                if skip_seen and is_seen(entry.link, state):
                    continue
                articles.append(entry)
        except Exception as exc:
            logger.warning("Feed failed for %s (%s): %s", source, url, exc)

    ranked = _rank_articles(articles)
    return ranked[:MAX_ARTICLES_FOR_AI]


def enrich_articles(articles: list[Article], top_n: int = FULL_TEXT_TOP_N) -> None:
    """Fetch full article text for the top-ranked articles (best effort)."""
    import trafilatura

    enriched = 0
    with httpx.Client(timeout=FEED_TIMEOUT_SECONDS, follow_redirects=True) as client:
        for article in articles[:top_n]:
            try:
                response = client.get(article.link, headers={"User-Agent": USER_AGENT})
                response.raise_for_status()
                text = trafilatura.extract(response.text) or ""
                text = text.strip()
                if len(text) > len(article.summary):
                    article.full_text = text[:FULL_TEXT_MAX_CHARS]
                    enriched += 1
            except Exception as exc:
                logger.debug("Full-text fetch failed for %s: %s", article.link, exc)
    logger.info("Full text extracted for %d/%d top articles", enriched, min(top_n, len(articles)))


def _fetch_feed(url: str, source: str, category: Category) -> list[Article]:
    last_error: Exception | None = None
    for attempt in range(2):
        try:
            with httpx.Client(timeout=FEED_TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = client.get(url, headers={"User-Agent": USER_AGENT})
                response.raise_for_status()
                parsed = feedparser.parse(response.content)
            return _parse_entries(parsed, source, category)
        except Exception as exc:
            last_error = exc
            if attempt == 0:
                logger.debug("Retrying feed %s after: %s", source, exc)
    raise last_error  # type: ignore[misc]


def _parse_entries(parsed: feedparser.FeedParserDict, source: str, category: Category) -> list[Article]:
    articles: list[Article] = []
    for entry in parsed.entries[:ENTRIES_PER_FEED]:
        link = (entry.get("link") or "").strip()
        title = _clean_text(entry.get("title", "Untitled"))
        if not link or not title:
            continue

        published_dt = _parse_published(entry)
        summary = _extract_summary(entry)

        articles.append(
            Article(
                title=title,
                link=link,
                published_at=published_dt.isoformat(),
                summary=summary,
                source=source,
                category=category,
                published_dt=published_dt,
            )
        )
    return articles


def _parse_published(entry: feedparser.FeedParserDict) -> datetime:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        parsed = entry.get(key)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass

    for key in ("published", "updated", "created"):
        raw = entry.get(key)
        if raw:
            try:
                dt = parsedate_to_datetime(raw)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc)
            except (TypeError, ValueError):
                pass

    return datetime.now(timezone.utc)


def _extract_summary(entry: feedparser.FeedParserDict) -> str:
    raw = entry.get("summary") or entry.get("description") or ""
    text = _clean_text(raw)
    if not text and entry.get("content"):
        for item in entry.content:
            value = item.get("value", "")
            if value:
                text = _clean_text(value)
                break
    return text[:SUMMARY_TRUNCATE_CHARS]


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _rank_articles(articles: list[Article]) -> list[Article]:
    keyword_patterns = [
        (re.compile(rf"\b{re.escape(kw.lower())}\b"), weight)
        for kw, weight in KEYWORDS.items()
    ]
    now = datetime.now(timezone.utc)

    for article in articles:
        score = 0.0
        blob = f"{article.title} {article.summary}".lower()

        for pattern, weight in keyword_patterns:
            if pattern.search(blob):
                score += weight

        if article.category == "nigeria":
            score += 1.0

        try:
            published = datetime.fromisoformat(article.published_at.replace("Z", "+00:00"))
            age_hours = max((now - published).total_seconds() / 3600, 0.1)
            score += max(0, 24 - age_hours) / 24
        except ValueError:
            pass

        article.score = score

    return sorted(articles, key=lambda a: a.score, reverse=True)


def articles_to_json(articles: list[Article]) -> str:
    import json

    return json.dumps([a.to_compact_dict() for a in articles], indent=2)


def format_headlines_fallback(articles: list[Article]) -> str:
    lines = []
    for article in articles:
        lines.append(f"- **{article.title}** ({article.source}) — {article.link}")
    return "\n".join(lines)
