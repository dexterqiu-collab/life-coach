from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "build_packages.py")], check=True)

    def zip_names(self, filename: str) -> set[str]:
        with zipfile.ZipFile(DIST / filename) as archive:
            return set(archive.namelist())

    def test_codex_archive_has_one_skill_root(self) -> None:
        names = self.zip_names("career-coach-codex.zip")
        self.assertIn("career-coach/SKILL.md", names)
        self.assertIn("career-coach/agents/openai.yaml", names)
        self.assertIn("career-coach/references/templates.md", names)

    def test_codex_plugin_archive_is_installable(self) -> None:
        archive_path = DIST / "life-coach-codex-plugin.zip"
        names = self.zip_names(archive_path.name)
        self.assertIn(".codex-plugin/plugin.json", names)
        self.assertIn("skills/career-coach/SKILL.md", names)
        self.assertIn("LICENSE", names)
        with zipfile.ZipFile(archive_path) as archive:
            plugin = json.loads(archive.read(".codex-plugin/plugin.json"))
            packaged_skill = archive.read("skills/career-coach/SKILL.md")
        self.assertEqual("life-coach", plugin["name"])
        self.assertEqual("2.2.0", plugin["version"])
        self.assertEqual((ROOT / "skills" / "career-coach" / "SKILL.md").read_bytes(), packaged_skill)

    def test_workbuddy_skill_archive_matches_official_shape(self) -> None:
        archive_path = DIST / "career-coach-workbuddy-skill.zip"
        names = self.zip_names(archive_path.name)
        self.assertIn("skills/career-coach/SKILL.md", names)
        self.assertNotIn("skills/career-coach/agents/openai.yaml", names)
        with zipfile.ZipFile(archive_path) as archive:
            skill_text = archive.read("skills/career-coach/SKILL.md").decode("utf-8")
        for field in ("description_zh:", "description_en:", "version: 2.2.0", "author: Dexter"):
            self.assertIn(field, skill_text)

    def test_workbuddy_agent_archive_contains_agent_and_skill(self) -> None:
        names = self.zip_names("career-coach-workbuddy-agent.zip")
        self.assertIn(".codebuddy-plugin/plugin.json", names)
        self.assertIn("agents/career-coach.md", names)
        self.assertIn("skills/career-coach/SKILL.md", names)
        self.assertIn("LICENSE", names)

    def test_elite_system_is_preserved_across_platforms(self) -> None:
        canonical = (ROOT / "skills" / "career-coach" / "SKILL.md").read_text(encoding="utf-8")
        playbook = (ROOT / "skills" / "career-coach" / "references" / "coaching-playbook.md").read_text(
            encoding="utf-8"
        )
        doubao = (ROOT / "platforms" / "doubao" / "SYSTEM_PROMPT.md").read_text(encoding="utf-8")

        for phrase in (
            "Marshall Goldsmith",
            "Brendon Burchard",
            "Bill Campbell",
            "Tony Robbins",
            "Robin Sharma",
            "Five-stage coaching arc",
        ):
            self.assertIn(phrase, canonical)
        for model in (
            "Feedforward growth",
            "State–action loop",
            "Trust–candor–humanity triangle",
            "Protected-focus moat",
            "Belief–evidence distinction",
            "Five-stage transformation",
            "Deliberate practice and accountability",
        ):
            self.assertIn(model, playbook)
        for phrase in ("前馈式成长", "状态—行动闭环", "信任—坦诚—人文三角", "五阶段教练流程"):
            self.assertIn(phrase, doubao)

    def test_manifest_and_checksums_cover_every_artifact(self) -> None:
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("2.2.0", manifest["version"])
        checksum_lines = (DIST / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        checksums = {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in checksum_lines}
        expected = set(manifest["artifacts"]) | {"manifest.json"}
        self.assertEqual(expected, set(checksums))
        for filename, expected_digest in checksums.items():
            actual = hashlib.sha256((DIST / filename).read_bytes()).hexdigest()
            self.assertEqual(expected_digest, actual)

    def test_source_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate.py")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_shell_installer_is_idempotent_and_force_keeps_backup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            skills_directory = Path(temporary_directory) / "skills"
            environment = os.environ.copy()
            environment["CAREER_COACH_CODEX_SKILLS_DIR"] = str(skills_directory)
            command = ["bash", str(ROOT / "scripts" / "install.sh"), "codex"]
            subprocess.run(command, check=True, capture_output=True, text=True, env=environment)
            installed = skills_directory / "career-coach"
            self.assertTrue((installed / "SKILL.md").is_file())

            second = subprocess.run(command, check=False, capture_output=True, text=True, env=environment)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertIn("Skipped existing installation", second.stderr)

            forced = subprocess.run(command + ["--force"], check=False, capture_output=True, text=True,
                                    env=environment)
            self.assertEqual(0, forced.returncode, forced.stderr)
            backups = list(skills_directory.glob("career-coach.backup-*"))
            self.assertEqual(1, len(backups))
            self.assertTrue((installed / "references" / "templates.md").is_file())


if __name__ == "__main__":
    unittest.main()
