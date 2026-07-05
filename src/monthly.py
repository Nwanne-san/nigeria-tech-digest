"""Monthly retrospective: synthesize the previous calendar month's digests."""

from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime, timezone

from src.archive import ARCHIVE_DIR, save_digest
from src.brain import generate_text
from src.config import MONTHLY_PROMPT_TEMPLATE, READER_PERSONA
from src.emailer import send_digest_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DAILY_DIGEST_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-(morning|evening)\.md$")


def _previous_month() -> tuple[str, str]:
    """Returns (YYYY-MM prefix, human label) for the previous calendar month."""
    now = datetime.now(timezone.utc)
    year, month = (now.year - 1, 12) if now.month == 1 else (now.year, now.month - 1)
    prev = datetime(year, month, 1, tzinfo=timezone.utc)
    return prev.strftime("%Y-%m"), prev.strftime("%B %Y")


def collect_month_digests(month_prefix: str) -> str:
    sections: list[str] = []
    for md_file in sorted(ARCHIVE_DIR.glob(f"{month_prefix}-*.md")):
        match = DAILY_DIGEST_PATTERN.match(md_file.name)
        if not match:
            continue
        date_str, slot = match.groups()
        content = md_file.read_text(encoding="utf-8").strip()
        sections.append(f"### Digest: {date_str} ({slot})\n\n{content}")
    return "\n\n---\n\n".join(sections)


def main() -> int:
    month_prefix, month_label = _previous_month()
    digests = collect_month_digests(month_prefix)
    if not digests:
        logger.info("No daily digests found for %s; skipping", month_label)
        return 0

    prompt = MONTHLY_PROMPT_TEMPLATE.format(persona=READER_PERSONA, digests=digests)
    text = generate_text(prompt)
    if not text:
        logger.error("All AI models failed for monthly retrospective")
        return 1

    save_digest(text, "monthly")

    subject = f"Nigeria & Tech Monthly Retrospective — {month_label}"
    if os.environ.get("DRY_RUN") == "1":
        logger.info("DRY_RUN=1 — skipping email send")
    else:
        send_digest_email(subject, text)

    logger.info("Monthly retrospective complete (%s)", month_label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
