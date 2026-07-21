---
name: mcp-server-configs
description: Use when configuring MCP servers in .claude.json or .mcp.json. Covers exact launch commands, package names, pinned versions, and hosted HTTP endpoints for common MCP servers (Jira, GitHub, Supabase, Playwright, fal.ai, Cloudflare, Vercel, and others).
---

# MCP Server Configs

Reference snapshot of working MCP server configurations (package names and URLs verified as of mid-2026; versions drift, treat as a lookup aid). Copy entries into the `mcpServers` section of `~/.claude.json` (global) or `.mcp.json` (project).

Config shapes:
- stdio servers: `{"command": ..., "args": [...], "env": {...}}`
- hosted HTTP servers: `{"type": "http", "url": ..., "headers": {...}}`

Keeping under ~10 servers enabled preserves context window; tool schemas from every enabled server load into context.

## stdio servers

```json
{
  "jira": {
    "command": "uvx",
    "args": ["mcp-atlassian==0.21.0"],
    "env": {
      "JIRA_URL": "...",
      "JIRA_EMAIL": "...",
      "JIRA_API_TOKEN": "..."
    }
  },
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "..." }
  },
  "firecrawl": {
    "command": "npx",
    "args": ["-y", "firecrawl-mcp"],
    "env": { "FIRECRAWL_API_KEY": "..." }
  },
  "supabase": {
    "command": "npx",
    "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=PROJECT_REF"]
  },
  "memory": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-memory"]
  },
  "sequential-thinking": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
  },
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/projects"]
  },
  "playwright": {
    "command": "npx",
    "args": ["-y", "@playwright/mcp", "--browser", "chrome"]
  },
  "fal-ai": {
    "command": "npx",
    "args": ["-y", "fal-ai-mcp-server"],
    "env": { "FAL_KEY": "..." }
  },
  "exa-web-search": {
    "command": "npx",
    "args": ["-y", "exa-mcp-server"],
    "env": { "EXA_API_KEY": "..." }
  },
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp@latest"]
  },
  "railway": {
    "command": "npx",
    "args": ["-y", "@railway/mcp-server"]
  },
  "browserbase": {
    "command": "npx",
    "args": ["-y", "@browserbasehq/mcp-server-browserbase"],
    "env": { "BROWSERBASE_API_KEY": "..." }
  },
  "confluence": {
    "command": "npx",
    "args": ["-y", "confluence-mcp-server"],
    "env": {
      "CONFLUENCE_BASE_URL": "...",
      "CONFLUENCE_EMAIL": "...",
      "CONFLUENCE_API_TOKEN": "..."
    }
  },
  "magic-ui": {
    "command": "npx",
    "args": ["-y", "@magicuidesign/mcp@latest"]
  }
}
```

Notes:
- `mcp-atlassian` is Python (uvx), pinned to 0.21.0 — newer releases changed tool names.
- Supabase server takes the project ref as a CLI flag, not an env var.
- Playwright MCP without `--browser` defaults to its own bundled Chromium.

## Hosted HTTP servers

```json
{
  "vercel": { "type": "http", "url": "https://mcp.vercel.com" },
  "cloudflare-docs": { "type": "http", "url": "https://docs.mcp.cloudflare.com/mcp" },
  "cloudflare-workers-builds": { "type": "http", "url": "https://builds.mcp.cloudflare.com/mcp" },
  "cloudflare-workers-bindings": { "type": "http", "url": "https://bindings.mcp.cloudflare.com/mcp" },
  "cloudflare-observability": { "type": "http", "url": "https://observability.mcp.cloudflare.com/mcp" },
  "clickhouse": { "type": "http", "url": "https://mcp.clickhouse.cloud/mcp" },
  "laraplugins": { "type": "http", "url": "https://laraplugins.io/mcp/plugins" },
  "browser-use": {
    "type": "http",
    "url": "https://api.browser-use.com/mcp",
    "headers": { "x-browser-use-api-key": "..." }
  }
}
```

Cloudflare exposes separate MCP endpoints per capability (docs, builds, bindings, observability) rather than one combined server. browser-use authenticates via the `x-browser-use-api-key` header, not an env var.
