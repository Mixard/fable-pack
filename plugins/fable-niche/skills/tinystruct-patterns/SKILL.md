---
name: tinystruct-patterns
description: Use when working on any project built on the tinystruct Java framework — creating Application classes, @Action-mapped routes, HTTP/CLI dual-mode handling, JSON with Builder/Builders, database persistence with AbstractData, POJO generation, Server-Sent Events, file uploads, and MCP tools/servers. Covers exact APIs, annotation modes, and the dispatcher CLI that a model would otherwise guess.
---

# tinystruct Development Patterns

Architecture and implementation patterns for building modules with the **tinystruct** Java framework — a lightweight framework that treats CLI and HTTP as equal citizens, requiring no `main()` method and minimal configuration.

## Core Principle

**CLI and HTTP are equal citizens.** Every method annotated with `@Action` should ideally be runnable from both a terminal and a web browser without modification. This "dual-mode" capability is the core design philosophy.

## How It Works

Any method annotated `@Action` is a routable endpoint for both terminal and web. Applications extend `AbstractApplication`, which provides lifecycle hooks like `init()` and access to the request `Context`. Routing is handled by the `ActionRegistry`, which maps path segments to method arguments and injects `Request`/`Response` dependencies. Native `Builder`/`Builders` handle JSON with zero external dependencies. The database layer uses `AbstractData` POJOs paired with XML mapping files.

See `references/` for detailed API references: routing, data-handling (JSON), and database persistence.

## Examples

### Basic Application

```java
public class MyService extends AbstractApplication {
    @Override
    public void init() {
        this.setTemplateRequired(false); // Disable .view lookup for data/API apps
    }

    @Override public String version() { return "1.0.0"; }

    @Action("greet")
    public String greet() { return "Hello from tinystruct!"; }

    // Path parameter: GET /?q=greet/James  OR  bin/dispatcher greet/James
    @Action("greet")
    public String greet(String name) { return "Hello, " + name + "!"; }
}
```

### HTTP Mode Disambiguation

```java
@Action(value = "login", mode = Mode.HTTP_POST)
public String doLogin(Request<?, ?> request) throws ApplicationException {
    request.getSession().setAttribute("userId", "42");
    return "Logged in";
}
```

### Native JSON Data Handling (Builder + Builders)

```java
import org.tinystruct.data.component.Builder;
import org.tinystruct.data.component.Builders;

@Action("api/data")
public String getData() throws ApplicationException {
    Builders dataList = new Builders();
    Builder item = new Builder();
    item.put("id", 1);
    item.put("name", "James");
    dataList.add(item);

    Builder response = new Builder();
    response.put("status", "success");
    response.put("data", dataList);
    return response.toString(); // {"status":"success","data":[{"id":1,"name":"James"}]}
}
```

### SSE (Server-Sent Events)

```java
import org.tinystruct.http.SSEPushManager;

// Push to a specific client
String sessionId = getContext().getId();
Builder msg = new Builder();
msg.put("text", "Hello, user!");
SSEPushManager.getInstance().push(sessionId, msg);

// Broadcast to all
SSEPushManager.getInstance().broadcast(msg);
```

### File Upload

```java
import org.tinystruct.data.FileEntity;

@Action(value = "upload", mode = Mode.HTTP_POST)
public String upload(Request<?, ?> request) throws ApplicationException {
    List<FileEntity> files = request.getAttachments();
    if (files != null) {
        for (FileEntity file : files) {
            System.out.println("Uploaded: " + file.getFilename());
        }
    }
    return "Upload OK";
}
```

## MCP Server and Tools Integration

tinystruct provides native support for the Model Context Protocol (MCP) starting with SDK version **`1.7.26`**. The MCP APIs (`org.tinystruct.mcp.MCPTool`, `MCPServer`, `MCPException`) are included directly in the core dependency:

```xml
<dependency>
    <groupId>org.tinystruct</groupId>
    <artifactId>tinystruct</artifactId>
    <version>1.7.26</version>
</dependency>
```

> **Security (Prompt Injection):** Tool return values are fed directly back into the model's context window. Validate and sanitize all caller-supplied arguments before including them in the return string — validate length, character sets, and nullity.

**To create an MCP Tool:**
1. Extend `org.tinystruct.mcp.MCPTool`.
2. Annotate operations with `@Action` and declare parameters using `@Argument` within the `arguments` array.
3. Accept parameters as explicit method arguments matching the keys in `@Argument`. (Do **not** use `getContext().getAttribute(...)` for tool arguments.)

```java
import org.tinystruct.mcp.MCPTool;
import org.tinystruct.mcp.MCPException;
import org.tinystruct.system.annotation.Action;
import org.tinystruct.system.annotation.Argument;

public class MyCustomTool extends MCPTool {
    public MyCustomTool() {
        super("custom", "A custom tool for demonstrating MCP");
    }

    @Action(
        value = "custom/hello",
        description = "Say hello to someone",
        arguments = {
            @Argument(key = "name", description = "The name to greet", type = "string", optional = false)
        }
    )
    public String hello(String name) throws MCPException {
        if (name == null || name.length() > 50 || !name.matches("^[a-zA-Z0-9 ]+$")) {
            throw new MCPException("Invalid name provided");
        }
        return "Hello, " + name + "!";
    }
}
```

**To deploy an MCP Server:** extend `org.tinystruct.mcp.MCPServer`, override `init()`, and register tools with `this.registerTool(new MyCustomTool())`. Run via the dispatcher:

```bash
bin/dispatcher start --import org.tinystruct.system.HttpServer --import com.example.MyMCPServer
```

## Configuration

Settings are managed in `src/main/resources/application.properties`.

```properties
# Database
driver=org.h2.Driver
database.url=jdbc:h2:~/mydb
database.user=sa
database.password=

# Server
default.home.page=hello
server.port=8080

# Locale
default.language=en_US

# Session (Redis for clustered environments)
# default.session.repository=org.tinystruct.http.RedisSessionRepository
# redis.host=127.0.0.1
# redis.port=6379
```

Access config values: `String port = this.getConfiguration("server.port");`

## Red Flags & Anti-patterns

| Symptom | Correct Pattern |
|---|---|
| Importing `com.google.gson` or `com.fasterxml.jackson` | Use `org.tinystruct.data.component.Builder` / `Builders`. |
| Using `List<Builder>` for JSON arrays | Use `Builders` to avoid generic type erasure issues. |
| `ApplicationRuntimeException: template not found` | Call `setTemplateRequired(false)` in `init()` for API-only apps. |
| Annotating `private` methods with `@Action` | Actions must be `public` to be registered. |
| Hardcoding `main(String[] args)` | Use `bin/dispatcher` as the entry point. |
| Manual `ActionRegistry` registration | Prefer the `@Action` annotation for automatic discovery. |
| Action not found at runtime | Ensure class is imported via `--import` or listed in `application.properties`. |
| CLI arg not visible | Pass with `--key value`; access via `getContext().getAttribute("--key")`. |
| Two methods same path, wrong one fires | Set explicit `mode` (e.g., `HTTP_GET` vs `HTTP_POST`) to disambiguate. |

## Best Practices

1. **Granular Applications**: Break logic into smaller, focused applications rather than one monolithic class.
2. **Setup in `init()`**: Leverage `init()` for setup (config, DB) rather than the constructor. Do NOT call `setAction()` — use the `@Action` annotation.
3. **Mode Awareness**: Use the `Mode` parameter in `@Action` to restrict sensitive operations to `CLI` only or specific HTTP methods.
4. **Context over Params**: For optional CLI flags, use `getContext().getAttribute("--flag")` rather than adding parameters to the method signature.
5. **Asynchronous Events**: For heavy tasks triggered by events, use `CompletableFuture.runAsync()` inside the event handler.
