"""Weekly Sunday synthesis: read the past week's digests, email trends + career actions."""

from __future__ import annotations

import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone

from src.archive import ARCHIVE_DIR, save_digest
from src.brain import generate_text
from src.config import READER_PERSONA, WEEKLY_PROMPT_TEMPLATE
from src.emailer import send_digest_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

LOOKBACK_DAYS = 7
DAILY_DIGEST_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-(morning|evening)\.md$")


def collect_week_digests() -> str:
    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    sections: list[str] = []

    for md_file in sorted(ARCHIVE_DIR.glob("*.md")):
        match = DAILY_DIGEST_PATTERN.match(md_file.name)
        if not match:
            continue
        date_str, slot = match.groups()
        try:
            file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if file_date < cutoff:
            continue
        content = md_file.read_text(encoding="utf-8").strip()
        sections.append(f"### Digest: {date_str} ({slot})\n\n{content}")

    return "\n\n---\n\n".join(sections)


def main() -> int:
    digests = collect_week_digests()
    if not digests:
        logger.info("No daily digests found in the past %d days; skipping", LOOKBACK_DAYS)
        return 0

    prompt = WEEKLY_PROMPT_TEMPLATE.format(persona=READER_PERSONA, digests=digests)
    text = generate_text(prompt)
    if not text:
        logger.error("All AI models failed for weekly synthesis")
        return 1

    save_digest(text, "weekly")

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    subject = f"Nigeria & Tech Weekly Synthesis — {date_str}"
    if os.environ.get("DRY_RUN") == "1":
        logger.info("DRY_RUN=1 — skipping email send")
    else:
        send_digest_email(subject, text)

    logger.info("Weekly synthesis complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
