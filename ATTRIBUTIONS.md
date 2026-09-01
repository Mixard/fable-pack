# Attributions

This pack adapts content from the following permissively licensed projects. Adaptation means: triaged against our selection principle, trimmed, cross-references to source-pack internals removed, frontmatter normalized. Substance and hard-won specifics are preserved.

| Source | License | Adapted into |
|--------|---------|--------------|
| [affaan-m/ECC](https://github.com/affaan-m/ECC) (everything-claude-code) | MIT | 35 of 36 skills across fable-mobile/web/integrations/media/niche from ECC triage (29 from the 183-skill revision, 18 from the 278-skill revision, minus regex-llm-hybrid removed in 1.0.0 and 11 model-known skills removed in 2.0); n8n-selfhosted-ops is original |
| [obra/superpowers](https://github.com/obra/superpowers) | MIT | fable-workflows: 10 of 20 skills (project-cartography, getting-unstuck, critical-review, solution-hunter are original; dispatching-parallel-agents removed in 1.0.0; requesting-code-review removed in 2.0; parallel-plans original) |
| [wshobson/agents](https://github.com/wshobson/agents) | MIT | fable-agents: 17 of 18 agents (23 adapted; sql-pro and devops-troubleshooter merged into database-optimizer and incident-responder in 1.0.0; quant-critic is original, added in 1.2.0; golang-pro, java-pro, rust-pro, python-pro removed in 2.0) |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | MIT | fable-marketing: all 20 skills |
| [BuilderIO/skills](https://github.com/BuilderIO/skills) | MIT | fable-workflows: 3 of 11 skills from triage (docs-first — renamed from read-the-damn-docs, stay-within-limits, agent-watchdog), all rewritten into the pack's hard-rule format; plan-arbiter's tie-break order folded into writing-plans. Skipped: rewind, visual-plan, visual-recap (vendor/platform-locked), efficient-fable, efficient-frontier, plow-ahead, quick-recap, plan-arbiter (overlap or below the bar) |
| [nick-vels/skills](https://github.com/nick-vels/skills) (autopilot) | MIT | fable-workflows: one rule adapted into fact-guard ("a fact about the user is never invented — visible placeholder"); fabrications-ledger format comes from an in-house project. Skipped after critical review: requirements manifest + blind acceptance, context ceiling/handoff, long-lived reviewers, secrets redaction (already in fable-guard), dashboard/state.js, polish loop — no documented failure in our projects that they would fix |

Thanks to the original authors. If you are an author and want an attribution adjusted, open an issue.
