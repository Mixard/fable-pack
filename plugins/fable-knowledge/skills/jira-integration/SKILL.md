---
name: jira-integration
description: Use when reading, searching, commenting on, or transitioning Jira issues via MCP or the REST API v3. Covers mcp-atlassian config, tool names, curl examples, the ADF comment schema, JQL patterns, and error troubleshooting.
---

# Jira Integration

Two access paths: the `mcp-atlassian` MCP server (exposes Jira as tools) or direct REST API v3 calls with basic auth (`email:api_token`).

## MCP Server Setup

Requires Python 3.10+ and `uvx` (from `uv`). Add to `mcpServers` in `~/.claude.json`:

```json
{
  "jira": {
    "command": "uvx",
    "args": ["mcp-atlassian==0.21.0"],
    "env": {
      "JIRA_URL": "https://YOUR_ORG.atlassian.net",
      "JIRA_EMAIL": "your.email@example.com",
      "JIRA_API_TOKEN": "your-api-token"
    }
  }
}
```

API tokens are created at https://id.atlassian.com/manage-profile/security/api-tokens. Prefer system environment variables over the `env` block for anything committed.

### Tools exposed by mcp-atlassian

| Tool | Purpose |
|------|---------|
| `jira_search` | JQL queries |
| `jira_get_issue` | Fetch full issue by key |
| `jira_create_issue` | Create Task, Bug, Story, Epic |
| `jira_update_issue` | Update summary, description, assignee, fields |
| `jira_transition_issue` | Change status |
| `jira_get_transitions` | List available transitions for an issue |
| `jira_add_comment` | Add a comment |
| `jira_get_sprint_issues` | List issues in a sprint |
| `jira_create_issue_link` | Link issues (Blocks, Relates to) |
| `jira_get_issue_development_info` | Linked PRs, branches, commits |

Transition IDs vary per project workflow, so call `jira_get_transitions` before `jira_transition_issue`.

## REST API v3

Environment: `JIRA_URL` (e.g. `https://yourorg.atlassian.net`), `JIRA_EMAIL`, `JIRA_API_TOKEN`.

### Fetch an issue

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234" | jq '{
    key: .key,
    summary: .fields.summary,
    status: .fields.status.name,
    priority: .fields.priority.name,
    type: .fields.issuetype.name,
    assignee: .fields.assignee.displayName,
    labels: .fields.labels,
    description: .fields.description
  }'
```

`description` and comment bodies come back as Atlassian Document Format (ADF) JSON, not plain text.

### Fetch comments

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234?fields=comment" \
  | jq '.fields.comment.comments[] | {author: .author.displayName, created: .created[:10], body: .body}'
```

### Add a comment (ADF body)

API v3 requires the comment body in ADF. Minimal single-paragraph schema:

```bash
curl -s -X POST -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body": {
      "version": 1,
      "type": "doc",
      "content": [{
        "type": "paragraph",
        "content": [{"type": "text", "text": "Your comment here"}]
      }]
    }
  }' \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234/comment"
```

A plain string body returns 400; that only works on API v2 (`/rest/api/2/...`).

### Transition an issue (two-step flow)

Transitions are executed by ID, and IDs differ per project workflow, so always list first:

```bash
# 1. List available transitions for this issue
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234/transitions" \
  | jq '.transitions[] | {id, name}'

# 2. Execute by ID
curl -s -X POST -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "TRANSITION_ID"}}' \
  "$JIRA_URL/rest/api/3/issue/PROJ-1234/transitions"
```

A successful transition returns 204 with an empty body. Only transitions valid from the issue's current status are listed.

### Search with JQL

```bash
curl -s -G -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  --data-urlencode "jql=project = PROJ AND status = 'In Progress'" \
  "$JIRA_URL/rest/api/3/search"
```

Note: Atlassian Cloud deprecated `/rest/api/3/search` in 2025 in favor of `/rest/api/3/search/jql`, which uses `nextPageToken` cursor pagination instead of `startAt` and requires an explicit `fields` list (defaults to `id` only). If the old endpoint 404s or 410s on your instance, switch to `/search/jql`.

### JQL patterns

```
project = PROJ AND status = "In Progress"
assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC
project = PROJ AND sprint in openSprints()
updated >= -7d AND project = PROJ ORDER BY updated DESC
issuetype = Bug AND priority in (Highest, High) AND status != Done
labels in ("backend", "api") AND created >= startOfMonth()
"Epic Link" = PROJ-100
issuekey in (PROJ-1, PROJ-2, PROJ-3)
text ~ "payment timeout"
```

Quote multi-word values; `~` is a fuzzy text match; relative dates accept `-7d`, `-4w`, `startOfDay()`, `startOfMonth()`.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or expired API token | Regenerate at id.atlassian.com |
| `403 Forbidden` | Token lacks project permissions | Check token scopes and project access |
| `404 Not Found` | Wrong issue key or base URL | Verify `JIRA_URL` and issue key |
| `400` on comment POST | Plain-string body on API v3 | Wrap body in the ADF `doc` schema above |
| `spawn uvx ENOENT` | Client cannot find `uvx` on PATH | Use full path (e.g. `~/.local/bin/uvx`) or fix PATH |
| Connection timeout | Network/VPN issue | Check VPN and firewall rules |
