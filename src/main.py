"""Main orchestrator for the Nigeria & Tech daily digest."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from src.archive import save_digest
from src.brain import generate_digest
from src.config import MIN_ARTICLES_FOR_DIGEST
from src.emailer import build_subject, send_digest_email
from src.fetcher import enrich_articles, fetch_all_articles, format_headlines_fallback
from src.state import load_state, mark_seen, save_state
from src.storylines import load_storylines, save_storylines, update_storylines

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"


def main() -> int:
    slot = os.environ.get("DIGEST_SLOT", "morning").lower()
    if slot not in ("morning", "evening"):
        logger.error("Invalid DIGEST_SLOT: %s", slot)
        return 1

    state_path = Path(__file__).resolve().parent.parent / "data" / "seen_articles.json"
    state = load_state(state_path)

    logger.info("Fetching articles for %s digest...", slot)
    articles = fetch_all_articles(slot, state)
    logger.info("Found %d new articles after filtering", len(articles))

    _write_artifact(articles, slot)

    storylines = load_storylines()

    if len(articles) < MIN_ARTICLES_FOR_DIGEST:
        md_content = (
            f"# Nigeria & Tech {'Morning' if slot == 'morning' else 'Evening'} Brief\n\n"
            f"Quiet period — only {len(articles)} new articles in this window.\n\n"
        )
        if articles:
            md_content += "## Headlines\n\n" + format_headlines_fallback(articles)
        used_ai = False
    else:
        enrich_articles(articles)
        md_content, used_ai = generate_digest(
            articles, slot, storylines_json=json.dumps(storylines)
        )

    save_digest(md_content, slot)

    if used_ai:
        updated = update_storylines(storylines, md_content)
        if updated is not None:
            save_storylines(updated)
            logger.info("Storylines updated (%d tracked)", len(updated))

    subject = build_subject(slot)
    if os.environ.get("DRY_RUN") == "1":
        logger.info("DRY_RUN=1 — skipping email send")
    else:
        try:
            send_digest_email(subject, md_content)
        except Exception as exc:
            logger.error("Failed to send email: %s", exc)
            return 1

    if articles:
        state = mark_seen([a.link for a in articles], state)
        save_state(state, state_path)

    logger.info(
        "Digest complete (slot=%s, articles=%d, ai=%s)",
        slot,
        len(articles),
        used_ai,
    )
    return 0


def _write_artifact(articles, slot: str) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACTS_DIR / f"raw-headlines-{slot}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump([a.to_compact_dict() for a in articles], f, indent=2)


if __name__ == "__main__":
    sys.exit(main())
