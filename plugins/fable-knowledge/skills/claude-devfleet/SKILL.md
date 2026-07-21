---
name: claude-devfleet
description: Use when orchestrating parallel Claude Code agents via the Claude DevFleet MCP server - planning projects into mission DAGs, dispatching agents in isolated git worktrees, monitoring progress, and reading structured reports. Covers exact tool signatures, the auto_dispatch draft-status gotcha, and concurrency limits.
---

# Claude DevFleet Multi-Agent Orchestration

DevFleet (github.com/LEC-AI/claude-devfleet) dispatches multiple Claude Code agents in parallel, each in an isolated git worktree with auto-merge on completion. It is a separate server: install and run it from its repository first, then connect:

```bash
claude mcp add devfleet --transport http http://localhost:18801/mcp
```

Before first use, verify the process listening on port 18801 is the DevFleet binary you installed (localhost MCP servers can be spoofed by other local processes).

## Tools

| Tool | Purpose |
|------|---------|
| `plan_project(prompt)` | AI breaks a description into a project with chained missions; returns `project_id` + mission DAG |
| `create_project(name, path?, description?)` | Create a project manually, returns `project_id` |
| `create_mission(project_id, title, prompt, depends_on?, auto_dispatch?)` | Add a mission. `depends_on` is a list of mission ID strings, e.g. `["abc-123"]` |
| `dispatch_mission(mission_id, model?, max_turns?)` | Start an agent on a mission |
| `cancel_mission(mission_id)` | Stop a running agent |
| `wait_for_mission(mission_id, timeout_seconds?)` | Block until completion (default timeout 600 s) |
| `get_mission_status(mission_id)` | Non-blocking progress check |
| `get_report(mission_id)` | Structured report: files changed, what was done, errors, next steps |
| `get_dashboard()` | Running agents, slot usage, stats, recent activity |
| `list_projects()` | Browse all projects |
| `list_missions(project_id, status?)` | List missions in a project |

Prefer polling `get_mission_status` every 30-60 s over `wait_for_mission`, which blocks the conversation for up to `timeout_seconds`.

## Gotchas

- **`auto_dispatch` defaults off for manual missions.** Without `auto_dispatch=true`, a mission stays in `draft` status and never starts when its dependencies complete. `plan_project` sets it to true automatically.
- Dispatch only the root mission (the one with empty `depends_on`); the rest auto-dispatch as dependencies resolve.
- Concurrency: 3 agents by default (configurable via `DEVFLEET_MAX_AGENTS`). Excess `auto_dispatch` missions queue and start as slots free. Check `get_dashboard()` before bulk dispatching.
- Dependencies form a DAG - no circular `depends_on`.
- On merge conflict, changes stay on the agent's worktree branch for manual resolution.
- Terminal mission states: `completed`, `failed`, `cancelled`. Read a failed mission's report before retrying.

## Workflows

Full auto: `plan_project` -> show the plan (titles, dependency chain) for approval -> `dispatch_mission` on the root -> poll `get_mission_status`/`get_dashboard` -> `get_report` per terminal mission.

Manual chain: `create_project` -> `create_mission(..., auto_dispatch=true)` for the root, then `create_mission(..., depends_on=["<root_id>"], auto_dispatch=true)` for each dependent -> `dispatch_mission` on the root.

Sequential with review: create + dispatch the implementation mission, poll to completion, review with `get_report`, then `create_mission(..., depends_on=[impl_id], auto_dispatch=true)` - it starts immediately since the dependency is already met.
