"""Validate all RSS feed endpoints."""

from __future__ import annotations

import sys
from datetime import datetime, timezone

import httpx
import feedparser

from src.config import FEED_TIMEOUT_SECONDS, GLOBAL_TECH_FEEDS, NIGERIAN_FEEDS, USER_AGENT


def validate_feeds() -> int:
    all_feeds = {**NIGERIAN_FEEDS, **GLOBAL_TECH_FEEDS}
    failed: list[str] = []
    ok_count = 0

    print(f"Validating {len(all_feeds)} feeds...\n")

    with httpx.Client(timeout=FEED_TIMEOUT_SECONDS, follow_redirects=True) as client:
        for name, url in all_feeds.items():
            try:
                response = client.get(url, headers={"User-Agent": USER_AGENT})
                response.raise_for_status()
                parsed = feedparser.parse(response.content)
                count = len(parsed.entries)
                latest = "n/a"
                if parsed.entries:
                    entry = parsed.entries[0]
                    latest = entry.get("published") or entry.get("updated") or "unknown"
                print(f"OK  {name:20} entries={count:3}  latest={latest}")
                print(f"    {url}")
                ok_count += 1
            except Exception as exc:
                print(f"FAIL {name:20} {exc}")
                print(f"    {url}")
                failed.append(name)

    print(f"\n{ok_count}/{len(all_feeds)} feeds OK")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(validate_feeds())
