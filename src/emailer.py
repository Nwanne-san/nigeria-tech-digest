"""Send digest emails via Resend."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone

import markdown
import resend

logger = logging.getLogger(__name__)


def build_subject(slot: str) -> str:
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    label = "Morning" if slot == "morning" else "Evening"
    return f"Nigeria & Tech {label} Brief — {date_str}"


def markdown_to_html(md_content: str) -> str:
    body = markdown.markdown(md_content, extensions=["extra", "sane_lists"])
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Georgia, serif; max-width: 720px; margin: 2rem auto; line-height: 1.6; color: #1a1a1a; }}
    h1, h2, h3 {{ color: #0d3b2e; }}
    a {{ color: #1a6b4a; }}
    hr {{ border: none; border-top: 1px solid #ddd; margin: 2rem 0; }}
  </style>
</head>
<body>
{body}
</body>
</html>"""


def send_digest_email(subject: str, md_content: str) -> None:
    api_key = os.environ.get("RESEND_API_KEY")
    from_email = os.environ.get("DIGEST_FROM_EMAIL", "onboarding@resend.dev")
    to_email = os.environ.get("DIGEST_TO_EMAIL", "nnamaninwanne@gmail.com")

    if not api_key:
        raise ValueError("RESEND_API_KEY is not set")

    resend.api_key = api_key
    html_body = markdown_to_html(md_content)

    _send_with_retry(
        {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
        }
    )


def _send_with_retry(payload: dict, retries: int = 1) -> None:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            resend.Emails.send(payload)
            logger.info("Email sent to %s", payload["to"])
            return
        except Exception as exc:
            last_error = exc
            logger.warning("Resend attempt %d failed: %s", attempt + 1, exc)
            if attempt < retries:
                time.sleep(2)
    raise last_error  # type: ignore[misc]
