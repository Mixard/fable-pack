---
name: uspto-database
description: Use when querying official US patent or trademark records — granted patents, pre-grant publications, application status, assignments, or trademark status via USPTO systems. Covers the PatentSearch (PatentsView) API v1 with its JSON query DSL and X-Api-Key header, TSDR trademark retrieval, ODP file-wrapper search, and the environment-variable auth conventions.
---

# USPTO Database

Use this skill when a task needs official United States patent or trademark records. This is a data-gathering and record-verification workflow — do not use it to give legal advice.

## When to Use

- Searching granted patents or pre-grant publications
- Checking patent application status, file-wrapper data, assignments, or prosecution history
- Looking up trademark status, documents, or assignment history
- Building reproducible prior-art, portfolio, or IP-landscape research

## Source Selection

Prefer official USPTO or USPTO-supported surfaces first:

- **Open Data Portal (ODP)** — current home for migrated USPTO datasets and APIs
- **Patent File Wrapper** — public patent application bibliographic and file-wrapper records
- **PatentSearch API** — PatentsView search API for granted patents and pre-grant publications
- **TSDR Data API** — trademark status and document retrieval
- **Patent and Trademark Assignment Search** — ownership transfer records
- **PTAB data in ODP** — Patent Trial and Appeal Board proceedings

Use secondary sources (Google Patents, Lens.org) only as convenience indexes; cross-check the official record when the answer matters.

## Authentication

Many USPTO API flows require an API key. Store keys in environment variables or a secret manager.

```bash
export USPTO_API_KEY="..."
export PATENTSVIEW_API_KEY="..."
```

For PatentSearch, send the key with the `X-Api-Key` header. For TSDR, follow the current USPTO API Manager instructions and rate-limit guidance.

## PatentSearch Workflow

Use PatentSearch for broad patent and pre-grant publication search — trends, inventors, assignees, classifications, dates, or portfolio slices.

Base URL: `https://search.patentsview.org/api/v1`

The query body uses a JSON DSL: `q` is the filter (with operators `_and`, `_or`, `_not`, `_gte`, `_lte`, `_text_any`, `_text_all`, `_text_phrase`), `f` is the returned-field list, `s` is the sort spec, and `o` holds options like `per_page` and `page`.

```python
import os, requests

API_KEY = os.environ["PATENTSVIEW_API_KEY"]
BASE = "https://search.patentsview.org/api/v1"

payload = {
    "q": {
        "_and": [
            {"patent_date": {"_gte": "2024-01-01"}},
            {"assignees.assignee_organization": {"_text_any": ["Google", "Alphabet"]}},
        ]
    },
    "f": ["patent_id", "patent_title", "patent_date"],
    "s": [{"patent_date": "desc"}],
    "o": {"per_page": 100, "page": 1},
}

response = requests.post(
    f"{BASE}/patent/",
    headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
    json=payload,
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

Verify current endpoint names, field paths, and request parameters in the live PatentSearch docs before reusing a query.

## Trademark / TSDR Workflow

Use TSDR when the task needs trademark case status, documents, images, owner history, or prosecution events.

1. Normalize the serial number or registration number.
2. Check the current TSDR API instructions and required API-key header.
3. Fetch status first, then documents only if needed.
4. Respect the lower rate limit for PDF, ZIP, and multi-case downloads.

For large trademark pulls, prefer documented bulk-data flows rather than screen-scraping public pages.

## File Wrapper and Assignments

For application status, transaction history, and prosecution documents, start with ODP Patent File Wrapper search using exact identifiers (application number, publication number, patent number, or party name). Record whether the record is a granted patent, pre-grant publication, or pending application.

For ownership, search official assignment data by patent/application/registration number, assignor, assignee, or reel/frame. Record conveyance text, execution date, recordation date, and parties. Distinguish assignment records from current legal-ownership conclusions; if ownership is material, flag for attorney review.

## References

- USPTO APIs catalog: https://developer.uspto.gov/api-catalog
- USPTO Open Data Portal: https://data.uspto.gov/
- PatentSearch API reference: https://search.patentsview.org/docs/docs/Search%20API/SearchAPIReference/
- TSDR API bulk download FAQ: https://developer.uspto.gov/faq/tsdr-api-bulk-download
