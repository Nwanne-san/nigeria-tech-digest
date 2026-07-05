"""Save digests to docs/archive and rebuild the GitHub Pages index."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import markdown

from src.config import ARCHIVE_PRUNE_DAYS

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
ARCHIVE_DIR = DOCS_DIR / "archive"

SLOT_LABELS = {"morning": "Morning", "evening": "Evening", "weekly": "Weekly"}


def _slot_label(slot: str) -> str:
    return SLOT_LABELS.get(slot, slot.title())


def save_digest(md_content: str, slot: str, date: datetime | None = None) -> Path:
    """Write markdown + HTML archive files; rebuild index. Returns md path."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    dt = date or datetime.now(timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")
    base_name = f"{date_str}-{slot}"

    md_path = ARCHIVE_DIR / f"{base_name}.md"
    html_path = ARCHIVE_DIR / f"{base_name}.html"

    header = f"# Nigeria & Tech {_slot_label(slot)} Brief — {date_str}\n\n"
    full_md = header + md_content if not md_content.startswith("#") else md_content
    md_path.write_text(full_md, encoding="utf-8")

    html_body = markdown.markdown(full_md, extensions=["extra", "sane_lists"])
    html_path.write_text(_wrap_archive_page(full_md, html_body, date_str, slot), encoding="utf-8")

    _prune_old_archives()
    _rebuild_index()
    return md_path


def _wrap_archive_page(title_md: str, body_html: str, date_str: str, slot: str) -> str:
    label = _slot_label(slot)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nigeria & Tech {label} Brief — {date_str}</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; line-height: 1.65; color: #1a1a1a; }}
    h1, h2, h3 {{ color: #0d3b2e; }}
    a {{ color: #1a6b4a; }}
    .back {{ margin-bottom: 2rem; font-family: system-ui, sans-serif; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <p class="back"><a href="../index.html">← All digests</a></p>
  {body_html}
</body>
</html>"""


def _rebuild_index() -> None:
    entries: list[tuple[str, str, str]] = []
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-(morning|evening|weekly)\.md$")

    for md_file in sorted(ARCHIVE_DIR.glob("*.md"), reverse=True):
        match = pattern.match(md_file.name)
        if not match:
            continue
        date_str, slot = match.groups()
        label = _slot_label(slot)
        html_name = md_file.stem + ".html"
        entries.append((date_str, label, f"archive/{html_name}"))

    rows = "\n".join(
        f'    <li><a href="{href}">{date} — {label}</a></li>'
        for date, label, href in entries
    )

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nigeria & Tech Daily Digest Archive</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }}
    h1 {{ color: #0d3b2e; }}
    ul {{ line-height: 2; }}
    a {{ color: #1a6b4a; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>Nigeria &amp; Tech Daily Digest</h1>
  <p class="meta">Twice-daily briefings on Nigerian governance, security, progress, and global tech — archived automatically.</p>
  <ul>
{rows if rows else "    <li>No digests yet.</li>"}
  </ul>
</body>
</html>"""

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")


def _prune_old_archives() -> None:
    cutoff = datetime.now(timezone.utc) - timedelta(days=ARCHIVE_PRUNE_DAYS)
    pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-(morning|evening|weekly)\.(md|html)$")

    for path in ARCHIVE_DIR.glob("*"):
        match = pattern.match(path.name)
        if not match:
            continue
        date_str = match.group(1)
        try:
            file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if file_date < cutoff:
            path.unlink(missing_ok=True)
