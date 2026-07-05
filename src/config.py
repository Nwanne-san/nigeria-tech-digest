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
    "BBC Africa": "https://feeds.bbci.co.uk/news/world/africa/rss.xml",
    "The Africa Report": "https://www.theafricareport.com/feed/",
    "Semafor": "https://www.semafor.com/rss.xml",
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
    "Rest of World": "https://restofworld.org/feed/latest/",
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
# Top-ranked articles get full text fetched for deeper AI context (Gemini only;
# smaller fallback models receive the compact summaries-only prompt)
FULL_TEXT_TOP_N = 10
FULL_TEXT_MAX_CHARS = 6000
MAX_OUTPUT_TOKENS = 32768
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

Ongoing storylines you have been tracking across previous digests (JSON; may be empty):
{storylines_json}

When a fresh article continues one of these storylines, explicitly reference the continuity (e.g., "third escalation this month", "follows last week's announcement") instead of treating it as a new event.

Using ONLY the articles provided, produce a markdown report with:

## Governance & Politics (Nigeria)
## Security & Insecurity (Nigeria)
## National Progress & Economy (Nigeria)
## Global Tech, AI & Software Engineering
## Career Radar
## Outlook & Speculation

For the first four sections:
- Cover up to **6 stories** per section when the material supports it.
- For the **top 3 most significant** stories in each section, include:
  - **Headline** (with source)
  - **What happened** (3–5 sentences, factual — include the concrete figures, names, places, and quotes from the articles)
  - **Deep Lore / Context** (2 substantial paragraphs: the background and how we got here; the actors and their incentives; the escalation history; why it matters and what it connects to)
  - **Source:** [link]
- For any additional stories (4th–6th), include:
  - **Headline**, **What happened** (2–3 sentences), **Context** (2–3 sentences), **Source**

## Career Radar
- 4–6 bullets connecting this window's news directly to the reader's career.
- Each bullet: the signal (from a provided article), then "→" and 2–3 sentences on what it means for a Nigerian web/cloud/AI engineer (a skill to watch, an opportunity, a risk, a tool worth trying) and a suggested first step.
- Ground every bullet in the provided articles; do not invent trends.

## Outlook & Speculation
- 5–7 bullet points on likely next directions across categories, each 2–3 sentences.
- Present multiple perspectives where debate exists; label speculation clearly.

Rules:
- Aim for roughly 2,500–3,500 words total. Do NOT compress for brevity — depth and specificity are preferred over summarization. Never reduce a story to a single vague sentence when the source material contains detail.
- Be objective; separate fact from speculation.
- If a section has no fresh stories, say "No major updates in this window."
- Do not invent events not present in the input.
- Prioritize stories that signal future direction (policy shifts, security trends, tech adoption).

Raw articles (JSON):
{articles_json}
"""

WEEKLY_PROMPT_TEMPLATE = """You are a career strategist and Nigeria analyst writing a twice-weekly synthesis (published Sundays and Wednesdays).

{persona}

Input: the daily digest briefings since the last synthesis (markdown, dated). Synthesize across the whole period — do not just repeat individual digests.

Produce a markdown report with:

## Nigeria: The Big Picture
- 4–6 major storylines, each with a full paragraph: trajectory across the period (escalating, resolving, stalled), the key developments day by day, and what the pattern reveals.

## Tech & AI: The Big Picture
- 4–6 storylines most relevant to the reader's stack and the Nigerian/African tech ecosystem, each a full paragraph with the specifics.

## Career Actions
- 4–6 concrete, specific actions for the days ahead (a skill to study, a tool to try, a trend to position for, an ecosystem shift to act on). For each: the evidence from the digests, the action, and a concrete first step — 2–4 sentences.

## Watchlist
- 4–6 things likely to develop before the next synthesis, each with 2–3 sentences on why it matters and what signal to look for.

Rules:
- Aim for roughly 1,500–2,500 words. Depth over compression — the daily digests already summarized; your job is connection and detail, not further shortening.
- Synthesize trends; cite the day a story appeared when useful.
- Do not invent events not present in the input.
- Be direct and practical in Career Actions — the reader wants leverage, not platitudes.

Digests since the last synthesis:
{digests}
"""

STORYLINE_UPDATE_PROMPT = """You maintain a compact tracker of ongoing news storylines for a personal digest.

Current storylines (JSON array; may be empty):
{storylines_json}

Today's digest ({date}):
{digest_md}

Update the tracker:
- Merge today's developments into existing storylines (update summary, status, last_updated).
- Add genuinely new multi-day storylines (policy sagas, security situations, tech/AI shifts, Nigerian ecosystem trends). Skip one-off events unlikely to develop further.
- Drop storylines dormant for more than 21 days.
- Keep at most 15 storylines.

Return ONLY a JSON array of objects with exactly these fields:
- "name": short storyline title
- "status": one of "escalating", "developing", "resolving", "dormant"
- "summary": 1-2 sentences of current state and trajectory
- "last_updated": ISO date of the latest development
"""

MONTHLY_PROMPT_TEMPLATE = """You are a strategist writing a monthly retrospective for a personal news digest.

{persona}

Input: a full month of daily digest briefings (markdown, dated).

Produce a markdown report with:

## What Actually Changed in Nigeria
- The 4-6 developments from this month that will still matter in a year. For each: a full paragraph on what shifted, the evidence across the month, and the trajectory.

## What Actually Changed in Tech & AI
- The 4-6 developments most relevant to the reader's stack and the Nigerian/African tech ecosystem, each a full paragraph with specifics.

## Announcements vs Follow-Through
- Which government or industry announcements from this month showed real follow-through, and which fizzled — with the dates and details for each.

## What Deserved More Attention
- 2-3 underweighted stories the reader should revisit, each with a paragraph on why it matters more than the coverage suggested.

## Positioning for Next Month
- 4-6 concrete career or attention recommendations based on the month's trends, each with the evidence and a first step.

Rules:
- Aim for roughly 2,000–3,000 words. Depth over compression — this is the one report of the month, so be thorough.
- Synthesize across the month; do not summarize digest by digest.
- Do not invent events not present in the input.
- Be candid about uncertainty and label speculation.

The month's digests:
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
