#!/usr/bin/env python3
"""Validate source structure and cross-platform metadata without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "career-coach"
SKILL_MD = SKILL_DIR / "SKILL.md"
ALLOWED_CODEX_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    require(match is not None, f"Invalid frontmatter: {path}")
    header, body = match.groups()
    top_level: dict[str, str] = {}
    for line in header.splitlines():
        if not line or line[0].isspace():
            continue
        key, separator, value = line.partition(":")
        require(bool(separator), f"Malformed frontmatter line in {path}: {line}")
        top_level[key.strip()] = value.strip()
    return top_level, body


def validate() -> list[str]:
    checks: list[str] = []
    require(SKILL_MD.is_file(), "Canonical SKILL.md is missing")
    frontmatter, body = parse_frontmatter(SKILL_MD)
    require(frontmatter.get("name") == "career-coach", "Skill name must be career-coach")
    require(bool(frontmatter.get("description")), "Skill description is required")
    require(set(frontmatter) <= ALLOWED_CODEX_KEYS, "Codex SKILL.md contains unsupported frontmatter keys")
    require(len(SKILL_MD.read_text(encoding="utf-8").splitlines()) < 500, "SKILL.md must stay under 500 lines")
    require("[TODO:" not in body, "SKILL.md contains an unfinished TODO")
    checks.append("Codex SKILL.md frontmatter and size")

    links = re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", body)
    require(len(links) == 3, "SKILL.md must route to exactly three Markdown references")
    for link in links:
        require((SKILL_DIR / link).is_file(), f"Missing referenced file: {link}")
    checks.append("Progressive-disclosure references")

    openai_yaml = SKILL_DIR / "agents" / "openai.yaml"
    require(openai_yaml.is_file(), "agents/openai.yaml is missing")
    openai_text = openai_yaml.read_text(encoding="utf-8")
    require("$career-coach" in openai_text, "OpenAI default prompt must mention $career-coach")
    require("allow_implicit_invocation: true" in openai_text, "Implicit invocation must remain enabled")
    checks.append("OpenAI UI metadata")

    plugin_path = ROOT / ".codebuddy-plugin" / "plugin.json"
    plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    skill_version_match = re.search(r'^\s+version:\s+"([0-9]+\.[0-9]+\.[0-9]+)"$',
                                    SKILL_MD.read_text(encoding="utf-8"), re.MULTILINE)
    require(skill_version_match is not None, "Skill metadata.version is missing")
    skill_version = skill_version_match.group(1)
    require(plugin.get("name") == "career-coach", "Plugin name mismatch")
    require(plugin.get("version") == skill_version, "Plugin version mismatch")
    agent_text = (ROOT / "agents" / "career-coach.md").read_text(encoding="utf-8")
    require("skills: career-coach" in agent_text, "WorkBuddy agent must auto-load the canonical skill")
    checks.append("WorkBuddy/CodeBuddy plugin and Agent metadata")

    doubao = (ROOT / "platforms" / "doubao" / "SYSTEM_PROMPT.md").read_text(encoding="utf-8")
    for phrase in ("一次最多问三个", "可回退", "不虚构研究", "自伤、自杀"):
        require(phrase in doubao, f"Doubao prompt is missing shared invariant: {phrase}")
    checks.append("Doubao standalone prompt invariants")

    install_text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    require("skills/career-coach" in install_text, "INSTALL.md must identify the canonical skill path")
    require("raw.githubusercontent.com/dexterqiu-collab/life-coach/main/INSTALL.md" in readme_text,
            "README.md must expose the one-link installation contract")
    checks.append("One-link installation entrypoint")

    return checks


def main() -> int:
    try:
        checks = validate()
    except (ValidationError, json.JSONDecodeError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1
    print(f"Validation passed ({len(checks)} checks):")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
