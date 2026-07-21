---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies, such as multiple unrelated test failures or bugs in separate subsystems.
---

# Dispatching Parallel Agents

## Overview

You delegate tasks to agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from the others
- No shared state between investigations

**Don't use when:**
- Failures are related (fixing one might fix others) — investigate together first
- Understanding requires seeing the entire system state
- Exploratory debugging — you don't know what's broken yet
- Agents would interfere with each other (editing same files, using same resources)

Decision: multiple failures -> are they independent? If related, a single agent investigates all. If independent and no shared state, dispatch in parallel; if they'd contend for shared state, run agents sequentially.

## The Pattern

### 1. Identify Independent Domains

Group failures by what's broken:
- File A tests: tool approval flow
- File B tests: batch completion behavior
- File C tests: abort functionality

Each domain is independent — fixing tool approval doesn't affect abort tests.

### 2. Create Focused Agent Tasks

Each agent gets:
- **Specific scope:** one test file or subsystem
- **Clear goal:** make these tests pass
- **Constraints:** don't change other code
- **Expected output:** summary of what you found and fixed

### 3. Dispatch in Parallel

Issue all dispatches in the same response — they run in parallel:

```text
Subagent: "Fix agent-tool-abort.test.ts failures"
Subagent: "Fix batch-completion-behavior.test.ts failures"
Subagent: "Fix tool-approval-race-conditions.test.ts failures"
```

Multiple dispatch calls in one response = parallel execution. One per response = sequential.

### 4. Review and Integrate

When agents return:
- Read each summary
- Verify fixes don't conflict
- Run the full test suite
- Integrate all changes

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** — one clear problem domain
2. **Self-contained** — all context needed to understand the problem
3. **Specific about output** — what should the agent return?

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by:
   - Replacing arbitrary timeouts with event-based waiting
   - Fixing bugs in abort implementation if found
   - Adjusting test expectations if testing changed behavior

Do NOT just increase timeouts - find the real issue.

Return: Summary of what you found and what you fixed.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too broad: "Fix all the tests" — agent gets lost | Specific: "Fix agent-tool-abort.test.ts" — focused scope |
| No context: "Fix the race condition" — agent doesn't know where | Paste the error messages and test names |
| No constraints — agent might refactor everything | "Do NOT change production code" or "Fix tests only" |
| Vague output: "Fix it" — you don't know what changed | "Return summary of root cause and changes" |

## Real Example

**Scenario:** 6 test failures across 3 files after major refactoring — abort logic, batch completion, and race conditions are independent domains.

**Dispatch:** three agents in one response, one per file.

**Results:**
- Agent 1: replaced timeouts with event-based waiting
- Agent 2: fixed event structure bug (threadId in wrong place)
- Agent 3: added wait for async tool execution to complete

**Integration:** all fixes independent, no conflicts, full suite green — three problems solved in the time of one.

## Verification

After agents return:
1. **Review each summary** — understand what changed
2. **Check for conflicts** — did agents edit the same code?
3. **Run the full suite** — verify all fixes work together
4. **Spot check** — agents can make systematic errors

## Key Benefits

1. **Parallelization** — multiple investigations happen simultaneously
2. **Focus** — each agent has narrow scope, less context to track
3. **Independence** — agents don't interfere with each other
4. **Speed** — N problems solved in the time of one
