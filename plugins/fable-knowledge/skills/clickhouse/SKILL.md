---
name: clickhouse
description: Use when designing ClickHouse schemas or queries. Covers MergeTree engine selection, State/Merge aggregate combinators, materialized view patterns, system.query_log and system.parts introspection, and data type / insert gotchas.
---

# ClickHouse

## MergeTree Engine Selection

- `MergeTree` -- default for raw event/fact tables.
- `ReplacingMergeTree` -- deduplication by ORDER BY key; duplicates removed only at merge time (queries may still see them until parts merge; `FINAL` forces it at query cost).
- `AggregatingMergeTree` -- stores partial aggregate states (`AggregateFunction(...)` columns), usually fed by a materialized view.

```sql
CREATE TABLE events (
    date Date,
    market_id String,
    volume UInt64,
    created_at DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, market_id);
```

Partitioning: by month or day, DATE-typed key, avoid high partition counts. ORDER BY: most-filtered columns first; column order affects both index usefulness and compression.

## State/Merge Combinators and Materialized Views

Aggregate states are written with `-State` functions and read back with the matching `-Merge` function. The MV target table declares `AggregateFunction` columns:

```sql
CREATE TABLE market_stats_hourly (
    hour DateTime,
    market_id String,
    total_volume AggregateFunction(sum, UInt64),
    total_trades AggregateFunction(count, UInt32),
    unique_users AggregateFunction(uniq, String)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, market_id);

CREATE MATERIALIZED VIEW market_stats_hourly_mv
TO market_stats_hourly
AS SELECT
    toStartOfHour(timestamp) AS hour,
    market_id,
    sumState(amount) AS total_volume,
    countState() AS total_trades,
    uniqState(user_id) AS unique_users
FROM trades
GROUP BY hour, market_id;
```

Reading requires `-Merge` plus GROUP BY (a plain SELECT on state columns returns opaque binary):

```sql
SELECT hour, market_id,
    sumMerge(total_volume) AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users) AS users
FROM market_stats_hourly
WHERE hour >= now() - INTERVAL 24 HOUR
GROUP BY hour, market_id;
```

An MV with `TO table` only sees rows inserted after its creation; backfill history with a manual `INSERT INTO target SELECT ... -State ...`.

## Query Notes

- Filter on ORDER BY / partition key columns first so partition pruning and the primary index apply; a leading `LIKE '%...%'` or non-key filter scans everything.
- Percentiles: `quantile(0.95)(x)` (approximate, fast); `quantiles(0.5, 0.95, 0.99)(x)` for several at once; `quantileExact` when precision matters.
- `uniq()` is approximate; `uniqExact()` for exact counts at higher memory cost.
- `countIf(cond)` / `sumIf(x, cond)` replace `count(CASE WHEN ...)` patterns.

## Introspection

Slow queries:

```sql
SELECT query_id, user, query, query_duration_ms, read_rows, read_bytes, memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND query_duration_ms > 1000
  AND event_time >= now() - INTERVAL 1 HOUR
ORDER BY query_duration_ms DESC
LIMIT 10;
```

Table sizes and part counts:

```sql
SELECT database, table,
    formatReadableSize(sum(bytes)) AS size,
    sum(rows) AS rows,
    count() AS parts,
    max(modification_time) AS latest_modification
FROM system.parts
WHERE active
GROUP BY database, table
ORDER BY sum(bytes) DESC;
```

## Data Types

- `LowCardinality(String)` for repeated string values (statuses, country codes, names with up to ~10k distinct values) -- large compression and speed win.
- Smallest integer type that fits (`UInt32` over `UInt64`); `Enum8/16` for fixed categorical sets.

## Gotchas

- Batch inserts: each INSERT creates a part; frequent single-row inserts cause "too many parts" errors. Batch thousands of rows per insert or use async_insert.
- Avoid `SELECT *` (column store reads every listed column) and `FINAL` in hot paths.
- Prefer denormalization over multi-way JOINs; the right side of a JOIN is materialized in memory.
