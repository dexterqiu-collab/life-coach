#!/usr/bin/env python3
"""Synchronize the canonical Career Coach skill into the Codex plugin package."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "career-coach"
DESTINATION = ROOT / "plugins" / "life-coach" / "skills" / "career-coach"


def sync() -> Path:
    if not (SOURCE / "SKILL.md").is_file():
        raise FileNotFoundError(f"Canonical skill is missing: {SOURCE}")
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, DESTINATION)
    return DESTINATION


if __name__ == "__main__":
    synced = sync()
    print(f"Synchronized Codex plugin skill: {synced}")
