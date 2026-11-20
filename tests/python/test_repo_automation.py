"""Smoke tests for repository governance automation."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "i2n.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class RepositoryAutomationTests(unittest.TestCase):
    def test_structural_validation_passes(self) -> None:
        result = run_cli("validate", "--skip-rust")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_workspace_and_boundary_inventory_match(self) -> None:
        cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
        boundaries = json.loads((ROOT / "project" / "boundaries.json").read_text(encoding="utf-8"))
        self.assertEqual(len(boundaries["entries"]), 34)
        self.assertGreaterEqual(len(boundaries["components"]), 8)
        self.assertIn('"crates/i2n-model"', cargo)
        self.assertIn('"apps/image2native-cli"', cargo)

    def test_done_work_items_have_evidence_and_closed_dependencies(self) -> None:
        data = json.loads((ROOT / "project" / "work-items.json").read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in data["items"]}
        for item in data["items"]:
            if item["status"] == "done":
                self.assertTrue(item["evidence"], item["id"])
                for dep in item["depends_on"]:
                    self.assertEqual(by_id[dep]["status"], "done", item["id"])

    def test_boundary_inventory_contains_no_external_dependencies_without_allowlist(self) -> None:
        data = json.loads((ROOT / "project" / "boundaries.json").read_text(encoding="utf-8"))
        for entry in data["entries"]:
            self.assertIn("allowed_external_dependencies", entry)

    def test_unapproved_external_dependency_is_rejected(self) -> None:
        manifest = ROOT / "crates" / "i2n-model" / "Cargo.toml"
        original = manifest.read_text(encoding="utf-8")
        try:
            manifest.write_text(original + "\n[dependencies]\nserde = \"1\"\n", encoding="utf-8")
            result = run_cli("inventory")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unapproved external dependency", result.stdout)
        finally:
            manifest.write_text(original, encoding="utf-8")

    def test_control_file_drift_is_rejected_by_baseline(self) -> None:
        manifest = ROOT / "Cargo.toml"
        original = manifest.read_text(encoding="utf-8")
        try:
            manifest.write_text(original + "\n# intentional test drift\n", encoding="utf-8")
            result = run_cli("baseline", "verify")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("control files changed", result.stdout)
        finally:
            manifest.write_text(original, encoding="utf-8")

    def test_manual_edit_to_generated_todo_is_rejected(self) -> None:
        todo = ROOT / "TODO.md"
        original = todo.read_text(encoding="utf-8")
        try:
            todo.write_text(original + "\nmanual edit\n", encoding="utf-8")
            result = run_cli("validate", "--skip-rust")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("generated file stale: TODO.md", result.stdout)
        finally:
            todo.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
