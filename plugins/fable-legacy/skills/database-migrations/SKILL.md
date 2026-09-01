---
name: database-migrations
description: Use when writing or reviewing schema migrations. Covers zero-downtime Postgres patterns (concurrent indexes, instant defaults, expand-contract) and tool-specific CLI workflows and gotchas for Prisma, Drizzle, Kysely, Django, TypeORM, and golang-migrate.
---

# Database Migrations

## PostgreSQL Facts

- `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. Most migration tools wrap each migration in a transaction by default, so this needs per-migration opt-out (or a hand-written migration file, see Prisma below).
- Postgres 11+: `ADD COLUMN ... NOT NULL DEFAULT x` is instant (default stored in catalog, no table rewrite). Before 11 it rewrote the whole table. `NOT NULL` without a default on an existing table still fails/rewrites -- add nullable, backfill, then `SET NOT NULL`.
- Plain `CREATE INDEX` blocks writes for the duration of the build; use `CONCURRENTLY` on live tables.

### Expand-Contract (Zero-Downtime Rename)

Never rename a column in place on a live system:

1. Add new column (nullable or with default).
2. Deploy app writing to both columns.
3. Backfill old rows (separate data migration).
4. Deploy app reading from new column only.
5. Drop old column in a later migration.

Same order for dropping a column: remove all application references and deploy first, drop the column in the next migration.

### Batched Backfill

```sql
DO $$
DECLARE
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET normalized_email = LOWER(email)
    WHERE id IN (
      SELECT id FROM users
      WHERE normalized_email IS NULL
      LIMIT batch_size
      FOR UPDATE SKIP LOCKED
    );
    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;
    COMMIT;
  END LOOP;
END $$;
```

Keep schema (DDL) and data (DML) in separate migrations: shorter transactions, independent rollback. Never edit a migration that has run in production -- write a new forward migration instead.

## Prisma

```bash
npx prisma migrate dev --name add_user_avatar   # create + apply in dev
npx prisma migrate deploy                        # apply pending in prod
npx prisma migrate dev --create-only --name x    # create empty migration to hand-edit
npx prisma generate                              # regenerate client
```

Prisma cannot generate `CONCURRENTLY` or data backfills -- use `--create-only` and edit `migration.sql` manually:

```sql
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);
```

Column mapping in schema: `@map("avatar_url")` per field, `@@map("users")` per model.

## Drizzle

```bash
npx drizzle-kit generate   # generate migration from schema diff
npx drizzle-kit migrate    # apply migrations
npx drizzle-kit push       # push schema directly, dev only (no migration file)
```

## Kysely (kysely-ctl)

```bash
kysely init                       # create kysely.config.ts
kysely migrate make add_avatar    # new migration file
kysely migrate latest             # apply all pending
kysely migrate down               # rollback last
kysely migrate list               # status
```

Migration files export `up`/`down` typed as `Kysely<any>`, never the typed DB interface -- migrations are frozen in time and cannot depend on the current schema types:

```typescript
import { type Kysely, sql } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('user_profile')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('email', 'varchar(255)', (col) => col.notNull().unique())
    .addColumn('created_at', 'timestamp', (col) => col.defaultTo(sql`now()`).notNull())
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('user_profile').execute()
}
```

Programmatic runner: `new Migrator({ db, provider: new FileMigrationProvider({ fs, path, migrationFolder }) })` then `migrator.migrateToLatest()`. The `allowUnorderedMigrations: true` option disables timestamp-ordering validation -- development only, it can cause schema drift between environments.

## Django

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py makemigrations --empty app_name -n description   # custom SQL / data migration
```

Data migrations use `migrations.RunPython(forward, reverse)` with `apps.get_model("app", "Model")` (historical model, not the live import). Batch with `bulk_update`.

`SeparateDatabaseAndState` updates Django's model state without touching the database -- the standard way to remove a field from the model now and drop the column in a later migration:

```python
class Migration(migrations.Migration):
    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name="user", name="legacy_field"),
            ],
            database_operations=[],  # DB untouched; drop column in a later migration
        ),
    ]
```

## TypeORM

```bash
npx typeorm migration:generate -d ./data-source.ts src/migrations/AddUserAvatar
npx typeorm migration:create src/migrations/BackfillNames   # empty migration
npx typeorm migration:run -d ./data-source.ts
npx typeorm migration:revert -d ./data-source.ts            # reverts one migration
```

Gotchas: `synchronize: true` auto-alters the schema and must stay off in production; `migration:generate` diffs entities against the live DB, so review the generated SQL -- it happily emits destructive DROPs for renames.

## golang-migrate

```bash
migrate create -ext sql -dir migrations -seq add_user_avatar   # creates .up.sql / .down.sql pair
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down 1      # rollback last
migrate -path migrations -database "$DATABASE_URL" force VERSION   # clear dirty state
```

A failed migration leaves the schema_migrations table "dirty"; fix the database manually, then `force` the correct version. Up and down files are plain SQL:

```sql
-- 000003_add_user_avatar.up.sql
ALTER TABLE users ADD COLUMN avatar_url TEXT;

-- 000003_add_user_avatar.down.sql
ALTER TABLE users DROP COLUMN IF EXISTS avatar_url;
```
