---
name: kotlin-ktor
description: Use when building Ktor 3.x HTTP servers. Covers the non-obvious defaults and gotchas — CORS's method allowlist, StatusPages exception-matching order, JWT validate-returning-null semantics, WebSocket protocol details — plus JWT/StatusPages/CORS/WebSocket install-block shapes.
---

# Ktor 3.x Server Patterns

Ktor apps are configured as `Application` extension functions installing plugins, with routes as `Route` extension functions. Keep routes thin; push logic to services injected via Koin (`val userService by inject<UserService>()` at the top of the `Route.` extension function, not inside handlers).

```kotlin
fun Application.module() {
    configureSerialization()
    configureAuthentication()
    configureStatusPages()
    configureCORS()
    configureDI()
    configureRouting()
}
```

Protect a route subtree with `authenticate("jwt") { ... }` nested inside `route`.

## JWT authentication

```kotlin
fun Application.configureAuthentication() {
    val jwtSecret = environment.config.property("jwt.secret").getString()
    install(Authentication) {
        jwt("jwt") {
            realm = environment.config.property("jwt.realm").getString()
            verifier(
                JWT.require(Algorithm.HMAC256(jwtSecret))
                    .withAudience(environment.config.property("jwt.audience").getString())
                    .withIssuer(environment.config.property("jwt.issuer").getString())
                    .build()
            )
            validate { credential ->
                if (credential.payload.audience.contains(jwtAudience)) {
                    JWTPrincipal(credential.payload)
                } else null
            }
            challenge { _, _ ->
                call.respond(HttpStatusCode.Unauthorized, "Invalid or expired token")
            }
        }
    }
}
```

`validate` returning `null` rejects the request even when the token's signature verified correctly — this is where audience/claim checks belong, and forgetting an `else null` branch silently accepts any signed token regardless of claims.

All `environment.config.property(...)` values come back as strings — convert numbers with `.toInt()` even for things that look numeric in the YAML.

## StatusPages

Handlers are matched from specific exception types down to `Throwable` as a catch-all; `status(...)` handles response codes with no matching route (not exceptions):

```kotlin
fun Application.configureStatusPages() {
    install(StatusPages) {
        exception<ContentTransformationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, "Invalid request body: ${cause.message}")
        }
        exception<IllegalArgumentException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, cause.message ?: "Bad request")
        }
        exception<Throwable> { call, cause ->
            call.application.log.error("Unhandled exception", cause)
            call.respond(HttpStatusCode.InternalServerError, "Internal server error")
        }
        status(HttpStatusCode.NotFound) { call, status ->
            call.respond(status, "Route not found")
        }
    }
}
```

`ContentTransformationException` is what `call.receive<T>()` throws on malformed bodies — put it before `IllegalArgumentException`, and put both before the `Throwable` catch-all (order in the `install` block is the match order). `require(...)` in a handler surfaces as 400 for free via the `IllegalArgumentException` handler.

## CORS

```kotlin
fun Application.configureCORS() {
    install(CORS) {
        allowHost("example.com", schemes = listOf("https"))
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowMethod(HttpMethod.Put)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Patch)
        allowCredentials = true
    }
}
```

GET/POST/HEAD are allowed by default; PUT/DELETE/PATCH require an explicit `allowMethod` or the browser preflight fails. `Authorization` likewise needs an explicit `allowHeader` — omitting it breaks JWT-bearing clients with no server-side error, only a browser-blocked CORS failure.

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
```

`masking = false` is correct for the server side — RFC 6455 requires client-to-server frames to be masked but forbids masking on server-to-server frames; setting `masking = true` here produces frames some clients reject.

Iterating `connections` while broadcasting needs a snapshot under lock, or a `ConcurrentModificationException` hits when a client disconnects mid-broadcast:

```kotlin
val snapshot = synchronized(connections) { connections.toList() }
snapshot.forEach { it.session.send(message) }
```

## testApplication

The default `client` inside `testApplication` has no content negotiation installed — build one with `createClient { install(ContentNegotiation) { json() } }` to send/receive JSON bodies. For routes behind `authenticate("jwt")`, send a real signed test JWT (`bearerAuth(token)`); a fake/unsigned principal does not exercise the actual verifier path.

```kotlin
test("protected route requires JWT") {
    testApplication {
        application { /* configureAuthentication(), configureRouting(), etc. */ }
        val response = client.post("/users") { setBody(CreateUserRequest("Alice", "a@example.com")) }
        response.status shouldBe HttpStatusCode.Unauthorized
    }
}
```
