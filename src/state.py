"""Persist seen article URLs for cross-run deduplication."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

DEFAULT_STATE_PATH = Path(__file__).resolve().parent.parent / "data" / "seen_articles.json"


def load_state(path: Path = DEFAULT_STATE_PATH) -> dict:
    if not path.exists():
        return {"urls": {}, "max_entries": 500, "prune_days": 7}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict, path: Path = DEFAULT_STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")


def is_seen(url: str, state: dict) -> bool:
    return url in state.get("urls", {})


def mark_seen(urls: list[str], state: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    state.setdefault("urls", {})
    for url in urls:
        state["urls"][url] = now
    _prune_state(state)
    return state


def _prune_state(state: dict) -> None:
    urls: dict[str, str] = state.get("urls", {})
    prune_days = state.get("prune_days", 7)
    max_entries = state.get("max_entries", 500)
    cutoff = datetime.now(timezone.utc) - timedelta(days=prune_days)

    pruned = {
        url: ts
        for url, ts in urls.items()
        if _parse_ts(ts) >= cutoff
    }

    if len(pruned) > max_entries:
        sorted_urls = sorted(pruned.items(), key=lambda x: _parse_ts(x[1]), reverse=True)
        pruned = dict(sorted_urls[:max_entries])

    state["urls"] = pruned


def _parse_ts(ts: str) -> datetime:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
