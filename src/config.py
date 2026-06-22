"""Configuration for feeds, keywords, and AI prompt templates."""

from __future__ import annotations

NIGERIAN_FEEDS: dict[str, str] = {
    "Punch": "https://punchng.com/feed/",
    "Vanguard": "https://www.vanguardngr.com/feed/",
    "The Sun": "https://sunnewsonline.com/feed/",
    "Channels TV": "https://www.channelstv.com/feed/",
    "Arise TV": "https://www.arise.tv/feed/",
    "Premium Times": "https://www.premiumtimesng.com/feed",
    "The Cable": "https://www.thecable.ng/feed",
    "Guardian Nigeria": "https://guardian.ng/category/news/feed/",
    "Daily Trust": "https://dailytrust.com/feed/",
    "Sahara Reporters": "https://saharareporters.com/articles/rss-feed",
}

GLOBAL_TECH_FEEDS: dict[str, str] = {
    "TechCrunch": "https://techcrunch.com/feed",
    "Hacker News": "https://news.ycombinator.com/rss",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "TechCabal": "https://techcabal.com/feed/",
}

KEYWORDS: list[str] = [
    "politics",
    "government",
    "security",
    "insecurity",
    "attack",
    "kidnap",
    "economy",
    "reform",
    "subsidy",
    "inec",
    "president",
    "senate",
    "assembly",
    "military",
    "bandit",
    "terror",
    "poverty",
    "health",
    "education",
    "ai",
    "llm",
    "developer",
    "software",
    "startup",
    "tech",
]

FEED_TIMEOUT_SECONDS = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; NigeriaTechDigest/1.0)"
ENTRIES_PER_FEED = 8
MAX_ARTICLES_FOR_AI = 25
SUMMARY_TRUNCATE_CHARS = 200
MAX_OUTPUT_TOKENS = 8192
GEMINI_MODEL = "gemini-2.5-flash"

TIME_WINDOWS_HOURS: dict[str, int] = {
    "morning": 14,
    "evening": 11,
}

ARCHIVE_PRUNE_DAYS = 90
MIN_ARTICLES_FOR_DIGEST = 5

DIGEST_PROMPT_TEMPLATE = """You are a senior Nigeria policy analyst and global tech strategist.

Using ONLY the articles provided, produce a markdown report with:

## Governance & Politics (Nigeria)
## Security & Insecurity (Nigeria)
## National Progress & Economy (Nigeria)
## Global Tech, AI & Software Engineering
## Outlook & Speculation

For each section:
- Cover up to **4 stories max** (prioritize quality over quantity).
- For the **top 2 most significant** stories in each section, include:
  - **Headline** (with source)
  - **What happened** (2 sentences, factual)
  - **Deep Lore / Context** (1 concise paragraph: background, escalation, why it matters)
  - **Source:** [link]
- For any additional stories (3rd–4th), include only:
  - **Headline**, **What happened** (1 sentence), **Brief Context** (1 sentence), **Source**

## Outlook & Speculation
- 3–5 bullet points on likely next directions across categories.
- Present multiple perspectives where debate exists; label speculation clearly.

Rules:
- Be objective; separate fact from speculation.
- If a section has no fresh stories, say "No major updates in this window."
- Do not invent events not present in the input.
- Prioritize stories that signal future direction (policy shifts, security trends, tech adoption).

Raw articles (JSON):
{articles_json}
"""

TRUNCATION_NOTICE = """

---

> **Note:** This digest was cut short because the AI hit its output limit. Later sections may be missing. Check the GitHub Pages archive for the saved copy, or wait for the next scheduled brief.
"""

FALLBACK_HEADLINES_TEMPLATE = """# Nigeria & Tech Brief — Headlines Only

AI summarization was unavailable (rate limit). Here are the top headlines from this window:

{headlines}
"""
