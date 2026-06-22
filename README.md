# Nigeria & Tech Daily Digest

Twice-daily automated briefing on Nigerian governance, politics, security, national progress, and global tech — delivered to your inbox and archived on GitHub Pages.

**Schedule:** 8:00 AM and 7:00 PM WAT (West Africa Time)

## Features

- Aggregates **17 RSS feeds** (10 Nigerian outlets + 6 global tech sources + TechCabal)
- AI summaries with **tiered lore** (deep context for top 3 stories per section)
- Email delivery via **Resend** (free plan)
- **GitHub Pages** archive of all past digests
- Runs on **GitHub Actions** — $0/month on free tiers

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/nigeria-tech-digest.git
cd nigeria-tech-digest
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

| Variable | Value |
|----------|-------|
| `GEMINI_API_KEY` | From [Google AI Studio](https://aistudio.google.com/) (free tier, billing off) |
| `RESEND_API_KEY` | From [Resend](https://resend.com/) dashboard |
| `DIGEST_FROM_EMAIL` | `onboarding@resend.dev` |
| `DIGEST_TO_EMAIL` | `nnamaninwanne@gmail.com` |

### 3. Validate feeds

```bash
python -m src.validate_feeds
```

### 4. Run locally

```bash
export $(grep -v '^#' .env | xargs)
DIGEST_SLOT=morning python -m src.main
```

## GitHub Actions setup

1. Create a **public** GitHub repo and push this project.
2. Add these **repository secrets** (Settings → Secrets → Actions):

| Secret | Value |
|--------|-------|
| `GEMINI_API_KEY` | Google AI Studio API key |
| `RESEND_API_KEY` | Resend API key |
| `DIGEST_FROM_EMAIL` | `onboarding@resend.dev` |
| `DIGEST_TO_EMAIL` | `nnamaninwanne@gmail.com` |

3. **Resend account setup** (one-time):
   - Sign up at [resend.com](https://resend.com/) with `nnamaninwanne@gmail.com`
   - Verify email → API Keys → Create key
   - No custom domain needed on free plan

4. Trigger **workflow_dispatch** manually to test before cron runs.

5. Enable **GitHub Pages**: Settings → Pages → Source: **GitHub Actions**.

Archive URL: `https://YOUR_USERNAME.github.io/nigeria-tech-digest/`

## Project structure

```
src/
  config.py       # Feeds, keywords, prompts
  fetcher.py      # RSS aggregation
  brain.py        # Gemini summarization
  emailer.py      # Resend delivery
  archive.py      # GitHub Pages archive
  state.py        # Deduplication state
  main.py         # Orchestrator
docs/
  index.html      # Archive homepage
  archive/        # Past digests (.md + .html)
data/
  seen_articles.json
```

## Free-tier notes

- **Gemini:** 2 API calls/day fits free tier; no billing enabled
- **Resend:** 60 emails/month on free plan; `onboarding@resend.dev` only sends to your account email
- **GitHub Actions:** Unlimited on public repos (~120 min/month actual usage)
- **GitHub Pages:** Free on public repos

## License

MIT
