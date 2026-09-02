#!/usr/bin/env python3
"""Build deterministic distribution packages for supported agent hosts."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import stat
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CANONICAL_SKILL = ROOT / "skills" / "career-coach"
SKILL_MD = CANONICAL_SKILL / "SKILL.md"


def skill_version() -> str:
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r'^\s+version:\s+"([0-9]+\.[0-9]+\.[0-9]+)"$', text, re.MULTILINE)
    if not match:
        raise ValueError("Could not read metadata.version from canonical SKILL.md")
    return match.group(1)


def skill_body() -> str:
    text = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"^---\n.*?\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("Canonical SKILL.md has invalid frontmatter")
    return match.group(1)


def copy_skill(source: Path, destination: Path, include_openai_metadata: bool = True) -> None:
    shutil.copytree(source, destination)
    if not include_openai_metadata:
        shutil.rmtree(destination / "agents", ignore_errors=True)


def workbuddy_skill_text(version: str) -> str:
    frontmatter = f"""---
name: career-coach
display_name: 精英职业教练
display_name_en: Elite Career Coach
description: 融合前馈、高绩效、信任与坦诚、状态管理及问责体系的职业教练，帮助用户完成职业决策与行为改变。
description_zh: 融合前馈、高绩效、信任与坦诚、状态管理及问责体系的职业教练，帮助用户完成职业决策与行为改变。
description_en: An elite career coach for decisions, leadership, sustainable performance, and accountable behavior change.
version: {version}
author: Dexter
user-invocable: true
---
"""
    return frontmatter + skill_body()


def zip_tree(source: Path, output: Path) -> None:
    entries = sorted(path for path in source.rglob("*") if path.is_file())
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in entries:
            relative = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, path.read_bytes())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build() -> list[Path]:
    version = skill_version()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    staging = DIST / ".staging"
    staging.mkdir()

    codex_stage = staging / "codex" / "career-coach"
    copy_skill(CANONICAL_SKILL, codex_stage)
    codex_zip = DIST / "career-coach-codex.zip"
    zip_tree(staging / "codex", codex_zip)

    workbuddy_skill_stage = staging / "workbuddy-skill" / "skills" / "career-coach"
    copy_skill(CANONICAL_SKILL, workbuddy_skill_stage, include_openai_metadata=False)
    (workbuddy_skill_stage / "SKILL.md").write_text(workbuddy_skill_text(version), encoding="utf-8")
    workbuddy_skill_zip = DIST / "career-coach-workbuddy-skill.zip"
    zip_tree(staging / "workbuddy-skill", workbuddy_skill_zip)

    workbuddy_agent_root = staging / "workbuddy-agent"
    shutil.copytree(ROOT / ".codebuddy-plugin", workbuddy_agent_root / ".codebuddy-plugin")
    shutil.copytree(ROOT / "agents", workbuddy_agent_root / "agents")
    copy_skill(CANONICAL_SKILL, workbuddy_agent_root / "skills" / "career-coach", include_openai_metadata=False)
    (workbuddy_agent_root / "skills" / "career-coach" / "SKILL.md").write_text(
        workbuddy_skill_text(version), encoding="utf-8"
    )
    shutil.copy2(ROOT / "LICENSE", workbuddy_agent_root / "LICENSE")
    workbuddy_agent_zip = DIST / "career-coach-workbuddy-agent.zip"
    zip_tree(workbuddy_agent_root, workbuddy_agent_zip)

    doubao_prompt = DIST / "career-coach-doubao.md"
    shutil.copy2(ROOT / "platforms" / "doubao" / "SYSTEM_PROMPT.md", doubao_prompt)

    manifest = {
        "name": "career-coach",
        "version": version,
        "source": "https://github.com/dexterqiu-collab/life-coach",
        "artifacts": [
            codex_zip.name,
            workbuddy_skill_zip.name,
            workbuddy_agent_zip.name,
            doubao_prompt.name,
        ],
    }
    manifest_path = DIST / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    artifacts = [codex_zip, workbuddy_skill_zip, workbuddy_agent_zip, doubao_prompt, manifest_path]
    checksums = DIST / "SHA256SUMS"
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in artifacts), encoding="utf-8"
    )
    artifacts.append(checksums)

    shutil.rmtree(staging)
    return artifacts


if __name__ == "__main__":
    built = build()
    print(f"Built {len(built)} artifacts in {DIST}")
    for artifact in built:
        print(f"- {artifact.name}")
