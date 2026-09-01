---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code. Also use when tempted to write code first and test after, or to skip tests "just this once".
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing. Violating the letter of the rules is violating the spirit of the rules.

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes. **Exceptions (ask the user):** throwaway prototypes, generated code, configuration files.

Thinking "skip TDD just this once"? Stop. That's rationalization.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. **No exceptions without asking** — don't keep it as "reference," don't "adapt" it while writing tests, don't even look at it. Delete means delete. Implement fresh from tests.

## Red-Green-Refactor

Cycle: RED (write failing test) -> verify it fails correctly -> GREEN (minimal code) -> verify it passes, all green -> REFACTOR (clean up, stay green) -> next test.

### RED - Write Failing Test

Write one minimal test showing what should happen — clear name, tests real behavior, one thing, real code (no mocks unless unavoidable):

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

Bad: a vague name (`test('retry works')`), or asserting on a mock's call count instead of the real result — that tests the mock, not the code.

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

## Red Flags - STOP and Start Over

- Code before test, test written after, or a test that passes immediately or fails for reasons you can't explain
- Tests added "later", or rationalized as "just this once"
- "Keep as reference" or "adapt existing code" instead of deleting it
- "Already spent X hours, deleting is wasteful" — sunk cost, delete anyway

**All of these mean: Delete code. Start over with TDD.**

## Debugging Integration

Bug found? Use the systematic-debugging skill to reproduce it as a failing test first, then follow the Red-Green-Refactor cycle above. Never fix bugs without a test.
