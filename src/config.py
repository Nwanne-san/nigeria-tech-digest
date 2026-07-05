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
    "Techpoint Africa": "https://techpoint.africa/feed/",
    "Nairametrics": "https://nairametrics.com/feed/",
    "BusinessDay": "https://businessday.ng/feed/",
    "Condia": "https://www.benjamindada.com/rss/",
}

GLOBAL_TECH_FEEDS: dict[str, str] = {
    "TechCrunch": "https://techcrunch.com/feed",
    "Hacker News": "https://news.ycombinator.com/rss",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "MIT Tech Review": "https://www.technologyreview.com/feed/",
    "TechCabal": "https://techcabal.com/feed/",
    "TypeScript Blog": "https://devblogs.microsoft.com/typescript/feed/",
    "JavaScript Weekly": "https://javascriptweekly.com/rss",
    "AWS News": "https://aws.amazon.com/blogs/aws/feed/",
    "Google Cloud Blog": "https://cloudblog.withgoogle.com/rss/",
    "Simon Willison (AI)": "https://simonwillison.net/atom/everything/",
    "The New Stack": "https://thenewstack.io/feed/",
}

# Keyword -> ranking weight. Career/stack terms outweigh generic policy terms
# so stories relevant to a web/TypeScript/cloud/AI engineer surface first.
KEYWORDS: dict[str, float] = {
    # Career & stack (highest priority)
    "typescript": 4.0,
    "javascript": 3.5,
    "react": 3.5,
    "next.js": 3.5,
    "node.js": 3.0,
    "frontend": 3.0,
    "web development": 3.0,
    "software engineer": 3.5,
    "developer": 3.0,
    "open source": 2.5,
    "ai": 4.0,
    "artificial intelligence": 4.0,
    "llm": 4.0,
    "machine learning": 3.5,
    "openai": 3.5,
    "anthropic": 3.5,
    "gemini": 3.0,
    "chatgpt": 3.0,
    "cloud": 3.5,
    "aws": 3.5,
    "azure": 3.0,
    "google cloud": 3.0,
    "serverless": 3.0,
    "devops": 3.0,
    "cybersecurity": 3.0,
    # Nigerian tech ecosystem
    "fintech": 3.5,
    "startup": 3.0,
    "paystack": 3.5,
    "flutterwave": 3.5,
    "moniepoint": 3.0,
    "funding": 2.5,
    "remote work": 3.0,
    "cbn": 3.0,
    "naira": 2.5,
    "tech": 2.0,
    "software": 2.5,
    # Nigeria governance, security, economy
    "politics": 2.0,
    "government": 2.0,
    "security": 2.0,
    "insecurity": 2.0,
    "attack": 2.0,
    "kidnap": 2.0,
    "economy": 2.0,
    "reform": 2.0,
    "subsidy": 2.0,
    "inec": 2.0,
    "president": 2.0,
    "senate": 2.0,
    "assembly": 2.0,
    "military": 2.0,
    "bandit": 2.0,
    "terror": 2.0,
    "poverty": 2.0,
    "health": 2.0,
    "education": 2.0,
}

FEED_TIMEOUT_SECONDS = 30.0
USER_AGENT = "Mozilla/5.0 (compatible; NigeriaTechDigest/1.0)"
ENTRIES_PER_FEED = 8
MAX_ARTICLES_FOR_AI = 40
SUMMARY_TRUNCATE_CHARS = 800
MAX_OUTPUT_TOKENS = 16384
GEMINI_MODEL = "gemini-2.5-flash"
# Tried in order after GEMINI_MODEL; flash-lite has its own free-tier quota on the same key
GEMINI_FALLBACK_MODELS: list[str] = ["gemini-2.5-flash-lite"]

# Optional OpenAI-compatible fallbacks, used only when their env key is set.
# (env_var, endpoint, model)
OPENAI_COMPAT_FALLBACKS: list[tuple[str, str, str]] = [
    ("CEREBRAS_API_KEY", "https://api.cerebras.ai/v1/chat/completions", "llama-3.3-70b"),
    ("GROQ_API_KEY", "https://api.groq.com/openai/v1/chat/completions", "llama-3.3-70b-versatile"),
]

TIME_WINDOWS_HOURS: dict[str, int] = {
    "morning": 14,
    "evening": 11,
}

ARCHIVE_PRUNE_DAYS = 90
MIN_ARTICLES_FOR_DIGEST = 5

READER_PERSONA = """The reader is a Nigerian web developer (TypeScript, React/Node, cloud platforms) actively growing into AI engineering. They care about: Nigeria's direction (governance, security, economy), the Nigerian tech ecosystem (startups, fintech, CBN policy, funding, remote work), and staying sharp on their stack (TypeScript, web, cloud, AI/LLMs)."""

SLOT_INSTRUCTIONS: dict[str, str] = {
    "morning": """This is the MORNING brief. Be forward-looking: frame stories around "what to watch today", flag developing situations, and note anything the reader should track during the workday.""",
    "evening": """This is the EVENING brief. Be reflective: frame stories around "what happened and what it means", connect the day's events to ongoing trends, and close loops on stories from earlier.""",
}

DIGEST_PROMPT_TEMPLATE = """You are a senior Nigeria policy analyst and global tech strategist writing a personal briefing.

{persona}

{slot_instructions}

Using ONLY the articles provided, produce a markdown report with:

## Governance & Politics (Nigeria)
## Security & Insecurity (Nigeria)
## National Progress & Economy (Nigeria)
## Global Tech, AI & Software Engineering
## Career Radar
## Outlook & Speculation

For the first four sections:
- Cover up to **4 stories max** (prioritize quality over quantity).
- For the **top 2 most significant** stories in each section, include:
  - **Headline** (with source)
  - **What happened** (2 sentences, factual)
  - **Deep Lore / Context** (1 concise paragraph: background, escalation, why it matters)
  - **Source:** [link]
- For any additional stories (3rd–4th), include only:
  - **Headline**, **What happened** (1 sentence), **Brief Context** (1 sentence), **Source**

## Career Radar
- 3–5 bullets connecting this window's news directly to the reader's career.
- Each bullet: the signal (from a provided article), then "→" and what it means for a Nigerian web/cloud/AI engineer (a skill to watch, an opportunity, a risk, a tool worth trying).
- Ground every bullet in the provided articles; do not invent trends.

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

WEEKLY_PROMPT_TEMPLATE = """You are a career strategist and Nigeria analyst writing a Sunday weekly synthesis.

{persona}

Input: the past week's daily digest briefings (markdown, dated). Synthesize across the whole week — do not just repeat individual digests.

Produce a markdown report with:

## The Week in Nigeria
- 3–5 major storylines with their trajectory across the week (escalating, resolving, stalled).

## The Week in Tech & AI
- 3–5 storylines most relevant to the reader's stack and the Nigerian/African tech ecosystem.

## Career Actions
- 3–5 concrete, specific actions for the coming week (a skill to study, a tool to try, a trend to position for, an ecosystem shift to act on). Base each on evidence from the week's digests.

## Watchlist for Next Week
- 3–5 things likely to develop next week and why they matter.

Rules:
- Synthesize trends; cite the day a story appeared when useful.
- Do not invent events not present in the input.
- Be direct and practical in Career Actions — the reader wants leverage, not platitudes.

Past week's digests:
{digests}
"""

TRUNCATION_NOTICE = """

---

> **Note:** This digest was cut short because the AI hit its output limit. Later sections may be missing. Check the GitHub Pages archive for the saved copy, or wait for the next scheduled brief.
"""

FALLBACK_HEADLINES_TEMPLATE = """# Nigeria & Tech Brief — Headlines Only

AI summarization was unavailable (rate limit). Here are the top headlines from this window:

{headlines}
"""
