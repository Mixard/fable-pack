#!/usr/bin/env python3
"""fable-guard PreToolUse hook: block secret leaks and dangerous shell patterns.

Reads the PreToolUse JSON from stdin. Exits 0 to allow, exits 2 with a reason on
stderr to block the tool call. No network, no state, no dependencies - the whole
policy is the regex tables below.
"""
import json
import re
import sys

SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (re.compile(r"sk-[A-Za-z0-9]{32,}"), "OpenAI-style API key"),
    (re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{22,}"), "GitHub fine-grained token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key ID"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), "private key material"),
]

DANGEROUS_BASH = [
    (
        re.compile(r"curl[^|;&]*\|\s*(?:sudo\s+)?(?:ba)?sh\b"),
        "piping a remote script straight into a shell (curl | sh)",
    ),
    (
        re.compile(r"wget[^|;&]*\|\s*(?:sudo\s+)?(?:ba)?sh\b"),
        "piping a remote script straight into a shell (wget | sh)",
    ),
    (
        re.compile(r"--dangerously-skip-permissions"),
        "disabling Claude Code permission prompts",
    ),
]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"fable-guard blocked this call: {reason}.",
        }
    }))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # malformed input: never brick the session, allow

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {}) or {}

    if tool == "Bash":
        text = tool_input.get("command", "")
        for pattern, label in DANGEROUS_BASH:
            if pattern.search(text):
                deny(label)
    else:  # Write / Edit
        text = "\n".join(
            str(tool_input.get(k, "")) for k in ("content", "new_string")
        )

    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text):
            deny(f"{label} detected in the {tool} input; move it to an env var or secret store")

    sys.exit(0)


if __name__ == "__main__":
    main()
