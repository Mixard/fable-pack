#!/usr/bin/env python3
"""fable-guard Stop hook: one-shot reminder when code changed but the project map did not.

Fires only in projects that opted into cartography (CODEMAP.md at repo root).
Blocks the stop exactly once with a soft reminder; the model judges whether the
changes were substantive and stops again freely (stop_hook_active guards the loop).
Fail-open on every error - this hook must never trap a session.
"""
import json
import subprocess
import sys
from pathlib import Path

MAP_FILES = {"CODEMAP.md", "PROJECT_STATE.md", "DECISIONS.md"}


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get("stop_hook_active"):
        sys.exit(0)  # already continued once because of us - never loop

    cwd = payload.get("cwd") or "."
    try:
        root = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if not root or not (Path(root) / "CODEMAP.md").is_file():
            sys.exit(0)  # not a mapped project - stay silent

        status = subprocess.run(
            ["git", "-C", root, "status", "--porcelain"],
            capture_output=True, text=True, timeout=5,
        ).stdout.splitlines()
    except Exception:
        sys.exit(0)

    changed = [line[3:].strip() for line in status if line.strip()]
    code_changed = any(
        Path(p).name not in MAP_FILES and not p.endswith(".md") for p in changed
    )
    map_changed = any(Path(p).name in MAP_FILES for p in changed)

    if code_changed and not map_changed:
        print(json.dumps({
            "decision": "block",
            "reason": (
                "fable-guard: code changed in this mapped project but CODEMAP.md / "
                "PROJECT_STATE.md / DECISIONS.md did not. If the changes were "
                "substantive (new module, moved responsibility, finished task, "
                "architectural choice), update the affected map file now. If they "
                "were not substantive, just finish - this reminder fires only once."
            ),
        }))
    sys.exit(0)


if __name__ == "__main__":
    main()
