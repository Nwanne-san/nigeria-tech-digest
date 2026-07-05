"""Persistent storyline tracker: gives digests memory of ongoing sagas."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from src.brain import generate_json
from src.config import STORYLINE_UPDATE_PROMPT

logger = logging.getLogger(__name__)

DEFAULT_STORYLINES_PATH = Path(__file__).resolve().parent.parent / "data" / "storylines.json"
MAX_STORYLINES = 15
REQUIRED_FIELDS = {"name", "status", "summary", "last_updated"}


def load_storylines(path: Path = DEFAULT_STORYLINES_PATH) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not load storylines: %s", exc)
        return []


def save_storylines(storylines: list[dict], path: Path = DEFAULT_STORYLINES_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(storylines, indent=2) + "\n", encoding="utf-8")


def update_storylines(storylines: list[dict], digest_md: str) -> list[dict] | None:
    """Ask the model to fold today's digest into the tracker. Returns None on failure."""
    prompt = STORYLINE_UPDATE_PROMPT.format(
        storylines_json=json.dumps(storylines, indent=2),
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        digest_md=digest_md,
    )
    result = generate_json(prompt)
    if not isinstance(result, list):
        logger.warning("Storyline update failed or returned non-list; keeping previous state")
        return None

    valid = [
        item for item in result
        if isinstance(item, dict) and REQUIRED_FIELDS.issubset(item.keys())
    ]
    if not valid:
        logger.warning("Storyline update returned no valid entries; keeping previous state")
        return None
    return valid[:MAX_STORYLINES]
