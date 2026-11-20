import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("github_project", ROOT / "scripts" / "github_project.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GitHubProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = MODULE.load_items()

    def test_work_item_ids_are_unique_and_dependencies_resolve(self):
        ids = [item["id"] for item in self.items]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(ids)
        for item in self.items:
            self.assertTrue(set(item.get("depends_on", [])).issubset(known))

    def test_each_item_has_stable_issue_marker(self):
        for item in self.items:
            self.assertIn(f"image2native-work-item:{item['id']}", MODULE.issue_body(item))

    def test_each_item_has_managed_label_and_branch(self):
        for item in self.items:
            self.assertIn("automation:managed", MODULE.labels_for(item))
            self.assertRegex(MODULE.branch_name(item), r"^(feat|docs|chore)/i2n-")

    def test_done_items_are_excluded_by_default(self):
        plan = MODULE.build_plan(self.items, include_done=False)
        self.assertTrue(all(item.get("status") != "done" for item in plan["items"]))

    def test_label_definitions_cover_generated_labels(self):
        plan = MODULE.build_plan(self.items, include_done=False)
        self.assertTrue(set(plan["labels"]).issubset(MODULE.LABELS))


if __name__ == "__main__":
    unittest.main()
