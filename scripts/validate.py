#!/usr/bin/env python3
"""Validate pack structure: manifests, skill/agent frontmatter, size limits."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_SKILL_LINES = 800
EMOJI_RE = re.compile(
    "[\U0001f300-\U0001faff\U00002700-\U000027bf\U0001f000-\U0001f0ff\U00002600-\U000026ff]"
)

errors = []


def err(msg):
    errors.append(msg)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        err(f"{path}: missing frontmatter")
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        err(f"{path}: unterminated frontmatter")
        return None, text
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields, text


def check_md(path, kind):
    fields, text = parse_frontmatter(path)
    if fields is None:
        return
    for req in ("name", "description"):
        if not fields.get(req):
            err(f"{path}: frontmatter missing '{req}'")
    if kind == "skill":
        expected = path.parent.name
        if fields.get("name") and fields["name"] != expected:
            err(f"{path}: name '{fields['name']}' != directory '{expected}'")
    nlines = text.count("\n") + 1
    if nlines > MAX_SKILL_LINES:
        err(f"{path}: {nlines} lines (max {MAX_SKILL_LINES})")
    if EMOJI_RE.search(text):
        err(f"{path}: contains emoji")


def main():
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = json.loads(mp.read_text())
    declared = set()
    for p in marketplace["plugins"]:
        declared.add(p["name"])
        src = ROOT / p["source"]
        if not src.is_dir():
            err(f"marketplace.json: source '{p['source']}' does not exist")

    for plugin_dir in sorted((ROOT / "plugins").iterdir()):
        if not plugin_dir.is_dir():
            continue
        manifest = plugin_dir / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            err(f"{plugin_dir.name}: missing .claude-plugin/plugin.json")
        else:
            pj = json.loads(manifest.read_text())
            if pj.get("name") != plugin_dir.name:
                err(f"{manifest}: name '{pj.get('name')}' != directory '{plugin_dir.name}'")
            if pj["name"] not in declared:
                err(f"{plugin_dir.name}: not declared in marketplace.json")
        skills_dir = plugin_dir / "skills"
        if skills_dir.is_dir():
            for sd in sorted(skills_dir.iterdir()):
                if not sd.is_dir():
                    continue
                sm = sd / "SKILL.md"
                if not sm.is_file():
                    err(f"{sd}: missing SKILL.md")
                else:
                    check_md(sm, "skill")
        agents_dir = plugin_dir / "agents"
        if agents_dir.is_dir():
            for am in sorted(agents_dir.glob("*.md")):
                check_md(am, "agent")

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    n_skills = len(list((ROOT / "plugins").glob("*/skills/*/SKILL.md")))
    n_agents = len(list((ROOT / "plugins").glob("*/agents/*.md")))
    print(f"OK: {len(declared)} plugins, {n_skills} skills, {n_agents} agents")


if __name__ == "__main__":
    main()
