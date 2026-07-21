---
name: n8n-selfhosted-ops
description: Use when operating a self-hosted n8n instance (npm/systemd, no Docker) - importing workflows via CLI without an API key, exposing env vars to workflow expressions, credential re-linking after import, and the Telegram human-in-the-loop pattern that avoids the broken sendAndWait node. Verified on n8n 2.8.
---

# Self-hosted n8n operations

Verified on n8n 2.8 (global npm install, systemd service, sqlite backend). The facts
below are the ones models reliably get wrong: they assume the REST API is the only
import path, that .env files load automatically, and that sendAndWait works.

## Workflow import without an API key

`n8n import:workflow --input=/path/to/workflow.json` writes directly into the sqlite
DB, bypassing the REST API entirely - no API key, no running UI session needed.
Safe to run repeatedly: the command also applies pending DB migrations on start.
Success output: `Successfully imported N workflow(s).`

- List workflows and recover IDs: `n8n list:workflow` (returns `ID|Name` rows).
- Gotcha: running import via `sudo -u OTHER_USER` fails with `EACCES` when the JSON
  is root-owned mode 600. Keep the file readable or run as the service user.

## Env vars in workflow expressions

n8n does NOT read a project `.env` automatically. For `{{$env.FOO}}` to resolve,
the variable must be in the service environment. With systemd:

```
sudo systemctl edit n8n
# add:
[Service]
EnvironmentFile=/path/to/.env
# then:
systemctl daemon-reload && systemctl restart n8n
```

## Credentials are never exported

Workflow JSON exports reference credentials by ID only - the secrets themselves are
not in the file. After importing to another instance, every credentialed node points
at a dangling ID. The user must create each credential in the UI (Settings >
Credentials > New) and re-link it in each node. This cannot be automated via CLI;
plan for it in migration instructions instead of promising a turnkey import.

## Webhook URLs

Public format: `{N8N_WEBHOOK_URL}/webhook/{path}` with `path` from the Webhook node.
Meta, Google Business Profile, and Telegram all reject plain HTTP callbacks -
a reverse proxy with TLS (or n8n's built-in SSL config) is a hard prerequisite.

## Telegram human-in-the-loop: do not use sendAndWait

`Telegram.sendAndWait` has long-standing bugs (n8n issues #13331, #15492). Working
pattern:

1. `Telegram: sendMessage` with an `inline_keyboard` whose button URLs embed the
   execution resume URL: `{{$execution.resumeUrl}}?answer=approve` / `?answer=reject`.
2. A `Wait` node in `webhook` mode listens on that resume URL.
3. Downstream nodes read the choice from `$json.query.answer`.

For dynamic inline keyboards (button list built at runtime), the native Telegram node
cannot express them - call `https://api.telegram.org/bot{token}/sendMessage` directly
with an HTTP Request node and build `reply_markup` yourself.
