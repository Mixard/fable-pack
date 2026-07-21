---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code. Also use when tempted to write code first and test after, or to skip tests "just this once".
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (ask the user):** throwaway prototypes, generated code, configuration files.

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## Red-Green-Refactor

Cycle: RED (write failing test) -> verify it fails correctly -> GREEN (minimal code) -> verify it passes, all green -> REFACTOR (clean up, stay green) -> next test.

### RED - Write Failing Test

Write one minimal test showing what should happen.

Good — clear name, tests real behavior, one thing:
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```

Bad — vague name, tests the mock instead of the code:
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```

**Requirements:** one behavior, clear name, real code (no mocks unless unavoidable).

### Verify RED - Watch It Fail

**MANDATORY. Never skip.** Run the test and confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature is missing (not typos)

**Test passes?** You're testing existing behavior. Fix the test.
**Test errors?** Fix the error, re-run until it fails correctly.

### GREEN - Minimal Code

Write the simplest code to pass the test. Don't add options, configurability, or features beyond the test (YAGNI). Don't refactor other code or "improve" beyond the test.

### Verify GREEN - Watch It Pass

**MANDATORY.** Run the test and confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix the code, not the test.
**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only: remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

### Repeat

Next failing test for the next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

## Why Order Matters

**"I'll write tests after to verify it works"** — Tests written after code pass immediately. Passing immediately proves nothing: might test the wrong thing, might test implementation instead of behavior, might miss forgotten edge cases. You never saw it catch the bug. Test-first forces you to see the test fail, proving it actually tests something.

**"I already manually tested all the edge cases"** — Manual testing is ad-hoc: no record of what you tested, can't re-run when code changes, easy to forget cases under pressure. Automated tests are systematic and run the same way every time.

**"Deleting X hours of work is wasteful"** — Sunk cost fallacy. The time is already gone. Delete and rewrite with TDD (high confidence) beats keeping code you can't trust (technical debt).

**"TDD is dogmatic, being pragmatic means adapting"** — TDD IS pragmatic: finds bugs before commit, prevents regressions, documents behavior, enables refactoring. "Pragmatic" shortcuts = debugging in production = slower.

**"Tests after achieve the same goals - it's spirit not ritual"** — No. Tests-after answer "What does this do?" Tests-first answer "What should this do?" Tests-after are biased by your implementation: you test what you built, not what's required, and verify remembered edge cases instead of discovered ones.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc != systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Example: Bug Fix

**Bug:** Empty email accepted

RED:
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```
Verify RED: `FAIL: expected 'Email required', got undefined`

GREEN:
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```
Verify GREEN: `PASS`. Refactor if needed (extract validation for multiple fields).

## Testing Anti-Patterns

Iron laws for mocks and test code:

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

| Anti-Pattern | Fix |
|--------------|-----|
| Asserting on mock elements (`getByTestId('sidebar-mock')`) | Test the real component or unmock it — you're verifying the mock exists, not that the code works |
| Test-only methods on production classes (e.g. `destroy()` called only in `afterEach`) | Move cleanup to test utilities; keep production API clean |
| Mocking a method whose side effect the test depends on | Understand the dependency chain first; mock at a lower level (the actually slow/external operation) |
| Partial mock responses (only the fields your test uses) | Mirror the real API response completely — downstream code may read omitted fields |
| Tests as afterthought ("implementation complete, ready for testing") | TDD — tests are part of implementation |
| Mock setup longer than test logic | Consider integration tests with real components |

Red flags: assertions on `*-mock` IDs, methods only called from tests, mocking "just to be safe", test fails when you remove a mock, can't explain why a mock is needed.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask the user. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write a failing test reproducing it. Follow the TDD cycle. The test proves the fix and prevents regression. Never fix bugs without a test.

## Final Rule

```
Production code -> test exists and failed first
Otherwise -> not TDD
```

No exceptions without the user's permission.
