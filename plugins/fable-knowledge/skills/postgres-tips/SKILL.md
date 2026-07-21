---
name: postgres-tips
description: Use when writing or tuning PostgreSQL. Covers the RLS initPlan wrap trick, SKIP LOCKED job queues, diagnostic queries for unindexed FKs and bloat, index type selection, and upsert patterns.
---

# Postgres Tips

## RLS Policy Performance

Wrap per-row function calls in a scalar subquery so the planner evaluates them once (initPlan) instead of per row:

```sql
-- Slow: auth.uid() called for every row
CREATE POLICY p ON orders USING (auth.uid() = user_id);

-- Fast: evaluated once per query
CREATE POLICY p ON orders USING ((SELECT auth.uid()) = user_id);
```

## Job Queue with SKIP LOCKED

Concurrent workers claim jobs without blocking each other or double-claiming:

```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

## Diagnostics

Unindexed foreign keys (every FK column should usually have an index -- deletes on the parent scan the child otherwise):

```sql
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );
```

Table bloat / vacuum lag:

```sql
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

Slow queries (requires `CREATE EXTENSION pg_stat_statements`):

```sql
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;
```

## Index Selection

| Query pattern | Index |
|---------------|-------|
| Equality / range on scalar | B-tree (default) |
| `WHERE a = x AND b > y` | Composite `(a, b)` -- equality columns first, then range |
| JSONB `@>`, full-text `@@` | GIN |
| Large append-only time-series ranges | BRIN (tiny index, correlated data only) |
| Frequent `SELECT email, name` by email | Covering: `(email) INCLUDE (name)` |
| Mostly-filtered subset | Partial: `(email) WHERE deleted_at IS NULL` |

## Upsert

```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

`ON CONFLICT DO NOTHING` for insert-if-absent; conflict target must match a unique index or constraint.
