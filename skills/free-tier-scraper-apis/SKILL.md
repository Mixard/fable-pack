---
name: free-tier-scraper-apis
description: Use when building zero-cost scraping or data-enrichment pipelines on free API tiers. Covers Gemini free-tier model IDs and rate limits, the generativelanguage REST endpoint and payload, Notion API property JSON shapes, model fallback, and scraping-method choice.
---

# Free-Tier APIs for Scraper Pipelines

Reference for the common free stack: `requests`/BeautifulSoup or Playwright for collection, Gemini free tier for enrichment, Notion API for storage.

## Gemini free tier

Model IDs and free-tier limits (API key from AI Studio, no billing):

| Model | RPM | RPD |
|---|---|---|
| `gemini-2.0-flash-lite` | 30 | 1500 |
| `gemini-2.0-flash` | 15 | 1500 |
| `gemini-2.5-flash` | 10 | 500 |
| `gemini-flash-lite-latest` | alias, tracks current flash-lite | - |

### REST endpoint

```
POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}
```

Payload for JSON-out enrichment:

```json
{
  "contents": [{"parts": [{"text": "your prompt"}]}],
  "generationConfig": {
    "responseMimeType": "application/json",
    "temperature": 0.3,
    "maxOutputTokens": 2048
  }
}
```

Response text lives at `candidates[0].content.parts[0].text`. Even with `responseMimeType: application/json` some models wrap output in ` ```json ` fences; strip them before `json.loads`. Keep `maxOutputTokens` at 2048+ for batch responses, otherwise truncated JSON fails to parse.

### Fallback chain and batching

- On HTTP 429 (quota) or 404 (model retired), retry the same prompt on the next model: `gemini-2.0-flash-lite -> gemini-2.0-flash -> gemini-2.5-flash -> gemini-flash-lite-latest`. Model IDs churn; the `-latest` alias survives retirements.
- Batch items into one prompt (about 5 per call, response as `{"analyses": [...]}` in input order) instead of one call per item; per-item calls exhaust RPM immediately.
- Self-throttle: ~7 s between calls stays under 10 RPM, safe for every model in the chain.

## Notion API property shapes

Writing rows via `pages.create(parent={"database_id": db_id}, properties=...)`. Each property type has its own JSON wrapper:

```json
{
  "Name":       {"title": [{"text": {"content": "Item name"}}]},
  "Summary":    {"rich_text": [{"text": {"content": "text, max 2000 chars per block"}}]},
  "URL":        {"url": "https://example.com/item"},
  "Status":     {"select": {"name": "New"}},
  "Tags":       {"multi_select": [{"name": "backend"}, {"name": "remote"}]},
  "Score":      {"number": 87},
  "Date Found": {"date": {"start": "2026-07-21"}},
  "Done":       {"checkbox": true}
}
```

Gotchas:
- `title` and `rich_text` are arrays of blocks; a single `text.content` block is capped at 2000 characters — truncate before writing.
- `select`/`multi_select` options are auto-created on write if the `name` is new.
- Reading back: a `url` property is at `page["properties"]["URL"]["url"]`; title text at `["Name"]["title"][0]["plain_text"]`.
- `databases.query` paginates at `page_size` max 100; loop with `start_cursor` = `next_cursor` while `has_more`. Query all existing URLs first to deduplicate before pushing.

## BeautifulSoup vs Playwright

Start with `requests` + BeautifulSoup (`lxml` parser) — it covers most public sites at zero overhead. If the response HTML is empty or missing the data, the page is JS-rendered: first check DevTools for the underlying JSON API the page calls (scraping that is faster and more stable), and only fall back to Playwright (`page.goto` + `wait_for_selector` + `page.content()`, then parse with BeautifulSoup) when no API exists. Playwright in CI needs a browser install step (`python -m playwright install chromium --with-deps`).
