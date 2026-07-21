---
name: pubmed-database
description: Use when searching biomedical literature via PubMed or NCBI E-utilities — MeSH queries, PMID lookup, abstract/citation retrieval, or API-backed literature monitoring. Covers PubMed field tags, publication-type and date filters, MeSH subheading syntax, and the E-utilities REST endpoints with a working Python request pattern.
---

# PubMed Database

Use this skill when a task needs biomedical literature from PubMed rather than general web search.

## When to Use

- Searching MEDLINE or life-sciences literature
- Building PubMed queries with MeSH terms, field tags, dates, or article types
- Looking up PMIDs, abstracts, publication metadata, or related citations
- Using NCBI E-utilities directly from Python, shell, or another HTTP client

## Query Construction

Combine concepts with Boolean operators (`AND`, `OR`, `NOT`).

### PubMed field tags

- `[ti]`: title
- `[ab]`: abstract
- `[tiab]`: title or abstract
- `[au]`: author
- `[ta]`: journal title abbreviation
- `[mh]`: MeSH term
- `[majr]`: major MeSH topic
- `[pt]`: publication type
- `[dp]`: date of publication
- `[la]`: language
- `[nm]`: substance name

Examples:

```text
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2026[dp]
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]
smith ja[au] AND cancer[tiab] AND 2026[dp] AND english[la]
```

## MeSH and Subheadings

Prefer MeSH when the concept has a stable controlled-vocabulary term. Combine MeSH with title/abstract terms when the topic is new or terminology varies.

Correct subheading syntax puts the subheading before the field tag:

```text
diabetes mellitus, type 2/drug therapy[mh]
cardiovascular diseases/prevention & control[mh]
```

Use `[majr]` only when the topic must be central to the paper — improves precision but may miss relevant work.

## Filters

Publication types:

```text
clinical trial[pt]
meta-analysis[pt]
randomized controlled trial[pt]
review[pt]
systematic review[pt]
guideline[pt]
```

Date filters:

```text
2026[dp]
2020:2026[dp]
2026/03/15[dp]
```

Availability filters:

```text
free full text[sb]
hasabstract[text]
```

## E-utilities Workflow

Base URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`

1. `esearch.fcgi`: search and return PMIDs
2. `esummary.fcgi`: return lightweight article metadata
3. `efetch.fcgi`: fetch abstracts or full records in XML, MEDLINE, or text
4. `elink.fcgi`: find related articles and linked resources

Provide `email` and, for higher rate limits, `api_key`. Store API keys in environment variables. Default rate limit is 3 requests/sec without a key, 10/sec with one.

```python
import os, time, requests

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def esearch(query: str, retmax: int = 20) -> list[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
        "tool": "my-pubmed-search",
        "email": os.environ.get("NCBI_EMAIL", ""),
    }
    api_key = os.environ.get("NCBI_API_KEY")
    if api_key:
        params["api_key"] = api_key

    response = requests.get(f"{BASE}/esearch.fcgi", params=params, timeout=30)
    response.raise_for_status()
    time.sleep(0.35)  # respect rate limit
    return response.json()["esearchresult"]["idlist"]

pmids = esearch("hypertension[mh] AND randomized controlled trial[pt] AND 2024:2026[dp]")
```

For batches, prefer NCBI history-server parameters (`usehistory=y`, `WebEnv`, `query_key`) instead of passing very long PMID lists through URLs.

## References

- PubMed help: https://pubmed.ncbi.nlm.nih.gov/help/
- NCBI E-utilities documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- NCBI API key guidance: https://support.nlm.nih.gov/kbArticle/?pn=KA-05317
