---
name: flox-environments
description: Use when creating reproducible cross-platform (macOS/Linux) dev environments with Flox, or when a project mentions .flox/, manifest.toml, or flox activate. Covers the exact manifest.toml schema ([install], [vars], [hook], [profile], [services], [include], [options]), version pinning, pkg-group/priority conflict resolution, per-language recipes, and CLI commands.
---

# Flox Environments

Flox creates reproducible development environments defined in a single TOML manifest, built on Nix (150,000+ packages), working identically on macOS and Linux without containers. Environments live in `.flox/env/manifest.toml` and are entered with `flox activate`.

Key paths:
- `.flox/env/manifest.toml` — environment definition (commit this)
- `$FLOX_ENV` — runtime path to installed packages (like `/usr`: `bin/`, `lib/`, `include/`)
- `$FLOX_ENV_CACHE` — persistent local storage for caches, venvs, data (survives rebuilds; NOT committed)
- `$FLOX_ENV_PROJECT` — project root (where `.flox/` lives)

## CLI Commands

```bash
flox init                       # Create new environment
flox search <package> [--all]   # Search packages (case-sensitive; --all for broader search)
flox show <package>             # Show available versions
flox install <package>          # Add a package
flox list                       # List installed packages
flox list -c                    # Show raw manifest
flox activate                   # Enter environment
flox activate -- <cmd>          # Run one command inside the environment, no subshell
flox activate --start-services  # Enter environment and start [services]
flox edit                       # Edit manifest interactively
flox edit -f <file>             # Apply a manifest from a file
flox push                       # Push environment to FloxHub
flox activate -r owner/env-name # Activate a remote FloxHub environment
```

## Manifest Structure

```toml
# .flox/env/manifest.toml

[install]
ripgrep.pkg-path = "ripgrep"
jq.pkg-path = "jq"

[vars]
DATABASE_URL = "postgres://localhost:5432/myapp"

[hook]
# Non-interactive setup, runs on every activation
on-activate = """
  echo "Environment ready"
"""

[profile]
# Shell functions/aliases available in the interactive shell
common = """
  alias dev="npm run dev"
"""

[options]
systems = ["x86_64-linux", "aarch64-linux", "x86_64-darwin", "aarch64-darwin"]
```

Rule of thumb: if it should happen automatically, put it in `[hook]`; if the user should be able to type it, put it in `[profile]`. Hook-defined functions are NOT available in the interactive shell.

## Package Installation

### Version pinning

```toml
[install]
nodejs.pkg-path = "nodejs"
nodejs.version = "^20.0"          # Semver range: latest 20.x

postgres.pkg-path = "postgresql"
postgres.version = "16.2"         # Exact version
```

### Platform-specific packages

```toml
[install]
valgrind.pkg-path = "valgrind"
valgrind.systems = ["x86_64-linux", "aarch64-linux"]

# macOS frameworks
Security.pkg-path = "darwin.apple_sdk.frameworks.Security"
Security.systems = ["x86_64-darwin", "aarch64-darwin"]

# GNU tools on macOS (where BSD defaults differ)
coreutils.pkg-path = "coreutils"
coreutils.systems = ["x86_64-darwin", "aarch64-darwin"]
```

### Conflict resolution

When two packages install the same binary, `priority` decides (lower number wins):

```toml
[install]
gcc.pkg-path = "gcc12"
gcc.priority = 3

clang.pkg-path = "clang_18"
clang.priority = 5               # gcc wins file conflicts
```

Use `pkg-group` to make packages resolve versions together:

```toml
[install]
python.pkg-path = "python311"
python.pkg-group = "python-stack"

pip.pkg-path = "python311Packages.pip"
pip.pkg-group = "python-stack"
```

## Language Recipes

### Python with uv

```toml
[install]
python.pkg-path = "python311"
uv.pkg-path = "uv"

[vars]
UV_CACHE_DIR = "$FLOX_ENV_CACHE/uv-cache"
PIP_CACHE_DIR = "$FLOX_ENV_CACHE/pip-cache"

[hook]
on-activate = """
  venv="$FLOX_ENV_CACHE/venv"
  if [ ! -d "$venv" ]; then
    uv venv "$venv" --python python3
  fi
  if [ -f "$venv/bin/activate" ]; then
    source "$venv/bin/activate"
  fi
  if [ -f requirements.txt ] && [ ! -f "$FLOX_ENV_CACHE/.deps_installed" ]; then
    uv pip install --python "$venv/bin/python" -r requirements.txt --quiet
    touch "$FLOX_ENV_CACHE/.deps_installed"
  fi
"""
```

### Node.js

```toml
[install]
nodejs.pkg-path = "nodejs"
nodejs.version = "^20.0"

[hook]
on-activate = """
  if [ -f package.json ] && [ ! -d node_modules ]; then
    npm install --silent
  fi
"""
```

### Rust

```toml
[install]
rustup.pkg-path = "rustup"
pkg-config.pkg-path = "pkg-config"
openssl.pkg-path = "openssl"

[vars]
RUSTUP_HOME = "$FLOX_ENV_CACHE/rustup"
CARGO_HOME = "$FLOX_ENV_CACHE/cargo"

[profile]
common = """
  export PATH="$CARGO_HOME/bin:$PATH"
"""
```

### Go

```toml
[install]
go.pkg-path = "go"
gopls.pkg-path = "gopls"
delve.pkg-path = "delve"

[vars]
GOPATH = "$FLOX_ENV_CACHE/go"
GOBIN = "$FLOX_ENV_CACHE/go/bin"

[profile]
common = """
  export PATH="$GOBIN:$PATH"
"""
```

### C/C++

```toml
[install]
gcc.pkg-path = "gcc13"
gcc.pkg-group = "compilers"

# IMPORTANT: gcc alone doesn't expose libstdc++ headers — you need gcc-unwrapped
gcc-unwrapped.pkg-path = "gcc-unwrapped"
gcc-unwrapped.pkg-group = "libraries"

cmake.pkg-path = "cmake"
gnumake.pkg-path = "gnumake"

gdb.pkg-path = "gdb"
gdb.systems = ["x86_64-linux", "aarch64-linux"]
```

## Services

```toml
[services]
postgres.command = "postgres -D $FLOX_ENV_CACHE/pgdata -k $FLOX_ENV_CACHE"
redis.command = "redis-server --port 6379 --daemonize no"
```

Start with `flox activate --start-services`. Initialize stateful services idempotently in `[hook]`:

```toml
[hook]
on-activate = """
  if [ ! -d "$FLOX_ENV_CACHE/pgdata" ]; then
    initdb -D "$FLOX_ENV_CACHE/pgdata" --no-locale --encoding=UTF8
  fi
"""
```

## Environment Sharing and Composition

Commit `.flox/` to git; collaborators run `git clone && flox activate`. For reusable bases, push to FloxHub and compose:

```toml
[include]
base.floxhub = "myorg/python-base"

[install]
fastapi.pkg-path = "python311Packages.fastapi"   # additions on top of base
```

## Anti-Patterns

- **Absolute paths in `[vars]`** — use `$FLOX_ENV_PROJECT` instead of `/home/alice/...`.
- **`exit` in hooks** — kills the shell. Use `return 1` instead.
- **Secrets in the manifest** — it is committed. Use `API_KEY = "${API_KEY:-}"` and pass at runtime: `API_KEY=... flox activate`.
- **Non-idempotent hooks** — guard slow work with a flag file in `$FLOX_ENV_CACHE` (see Python recipe); otherwise it reruns on every activation.
- **User commands in `[hook]`** — functions defined in hooks are not available interactively; put them in `[profile]`.

## Debugging

```bash
flox list -c                      # Show raw manifest
flox activate -- which python     # Check which binary resolves
flox activate -- env | grep FLOX  # See Flox environment variables
flox search <package> --all       # Broader search (search is case-sensitive)
```

Common issues:
- Package not found: search is case-sensitive; try `flox search --all`.
- File conflicts between packages: add `priority` to the package that should win.
- Hook failures: use `return`, not `exit`; guard with `${FLOX_ENV_CACHE:-}`.
- Stale dependencies: delete the `$FLOX_ENV_CACHE/.deps_installed` flag file.

## Agent Workflow

Flox installs work entirely in user space (no sudo), are project-scoped, and are captured in `manifest.toml` (reversible, reproducible). Pattern for adding a tool on the fly:

```bash
flox search jq
flox install jq
flox activate -- jq '.results[]' data.json

# Or edit the manifest programmatically
tmp_manifest="$(mktemp)"
flox list -c > "$tmp_manifest"
# add package to [install], then:
flox edit -f "$tmp_manifest"
```
