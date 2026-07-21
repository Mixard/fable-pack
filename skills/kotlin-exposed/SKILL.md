---
name: kotlin-exposed
description: Use when building database access with JetBrains Exposed 1.0.0. Covers newSuspendedTransaction, DSL vs DAO styles, upsert/batchInsert, a custom jsonb ColumnType, UUIDTable definitions, HikariCP and Flyway wiring, H2 test setup, and pinned Gradle coordinates.
---

# JetBrains Exposed 1.0.0

Exposed offers two query styles: DSL (SQL-like expressions) and DAO (entity lifecycle). Use DSL for straightforward queries, DAO when you want entity objects with lazy references. In coroutine code, wrap all database work in `newSuspendedTransaction { }`; the block is atomic.

Note the 1.0.0 query API shape: `Table.selectAll().where { ... }` (the old `Table.select { ... }` overload is gone; `select(columns)` now takes a column list).

## Gradle dependencies

```kotlin
dependencies {
    implementation("org.jetbrains.exposed:exposed-core:1.0.0")
    implementation("org.jetbrains.exposed:exposed-dao:1.0.0")
    implementation("org.jetbrains.exposed:exposed-jdbc:1.0.0")
    implementation("org.jetbrains.exposed:exposed-kotlin-datetime:1.0.0")
    implementation("org.jetbrains.exposed:exposed-json:1.0.0")

    implementation("org.postgresql:postgresql:42.7.5")
    implementation("com.zaxxer:HikariCP:6.2.1")
    implementation("org.flywaydb:flyway-core:10.22.0")
    implementation("org.flywaydb:flyway-database-postgresql:10.22.0")

    testImplementation("com.h2database:h2:2.3.232")
}
```

Flyway 10+ splits Postgres support into `flyway-database-postgresql` — `flyway-core` alone fails at runtime against Postgres.

## HikariCP and Flyway wiring

```kotlin
object DatabaseFactory {
    fun create(config: DatabaseConfig): Database {
        val hikariConfig = HikariConfig().apply {
            driverClassName = config.driver          // "org.postgresql.Driver"
            jdbcUrl = config.url
            username = config.username
            password = config.password
            maximumPoolSize = config.maxPoolSize     // e.g. 10
            isAutoCommit = false
            transactionIsolation = "TRANSACTION_READ_COMMITTED"
            validate()
        }
        return Database.connect(HikariDataSource(hikariConfig))
    }
}

fun runMigrations(config: DatabaseConfig) {
    Flyway.configure()
        .dataSource(config.url, config.username, config.password)
        .locations("classpath:db/migration")
        .baselineOnMigrate(true)
        .load()
        .migrate()
}
```

Run migrations before `Database.connect` at startup. Migration files live at `src/main/resources/db/migration/V1__create_users.sql` (versioned `V<n>__name.sql`).

## Table definitions

```kotlin
object UsersTable : UUIDTable("users") {
    val name = varchar("name", 100)
    val email = varchar("email", 255).uniqueIndex()
    val role = enumerationByName<Role>("role", 20)
    val metadata = jsonb<UserMetadata>("metadata", Json.Default).nullable()
    val createdAt = timestampWithTimeZone("created_at").defaultExpression(CurrentTimestampWithTimeZone)
    val updatedAt = timestampWithTimeZone("updated_at").defaultExpression(CurrentTimestampWithTimeZone)
}

object OrderItemsTable : UUIDTable("order_items") {
    val orderId = uuid("order_id").references(OrdersTable.id, onDelete = ReferenceOption.CASCADE)
    val productId = uuid("product_id")
    val quantity = integer("quantity")
    val unitPrice = long("unit_price")
}

// Composite primary key
object UserRolesTable : Table("user_roles") {
    val userId = uuid("user_id").references(UsersTable.id, onDelete = ReferenceOption.CASCADE)
    val roleId = uuid("role_id").references(RolesTable.id, onDelete = ReferenceOption.CASCADE)
    override val primaryKey = PrimaryKey(userId, roleId)
}
```

## DSL queries

```kotlin
// Insert returning id
suspend fun insertUser(name: String, email: String, role: Role): UUID =
    newSuspendedTransaction {
        UsersTable.insertAndGetId {
            it[UsersTable.name] = name
            it[UsersTable.email] = email
            it[UsersTable.role] = role
        }.value
    }

// Select
suspend fun findUserById(id: UUID): UserRow? =
    newSuspendedTransaction {
        UsersTable.selectAll()
            .where { UsersTable.id eq id }
            .map { it.toUser() }
            .singleOrNull()
    }

// Update / delete return affected row counts
suspend fun updateUserEmail(id: UUID, newEmail: String): Boolean =
    newSuspendedTransaction {
        UsersTable.update({ UsersTable.id eq id }) {
            it[email] = newEmail
            it[updatedAt] = CurrentTimestampWithTimeZone
        } > 0
    }

suspend fun deleteUser(id: UUID): Boolean =
    newSuspendedTransaction {
        UsersTable.deleteWhere { UsersTable.id eq id } > 0
    }

// Row mapping
private fun ResultRow.toUser() = UserRow(
    id = this[UsersTable.id].value,
    name = this[UsersTable.name],
    email = this[UsersTable.email],
    role = this[UsersTable.role],
    metadata = this[UsersTable.metadata],
    createdAt = this[UsersTable.createdAt],
    updatedAt = this[UsersTable.updatedAt],
)
```

Joins, aggregation, subqueries:

```kotlin
(OrdersTable innerJoin UsersTable)
    .selectAll()
    .where { OrdersTable.userId eq userId }
    .orderBy(OrdersTable.createdAt, SortOrder.DESC)

UsersTable
    .select(UsersTable.role, UsersTable.id.count())
    .groupBy(UsersTable.role)
    .associate { it[UsersTable.role] to it[UsersTable.id.count()] }

UsersTable.selectAll()
    .where { UsersTable.id inSubQuery OrdersTable.select(OrdersTable.userId).withDistinct() }
```

LIKE with user input — escape wildcards, otherwise `%`/`_` in the query act as patterns:

```kotlin
private fun escapeLikePattern(input: String): String =
    input.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

UsersTable.selectAll()
    .where { UsersTable.name.lowerCase() like "%${escapeLikePattern(q.lowercase())}%" }
```

Pagination — `limit()` and `offset()` are separate calls, offset takes Long:

```kotlin
UsersTable.selectAll()
    .orderBy(UsersTable.createdAt, SortOrder.DESC)
    .limit(limit)
    .offset(((page - 1) * limit).toLong())
```

## Batch insert and upsert

```kotlin
UsersTable.batchInsert(users) { user ->
    this[UsersTable.name] = user.name
    this[UsersTable.email] = user.email
    this[UsersTable.role] = user.role
}.map { it[UsersTable.id].value }

// Upsert: conflict target column(s) as arguments
UsersTable.upsert(UsersTable.email) {
    it[UsersTable.id] = EntityID(id, UsersTable)
    it[UsersTable.name] = name
    it[UsersTable.email] = email
    it[updatedAt] = CurrentTimestampWithTimeZone
}
```

## DAO style

```kotlin
class UserEntity(id: EntityID<UUID>) : UUIDEntity(id) {
    companion object : UUIDEntityClass<UserEntity>(UsersTable)

    var name by UsersTable.name
    var email by UsersTable.email
    var role by UsersTable.role
    var updatedAt by UsersTable.updatedAt

    val orders by OrderEntity referrersOn OrdersTable.userId   // one-to-many
}

class OrderEntity(id: EntityID<UUID>) : UUIDEntity(id) {
    companion object : UUIDEntityClass<OrderEntity>(OrdersTable)

    var user by UserEntity referencedOn OrdersTable.userId     // many-to-one
    var status by OrdersTable.status
}
```

Operations: `UserEntity.new { ... }`, `UserEntity.findById(id)`, `UserEntity.find { UsersTable.email eq email }`, `UserEntity.all()`. Mutating properties inside a transaction writes back automatically:

```kotlin
suspend fun updateUser(id: UUID, request: UpdateUserRequest): User? =
    newSuspendedTransaction {
        UserEntity.findById(id)?.apply {
            request.name?.let { name = it }
            updatedAt = OffsetDateTime.now(ZoneOffset.UTC)
        }?.toModel()
    }
```

DAO entities and their lazy references are only valid inside the transaction — map to plain models before returning.

## Transactions

`newSuspendedTransaction` accepts an isolation level and a specific database:

```kotlin
newSuspendedTransaction(transactionIsolation = Connection.TRANSACTION_SERIALIZABLE) { /* ... */ }
newSuspendedTransaction(db = database) { /* ... */ }
```

Passing `db = database` explicitly (e.g. in a repository holding its `Database`) avoids relying on the global default connection — needed when tests and app use different databases.

## JSONB column type

Custom `ColumnType` for Postgres JSONB with kotlinx.serialization (the JDBC driver returns `PGobject`):

```kotlin
inline fun <reified T : Any> Table.jsonb(
    name: String,
    json: Json,
): Column<T> = registerColumn(name, object : ColumnType<T>() {
    override fun sqlType() = "JSONB"

    override fun valueFromDB(value: Any): T = when (value) {
        is String -> json.decodeFromString(value)
        is PGobject -> {
            val jsonString = value.value
                ?: throw IllegalArgumentException("PGobject value is null for column '$name'")
            json.decodeFromString(jsonString)
        }
        else -> throw IllegalArgumentException("Unexpected value: $value")
    }

    override fun notNullValueToDB(value: T): Any =
        PGobject().apply {
            type = "jsonb"
            this.value = json.encodeToString(value)
        }
})

@Serializable
data class UserMetadata(
    val preferences: Map<String, String> = emptyMap(),
    val tags: List<String> = emptyList(),
)
```

## Testing with H2

In-memory H2 in Postgres compatibility mode; create the schema with `SchemaUtils`:

```kotlin
val database = Database.connect(
    url = "jdbc:h2:mem:test;DB_CLOSE_DELAY=-1;MODE=PostgreSQL",
    driver = "org.h2.Driver",
)
transaction(database) { SchemaUtils.create(UsersTable) }

// per-test cleanup
transaction(database) { UsersTable.deleteAll() }
```

H2's PostgreSQL mode does not cover everything (JSONB in particular) — keep repository interfaces so integration tests against real Postgres can back the same contract.
