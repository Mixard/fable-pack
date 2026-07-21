---
name: getting-unstuck
description: Use when about to conclude something is impossible, unsupported, or blocked - before reporting a dead end to the user. Especially after 2+ failed approaches, when a constraint comes from memory rather than a test, or when the phrase "can't be done" is forming.
---

# Getting Unstuck

## Overview

Most reported dead ends are not real. They are unverified assumptions, walls around a step rather than the goal, or approaches abandoned after one failure. Declaring "impossible" without evidence wastes the user's time twice: once on the false stop, once on the human re-investigation that follows.

**Core principle:** a dead end is a claim, and claims require evidence. "We can't" must arrive with an experiment log attached.

## The Iron Law

```
NO "IMPOSSIBLE" WITHOUT A VERIFIED CONSTRAINT AND 3+ TESTED HYPOTHESES
```

If you have not verified the wall is real AND run cheap experiments against at least 3 distinct bypass hypotheses, you may not report a dead end.

## When to Use

Trigger this process when you catch yourself:

- Drafting a message that says "this isn't possible", "the API doesn't support it", "we don't have access", "there's no way to..."
- On the 2nd-3rd failure of the *same* approach
- Citing a limitation from training-data memory instead of from a test run this session
- Facing an error you can't explain and considering giving up on the path
- About to ask the user to do something manually because automation "can't" do it

**Boundary with systematic-debugging:** if the wall is "a bug I can't fix", use systematic-debugging (root cause first). This skill is for "the path appears closed" - missing capability, unsupported feature, blocked access, no known method.

**Hard limits - these are NOT walls to break:**
- Security and permission boundaries, denied tool calls, authorization limits
- Explicit user decisions ("don't touch X", "use approach Y")
- Legal/policy constraints

Those are requirements. Route around them only by asking the user, never by hypothesis-testing bypasses.

## The Four Phases

### Phase 1: Interrogate the Wall

Before generating alternatives, establish what the wall actually is.

1. **Classify the constraint's evidence:**
   - VERIFIED: you ran a command/test this session and saw it fail; you read the actual source/docs and found the limit
   - ASSUMED: from training-data memory, from extrapolation, from "usually tools like this don't..."

   ASSUMED constraints get tested first - directly, this session. A large share of dead ends dissolve right here: the flag exists, the API has the endpoint, the version changed.

2. **Classify the constraint's hardness:**
   - HARD: physics, math, missing data that never existed, external service truly lacking the capability
   - SOFT: default config, convention, missing dependency, your own unfamiliarity, wrong tool for the layer

   Only HARD constraints can support a dead-end verdict. SOFT constraints are work items.

3. **Restate the goal one level up.** Write down: "The blocked step is X. The goal behind it is Y." Walls almost always block a step, not the goal. If Y has another path, X's wall is irrelevant.

### Phase 2: Generate Hypotheses

Produce **at least 3 distinct hypotheses** before evaluating any of them. Evaluation during generation kills the weird-but-cheap ideas that most often break impasses.

Generation moves, in rough order of yield:

| Move | Question |
|------|----------|
| Test the wall itself | "Is the constraint actually true? What one command proves/disproves it?" |
| Change layer | "Same effect via a different layer - CLI instead of API, file on disk instead of endpoint, DB directly instead of ORM, env var instead of config?" |
| Go up a level | "Does the parent goal have a path that skips this step entirely?" |
| Reduce scope | "Does solving 80% of cases unblock us? Can the rest be handled differently or later?" |
| Invert | "Instead of making X provide Y, can we make the consumer not need Y?" |
| Search the exact error | "Has someone hit this verbatim error/limit? Search issues, changelogs, forums with the exact message." |
| Fresh eyes | "Spawn a subagent with a *neutral* problem statement - goal and facts only, none of my accumulated assumptions - and see what approach it proposes." |

Write hypotheses down as a numbered list with a one-line test for each. Not "maybe try the CLI" but "H2: the CLI exposes this even though the API doesn't - test: run `tool export --help` and grep for the field."

### Phase 3: Give Each Hypothesis a Fair Chance

This is where critical thinking becomes discipline:

1. **Rank by cost-to-test, not by plausibility.** A 10-second experiment on a "probably won't work" idea runs before a 10-minute experiment on a favorite. Cheap-and-weird first.
2. **Reject only by evidence.** A hypothesis dies from a failed experiment or a VERIFIED fact - never from "that probably won't work." If you can't articulate the experiment that killed it, it isn't dead.
3. **Minimal experiments.** Smallest command, snippet, or search that produces evidence. One variable at a time. Timebox each (minutes, not hours) - a timeout means INCONCLUSIVE, not refuted.
4. **Record verdicts in a written log.** One block per hypothesis, filled in as you go - a log kept "in the head" degrades into imitation:

   ```
   H2: the CLI exposes the field even though the API hides it
   Test: tool export --help | grep -i field    (timebox: 2 min)
   Verdict: REFUTED - flag absent in v3.2 help output
   New fact: export exists but emits JSON without metadata
   ```

   CONFIRMED / REFUTED (+ the evidence) / INCONCLUSIVE. Inconclusive hypotheses survive and get reported in Phase 4.
5. **Let results breed.** A refuted hypothesis usually reveals a new fact about the system (the `New fact` line above). Feed it back: does it suggest a new hypothesis or reclassify the wall?
6. **Loop limit.** After exhausting a batch, you may return to Phase 2 with the new facts. But if two consecutive generation rounds produce no new *distinct* hypothesis, stop and proceed to Phase 4 with what you have. This skill exists to break tunnel vision, not to replace it with an endless rabbit hole.

### Phase 4: Verdict

Two valid outcomes:

**Breakthrough:** a hypothesis confirmed. Proceed with it. Note in one line which assumption turned out false - that's the lesson worth remembering.

**Documented dead end:** the constraint is VERIFIED + HARD, and 3+ distinct hypotheses were tested with recorded evidence. Report to the user:
1. The constraint and how it was verified (command/source, not vibes)
2. Each hypothesis tested and the evidence that killed it
3. Surviving INCONCLUSIVE options, with what testing them would cost
4. Best remaining alternatives with tradeoffs (reduced scope, manual step, different tool)

A dead-end report without items 1-2 is a process violation - return to Phase 1.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "The API/library/tool doesn't support this" - without having checked this session
- "I already tried everything" - when you tried variations of ONE approach
- "That idea probably won't work" - rejecting without an experiment
- "This is a known limitation" - citing memory, not the current version's docs
- Writing an apologetic "unfortunately, this isn't possible" message with zero experiments behind it
- Asking the user for a workaround before testing your own hypotheses

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I know this tool, it can't do that" | Tools change between versions. Your memory has a cutoff. Test it. |
| "Trying alternatives wastes time" | Three cheap experiments cost minutes. A false "impossible" costs the user hours. |
| "The docs say it's not supported" | Docs from memory are ASSUMED, not VERIFIED. Read the current docs or test directly. |
| "I tried three things already" | Three variations of one approach is ONE hypothesis. Count distinct mechanisms. |
| "The weird idea is embarrassing to try" | Nobody sees the experiment. Everyone sees the false dead end. |
| "User is waiting, report the blocker now" | The user wants the goal, not a status update. A breakthrough IS the fastest report. |
| "It failed once, moving on" | One failure with one configuration proves almost nothing. Vary the variable that matters. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Interrogate** | Classify evidence (verified/assumed) and hardness (hard/soft), restate goal one level up | Know what the wall actually is |
| **2. Generate** | 3+ distinct hypotheses via layer-change, level-up, scope-cut, inversion, search, fresh eyes | Numbered list, each with a one-line test |
| **3. Test** | Cheapest first, evidence-only rejection, timeboxed, verdicts recorded | Every hypothesis CONFIRMED/REFUTED/INCONCLUSIVE |
| **4. Verdict** | Proceed on breakthrough, or report documented dead end | Either progress, or an evidence-backed "no" with alternatives |
