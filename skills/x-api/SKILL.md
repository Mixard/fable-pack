---
name: x-api
description: Use when interacting with the X (Twitter) API programmatically - posting tweets, threads, media, reading timelines, or searching. Covers v2 endpoints, the v1.1 media upload endpoint, OAuth 1.0a vs Bearer token rules, reply/thread payload shapes, rate-limit headers, and error handling.
---

# X (Twitter) API

Base URL for v2: `https://api.x.com/2`. Media upload still lives on v1.1: `https://upload.twitter.com/1.1/media/upload.json`.

## Authentication

Two schemes; the choice is dictated by the operation, not preference:

- **OAuth 2.0 Bearer token (app-only)** — read-only public data: search, timelines, user lookup.
- **OAuth 1.0a (user context)** — required for every write: posting tweets, media upload, DMs, account management.

```bash
export X_BEARER_TOKEN="..."
# OAuth 1.0a credentials:
export X_CONSUMER_KEY="..."
export X_CONSUMER_SECRET="..."
export X_ACCESS_TOKEN="..."
export X_ACCESS_TOKEN_SECRET="..."
```

Legacy env names (`X_API_KEY`, `X_API_SECRET`, `X_ACCESS_SECRET`) may exist in older setups; prefer the `X_CONSUMER_*` / `X_ACCESS_TOKEN_SECRET` names for new wiring. Tokens are regenerated at developer.x.com.

```python
import os
import requests
from requests_oauthlib import OAuth1Session

bearer_headers = {"Authorization": f"Bearer {os.environ['X_BEARER_TOKEN']}"}

oauth = OAuth1Session(
    os.environ["X_CONSUMER_KEY"],
    client_secret=os.environ["X_CONSUMER_SECRET"],
    resource_owner_key=os.environ["X_ACCESS_TOKEN"],
    resource_owner_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)
```

## Posting

`POST https://api.x.com/2/tweets` (OAuth 1.0a). Success status is **201**; tweet ID at `resp.json()["data"]["id"]`.

```python
resp = oauth.post("https://api.x.com/2/tweets", json={"text": "Hello"})
tweet_id = resp.json()["data"]["id"]
```

Reply payload shape (also how threads are chained):

```json
{"text": "...", "reply": {"in_reply_to_tweet_id": "<tweet_id>"}}
```

Thread = sequential posts, each replying to the previous ID:

```python
def post_thread(oauth, tweets: list[str]) -> list[str]:
    ids, reply_to = [], None
    for text in tweets:
        payload = {"text": text}
        if reply_to:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to}
        resp = oauth.post("https://api.x.com/2/tweets", json=payload)
        reply_to = resp.json()["data"]["id"]
        ids.append(reply_to)
    return ids
```

## Media upload

Two steps: upload via **v1.1**, then reference the media ID in a **v2** post. Use `media_id_string` (not the numeric `media_id` — JSON precision loss).

```python
media_resp = oauth.post(
    "https://upload.twitter.com/1.1/media/upload.json",
    files={"media": open("image.png", "rb")},
)
media_id = media_resp.json()["media_id_string"]

resp = oauth.post(
    "https://api.x.com/2/tweets",
    json={"text": "Check this out", "media": {"media_ids": [media_id]}},
)
```

## Reading (Bearer token)

Search recent tweets — `GET https://api.x.com/2/tweets/search/recent`:

```python
resp = requests.get(
    "https://api.x.com/2/tweets/search/recent",
    headers=bearer_headers,
    params={
        "query": "from:someuser -is:retweet -is:reply",  # standard operators
        "max_results": 25,
        "tweet.fields": "created_at,public_metrics",
    },
)
```

User timeline — `GET https://api.x.com/2/users/{user_id}/tweets`:

```python
resp = requests.get(
    f"https://api.x.com/2/users/{user_id}/tweets",
    headers=bearer_headers,
    params={"max_results": 10, "tweet.fields": "created_at,public_metrics"},
)
```

User lookup — `GET https://api.x.com/2/users/by/username/{username}`:

```python
resp = requests.get(
    "https://api.x.com/2/users/by/username/someuser",
    headers=bearer_headers,
    params={"user.fields": "public_metrics,description,created_at"},
)
```

Expansion params (`tweet.fields`, `user.fields`) are comma-separated; without them responses contain only `id` and `text`. Engagement counts come back under `public_metrics`.

## Rate limits

Limits vary by endpoint, auth method, and account tier, and change over time — read them from response headers instead of hardcoding tables:

- `x-rate-limit-remaining` — requests left in the window
- `x-rate-limit-reset` — window reset time (Unix timestamp)
- `x-rate-limit-limit` — window cap

```python
import time

remaining = int(resp.headers.get("x-rate-limit-remaining", 0))
if remaining < 5:
    reset = int(resp.headers.get("x-rate-limit-reset", 0))
    wait = max(0, reset - int(time.time()))
    # back off for `wait` seconds
```

## Error handling

```python
resp = oauth.post("https://api.x.com/2/tweets", json={"text": content})
if resp.status_code == 201:
    tweet_id = resp.json()["data"]["id"]
elif resp.status_code == 429:
    reset = int(resp.headers["x-rate-limit-reset"])   # rate limited; retry after reset
elif resp.status_code == 403:
    detail = resp.json().get("detail")  # permissions: app lacks write access, duplicate tweet, etc.
else:
    raise Exception(f"X API error {resp.status_code}: {resp.text}")
```

Common cases: 401 = bad/expired credentials or wrong auth scheme for the endpoint (e.g. Bearer on a write); 403 = app permission level (read-only app trying to post) or duplicate content; 429 = rate limit, honor `x-rate-limit-reset`. v2 error bodies carry `title`, `detail`, and `errors[]`.
