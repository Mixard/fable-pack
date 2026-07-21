---
name: laravel-plugin-discovery
description: Use when finding or evaluating Laravel packages (maintenance health, Laravel/PHP version compatibility, vendor reputation) via the free LaraPlugins.io MCP server. Covers the MCP endpoint config and the exact SearchPluginTool / GetPluginDetailsTool parameter schemas and filter values.
---

# Laravel Plugin Discovery (LaraPlugins.io MCP)

Find and evaluate Laravel packages using the LaraPlugins.io MCP server. Free, no API key.

## MCP Configuration

Add to `mcpServers` in `~/.claude.json` (or `.mcp.json`):

```json
"laraplugins": {
  "type": "http",
  "url": "https://laraplugins.io/mcp/plugins"
}
```

## Tools

### SearchPluginTool

Search packages by keyword, health, vendor, and version compatibility.

Parameters (all optional):
- `text_search` (string): keyword, e.g. "permission", "admin", "api"
- `health_score` (string): `Healthy`, `Medium`, `Unhealthy`, or `Unrated`
- `laravel_compatibility` (string): Laravel major version as a string — `"5"` through `"13"`
- `php_compatibility` (string): `"7.4"`, `"8.0"`, `"8.1"`, `"8.2"`, `"8.3"`, `"8.4"`, `"8.5"`
- `vendor_filter` (string): vendor name, e.g. "spatie", "laravel"
- `page` (number): pagination

### GetPluginDetailsTool

Fetch detailed metrics, readme, and version history for one package.

Parameters:
- `package` (string, required): full Composer name, e.g. "spatie/laravel-permission"
- `include_versions` (boolean, optional): include version history

Detail responses include health score, last activity, Laravel/PHP compatibility matrix, vendor risk score, and version history.

## Health Bands

| Band | Meaning |
| --- | --- |
| `Healthy` | Active maintenance, recent updates |
| `Medium` | Occasional updates |
| `Unhealthy` | Abandoned or rarely maintained |
| `Unrated` | Not yet assessed |

Prefer `Healthy` for production; always match `laravel_compatibility` to the target project's version.

## Example Calls

```
SearchPluginTool({ text_search: "authentication", health_score: "Healthy" })

SearchPluginTool({ text_search: "admin panel", laravel_compatibility: "12" })

SearchPluginTool({ vendor_filter: "spatie", health_score: "Healthy" })

GetPluginDetailsTool({ package: "spatie/laravel-permission", include_versions: true })
```
