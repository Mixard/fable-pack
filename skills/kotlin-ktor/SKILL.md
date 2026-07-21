---
name: kotlin-ktor
description: Use when building Ktor 3.x HTTP servers. Covers install blocks for ContentNegotiation, StatusPages, CORS, and WebSockets, JWT verifier configuration, Koin DI wiring, routing DSL, and testApplication integration tests including authenticated routes.
---

# Ktor 3.x Server Patterns

Ktor apps are configured as `Application` extension functions installing plugins, with routes as `Route` extension functions. Keep routes thin; push logic to services injected via Koin.

## Entry point and module

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module).start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureAuthentication()
    configureStatusPages()
    configureCORS()
    configureDI()
    configureRouting()
}
```

## Routing DSL

```kotlin
fun Application.configureRouting() {
    routing {
        userRoutes()
        authRoutes()
    }
}

fun Route.userRoutes() {
    val userService by inject<UserService>()   // Koin

    route("/users") {
        get { call.respond(userService.getAll()) }

        get("/{id}") {
            val id = call.parameters["id"]
                ?: return@get call.respond(HttpStatusCode.BadRequest, "Missing id")
            val user = userService.getById(id)
                ?: return@get call.respond(HttpStatusCode.NotFound)
            call.respond(user)
        }

        post {
            val request = call.receive<CreateUserRequest>()
            call.respond(HttpStatusCode.Created, userService.create(request))
        }

        delete("/{id}") {
            val id = call.parameters["id"]
                ?: return@delete call.respond(HttpStatusCode.BadRequest, "Missing id")
            if (userService.delete(id)) call.respond(HttpStatusCode.NoContent)
            else call.respond(HttpStatusCode.NotFound)
        }
    }
}
```

Query parameters: `call.request.queryParameters["q"]`. Protect a subtree with `authenticate("jwt") { ... }` nested inside `route`.

## ContentNegotiation (kotlinx.serialization)

```kotlin
fun Application.configureSerialization() {
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = false
            ignoreUnknownKeys = true
            encodeDefaults = true
            explicitNulls = false
        })
    }
}
```

Custom serializer for types kotlinx.serialization does not handle:

```kotlin
object InstantSerializer : KSerializer<Instant> {
    override val descriptor = PrimitiveSerialDescriptor("Instant", PrimitiveKind.STRING)
    override fun serialize(encoder: Encoder, value: Instant) = encoder.encodeString(value.toString())
    override fun deserialize(decoder: Decoder): Instant = Instant.parse(decoder.decodeString())
}

@Serializable
data class UserResponse(
    val id: String,
    val name: String,
    @Serializable(with = InstantSerializer::class)
    val createdAt: Instant,
)
```

Response envelope pattern:

```kotlin
@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: String? = null,
) {
    companion object {
        fun <T> ok(data: T): ApiResponse<T> = ApiResponse(success = true, data = data)
        fun <T> error(message: String): ApiResponse<T> = ApiResponse(success = false, error = message)
    }
}
```

## JWT authentication

```kotlin
fun Application.configureAuthentication() {
    val jwtSecret = environment.config.property("jwt.secret").getString()
    val jwtIssuer = environment.config.property("jwt.issuer").getString()
    val jwtAudience = environment.config.property("jwt.audience").getString()
    val jwtRealm = environment.config.property("jwt.realm").getString()

    install(Authentication) {
        jwt("jwt") {
            realm = jwtRealm
            verifier(
                JWT.require(Algorithm.HMAC256(jwtSecret))
                    .withAudience(jwtAudience)
                    .withIssuer(jwtIssuer)
                    .build()
            )
            validate { credential ->
                if (credential.payload.audience.contains(jwtAudience)) {
                    JWTPrincipal(credential.payload)
                } else null
            }
            challenge { _, _ ->
                call.respond(HttpStatusCode.Unauthorized,
                    ApiResponse.error<Unit>("Invalid or expired token"))
            }
        }
    }
}
```

`validate` returning null rejects the token even if the signature verified — audience/claim checks go here. Extracting claims in handlers:

```kotlin
fun ApplicationCall.userId(): String =
    principal<JWTPrincipal>()
        ?.payload
        ?.getClaim("userId")
        ?.asString()
        ?: throw AuthenticationException("No userId in token")
```

## StatusPages

Order handlers from specific exception types to `Throwable` catch-all; `status(...)` handles response codes with no matching route:

```kotlin
fun Application.configureStatusPages() {
    install(StatusPages) {
        exception<ContentTransformationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest,
                ApiResponse.error<Unit>("Invalid request body: ${cause.message}"))
        }
        exception<IllegalArgumentException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest,
                ApiResponse.error<Unit>(cause.message ?: "Bad request"))
        }
        exception<AuthenticationException> { call, _ ->
            call.respond(HttpStatusCode.Unauthorized,
                ApiResponse.error<Unit>("Authentication required"))
        }
        exception<NotFoundException> { call, cause ->
            call.respond(HttpStatusCode.NotFound,
                ApiResponse.error<Unit>(cause.message ?: "Resource not found"))
        }
        exception<Throwable> { call, cause ->
            call.application.log.error("Unhandled exception", cause)
            call.respond(HttpStatusCode.InternalServerError,
                ApiResponse.error<Unit>("Internal server error"))
        }
        status(HttpStatusCode.NotFound) { call, status ->
            call.respond(status, ApiResponse.error<Unit>("Route not found"))
        }
    }
}
```

`ContentTransformationException` is what `call.receive<T>()` throws on malformed bodies. `require(...)` in handlers maps to 400 via the `IllegalArgumentException` handler — a cheap validation mechanism.

## CORS

```kotlin
fun Application.configureCORS() {
    install(CORS) {
        allowHost("localhost:3000")
        allowHost("example.com", schemes = listOf("https"))
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowMethod(HttpMethod.Put)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Patch)
        allowCredentials = true
        maxAgeInSeconds = 3600
    }
}
```

GET/POST/HEAD are allowed by default; PUT/DELETE/PATCH require explicit `allowMethod`. `Authorization` needs explicit `allowHeader` for JWT clients.

## Koin DI

```kotlin
val appModule = module {
    single<Database> { DatabaseFactory.create(get()) }
    single<UserRepository> { ExposedUserRepository(get()) }
    single { UserService(get()) }
    single { AuthService(get(), get()) }
}

fun Application.configureDI() {
    install(Koin) {
        modules(appModule)
    }
}
```

In routes: `val userService by inject<UserService>()` at the top of the `Route.` extension function (not inside handlers). In Kotest tests, `KoinTest` + `KoinExtension(testModule)` with mockk-backed singles.

## WebSockets

```kotlin
fun Application.configureWebSockets() {
    install(WebSockets) {
        pingPeriod = 15.seconds
        timeout = 15.seconds
        maxFrameSize = 64 * 1024   // bump only if the protocol needs larger frames
        masking = false            // server-to-client frames are unmasked per RFC 6455
    }
}

fun Route.chatRoutes() {
    val connections = Collections.synchronizedSet<Connection>(LinkedHashSet())

    webSocket("/chat") {
        val thisConnection = Connection(this)
        connections += thisConnection
        try {
            send("Connected! Users online: ${connections.size}")
            for (frame in incoming) {
                frame as? Frame.Text ?: continue
                val message = ChatMessage(thisConnection.name, frame.readText())
                // snapshot under lock to avoid ConcurrentModificationException
                val snapshot = synchronized(connections) { connections.toList() }
                snapshot.forEach { it.session.send(Json.encodeToString(message)) }
            }
        } finally {
            connections -= thisConnection
        }
    }
}

data class Connection(val session: DefaultWebSocketSession) {
    val name: String = "User-${counter.getAndIncrement()}"
    companion object { private val counter = AtomicInteger(0) }
}
```

## testApplication

`testApplication` boots the app in-process; configure only the plugins the test needs inside `application { }`. The default `client` has no content negotiation — build one with `createClient` for JSON bodies.

```kotlin
test("POST /users creates a user") {
    testApplication {
        application {
            install(Koin) { modules(testModule) }
            configureSerialization()
            configureStatusPages()
            configureRouting()
        }

        val client = createClient {
            install(io.ktor.client.plugins.contentnegotiation.ContentNegotiation) { json() }
        }

        val response = client.post("/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest("Alice", "alice@example.com"))
        }
        response.status shouldBe HttpStatusCode.Created
    }
}

test("GET /users returns list") {
    testApplication {
        application {
            install(Koin) { modules(testModule) }
            configureSerialization()
            configureRouting()
        }
        val response = client.get("/users")
        response.status shouldBe HttpStatusCode.OK
        val body = response.body<ApiResponse<List<UserResponse>>>()
        body.success shouldBe true
    }
}
```

Authenticated routes — install `configureAuthentication()` and send a real signed test token:

```kotlin
test("protected route requires JWT") {
    testApplication {
        application {
            install(Koin) { modules(testModule) }
            configureSerialization()
            configureAuthentication()
            configureRouting()
        }
        val response = client.post("/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest("Alice", "alice@example.com"))
        }
        response.status shouldBe HttpStatusCode.Unauthorized
    }
}

test("protected route succeeds with valid JWT") {
    testApplication {
        application { /* same setup */ }
        val token = generateTestJWT(userId = "test-user")
        val client = createClient {
            install(io.ktor.client.plugins.contentnegotiation.ContentNegotiation) { json() }
        }
        val response = client.post("/users") {
            contentType(ContentType.Application.Json)
            bearerAuth(token)
            setBody(CreateUserRequest("Alice", "alice@example.com"))
        }
        response.status shouldBe HttpStatusCode.Created
    }
}
```

## Configuration (application.yaml)

```yaml
ktor:
  application:
    modules:
      - com.example.ApplicationKt.module
  deployment:
    port: 8080

jwt:
  secret: ${JWT_SECRET}
  issuer: "https://example.com"
  audience: "https://example.com/api"
  realm: "example"

database:
  url: ${DATABASE_URL}
  driver: "org.postgresql.Driver"
  maxPoolSize: 10
```

Read values with `environment.config.property("jwt.secret").getString()`; `${VAR}` interpolates environment variables. All `property(...)` values come back as strings — convert numbers with `.toInt()`.
