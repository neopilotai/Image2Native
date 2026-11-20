#!/usr/bin/env python3
"""Create GitHub labels, issues, and local development branches from work-items.json.

Safe by default: `plan` is read-only. `apply` requires an explicit GitHub CLI login
and a Git repository. Branches are created locally but never checked out; pushing is
opt-in with --push-branches.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORK_ITEMS = ROOT / "project" / "work-items.json"

LABELS: dict[str, tuple[str, str]] = {
    "type:feature": ("0E8A16", "New capability"),
    "type:task": ("1D76DB", "Engineering task"),
    "type:documentation": ("0075CA", "Documentation work"),
    "type:security": ("B60205", "Security-related work"),
    "type:testing": ("5319E7", "Testing and validation"),
    "type:chore": ("FBCA04", "Maintenance and project hygiene"),
    "priority:P0": ("B60205", "Critical priority"),
    "priority:P1": ("D93F0B", "High priority"),
    "priority:P2": ("FBCA04", "Normal priority"),
    "priority:P3": ("C5DEF5", "Low priority"),
    "status:todo": ("EDEDED", "Not started"),
    "status:in-progress": ("1D76DB", "Work in progress"),
    "status:blocked": ("B60205", "Blocked by dependency or decision"),
    "area:foundation": ("C2E0C6", "Workspace and engineering foundation"),
    "area:compiler": ("BFDADC", "Compiler and intermediate representation"),
    "area:oci": ("D4C5F9", "OCI ingestion and image handling"),
    "area:runtime": ("F9D0C4", "Execution runtime and platform backends"),
    "area:security": ("B60205", "Security and supply chain"),
    "area:release": ("C5DEF5", "Packaging and release engineering"),
    "area:docs": ("0075CA", "Documentation"),
    "area:platform": ("E99695", "Platform integration"),
    "automation:managed": ("5319E7", "Generated from project/work-items.json"),
}


def run(args: list[str], *, capture: bool = True, check: bool = True) -> str:
    proc = subprocess.run(args, cwd=ROOT, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)
    if check and proc.returncode:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(args)}\n{detail}")
    return (proc.stdout or "").strip()


def load_items() -> list[dict[str, Any]]:
    data = json.loads(WORK_ITEMS.read_text(encoding="utf-8"))
    items = data.get("items", [])
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate work-item IDs in project/work-items.json")
    known = set(ids)
    for item in items:
        missing = set(item.get("depends_on", [])) - known
        if missing:
            raise ValueError(f"{item['id']} has unknown dependencies: {sorted(missing)}")
    return items


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:48].rstrip("-") or "task"


def branch_name(item: dict[str, Any]) -> str:
    kind = "docs" if item.get("boundary") == "documentation" else "chore" if item.get("priority") == "P3" else "feat"
    return f"{kind}/{item['id'].lower()}-{slug(item['title'])}"


def area_label(item: dict[str, Any]) -> str:
    boundary = item.get("boundary", "")
    owner = item.get("owner", "")
    scope = item.get("scope", "")
    if boundary == "documentation" or owner == "docs":
        return "area:docs"
    if any(x in boundary + scope for x in ("platform", "macos", "windows", "linux")):
        return "area:platform"
    if any(x in boundary + scope for x in ("runtime", "network", "storage", "supervisor")):
        return "area:runtime"
    if any(x in boundary + scope for x in ("security", "signing", "sbom")):
        return "area:security"
    if any(x in boundary + scope for x in ("oci", "registry", "image", "layer", "rootfs", "content")):
        return "area:oci"
    if any(x in boundary + scope for x in ("release", "artifact", "package")):
        return "area:release"
    if any(x in boundary + scope for x in ("compiler", "nir", "model", "diagnostic")):
        return "area:compiler"
    return "area:foundation"


def type_label(item: dict[str, Any]) -> str:
    title = item["title"].lower()
    boundary = item.get("boundary", "").lower()
    if "security" in title or "security" in boundary:
        return "type:security"
    if "test" in title or "test" in boundary:
        return "type:testing"
    if "doc" in title or boundary == "documentation":
        return "type:documentation"
    if any(word in title for word in ("implement", "build", "support", "integrate", "create", "compile")):
        return "type:feature"
    return "type:task"


def labels_for(item: dict[str, Any]) -> list[str]:
    priority = item.get("priority", "P2")
    status = item.get("status", "todo")
    status_map = {"todo": "status:todo", "in_progress": "status:in-progress", "blocked": "status:blocked"}
    result = [type_label(item), f"priority:{priority}", area_label(item), "automation:managed"]
    if status in status_map:
        result.append(status_map[status])
    return result


def issue_body(item: dict[str, Any]) -> str:
    deps = item.get("depends_on", [])
    criteria = item.get("acceptance_criteria", [])
    evidence = item.get("evidence", [])
    dep_text = "\n".join(f"- `{dep}` (ensure dependency is complete)" for dep in deps) or "- None"
    criteria_text = "\n".join(f"- [ ] {entry}" for entry in criteria) or "- [ ] Define acceptance criteria"
    evidence_text = "\n".join(f"- `{entry}`" for entry in evidence) or "- Not yet provided"
    return f"""<!-- image2native-work-item:{item['id']} -->
## Summary
{item['title']}

## Tracking
- **Work item:** `{item['id']}`
- **Phase:** {item.get('phase', 'Unassigned')}
- **Priority:** {item.get('priority', 'P2')}
- **Owner:** `{item.get('owner', 'unassigned')}`
- **Scope:** `{item.get('scope', 'unspecified')}`
- **Boundary:** `{item.get('boundary', 'unspecified')}`
- **Suggested branch:** `{branch_name(item)}`

## Dependencies
{dep_text}

## Acceptance criteria
{criteria_text}

## Existing evidence / starting points
{evidence_text}

## Implementation notes
- Respect the package ownership and dependency rules in `project/boundaries.json`.
- Update `project/work-items.json` when status or evidence changes.
- Add or update tests; do not claim completion without verifiable evidence.
- Regenerate project reports with `python3 scripts/i2n.py all --write` when that automation is available.

---
_Generated from `project/work-items.json`; edit the source work item, not this issue body._
"""


def github_repo() -> str:
    return run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])


def existing_issues() -> dict[str, int]:
    raw = run(["gh", "issue", "list", "--state", "all", "--limit", "1000",
               "--json", "number,body"])
    found: dict[str, int] = {}
    for issue in json.loads(raw):
        body = issue.get("body") or ""
        match = re.search(r"<!-- image2native-work-item:(I2N-[A-Z0-9-]+) -->", body)
        if match:
            found[match.group(1)] = int(issue["number"])
    return found


def git_branch_exists(name: str) -> bool:
    return subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{name}"],
                          cwd=ROOT).returncode == 0


def build_plan(items: list[dict[str, Any]], include_done: bool) -> dict[str, Any]:
    selected = [x for x in items if include_done or x.get("status") != "done"]
    needed = sorted({label for item in selected for label in labels_for(item)})
    return {"items": selected, "labels": needed}


def cmd_plan(args: argparse.Namespace) -> int:
    plan = build_plan(load_items(), args.include_done)
    print(f"Repository: {ROOT}")
    print(f"Work items: {len(plan['items'])}")
    print(f"Labels to ensure: {len(plan['labels'])}")
    print("\nLabels:")
    for label in plan["labels"]:
        print(f"  - {label}")
    print("\nIssues and branches:")
    for item in plan["items"]:
        print(f"  {item['id']} [{item.get('priority')}] {item['title']}\n    issue labels: {', '.join(labels_for(item))}\n    branch: {branch_name(item)}")
    print("\nNo remote changes made. Run `apply --confirm` to create GitHub labels/issues and local branches.")
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    if not args.confirm:
        raise RuntimeError("Refusing to mutate GitHub/Git. Re-run with --confirm after reviewing `plan`.")
    if not shutil.which("gh"):
        raise RuntimeError("GitHub CLI (`gh`) is required. Install it and run `gh auth login`.")
    if not shutil.which("git") or not (ROOT / ".git").exists():
        raise RuntimeError("Initialize this directory as a Git repository before applying: git init -b main")
    repo = github_repo()
    items = build_plan(load_items(), args.include_done)["items"]
    existing = existing_issues()
    print(f"Target repository: {repo}")

    # Ensure labels before issues; --force updates descriptions/colors idempotently.
    labels_needed = sorted({label for item in items for label in labels_for(item)})
    for label in labels_needed:
        color, description = LABELS.get(label, ("EDEDED", "Image2Native project label"))
        run(["gh", "label", "create", label, "--color", color,
             "--description", description, "--force"], capture=False)
        print(f"label ensured: {label}")

    created = skipped = 0
    issue_numbers = dict(existing)
    for item in items:
        item_id = item["id"]
        if item_id in existing:
            skipped += 1
            print(f"issue exists: {item_id} -> #{existing[item_id]}")
            continue
        cmd = ["gh", "issue", "create", "--title", f"[{item_id}] {item['title']}",
               "--body", issue_body(item)]
        for label in labels_for(item):
            cmd.extend(["--label", label])
        url = run(cmd)
        match = re.search(r"/(\d+)$", url)
        if match:
            issue_numbers[item_id] = int(match.group(1))
        created += 1
        print(f"issue created: {item_id} -> {url}")

    branch_created = branch_skipped = 0
    base = args.base or run(["git", "branch", "--show-current"])
    if not base:
        base = "HEAD"
    for item in items:
        name = branch_name(item)
        if git_branch_exists(name):
            branch_skipped += 1
            print(f"branch exists: {name}")
            continue
        run(["git", "branch", name, base], capture=False)
        branch_created += 1
        print(f"branch created: {name} (from {base})")
        if args.push_branches:
            run(["git", "push", "--set-upstream", "origin", name], capture=False)

    print("\nSummary")
    print(f"  Issues created: {created}; already present: {skipped}")
    print(f"  Local branches created: {branch_created}; already present: {branch_skipped}")
    if args.push_branches:
        print("  Branches pushed: yes")
    else:
        print("  Branches pushed: no (use --push-branches to opt in)")
    print("Note: issue creation is idempotent by embedded work-item marker; branches are never checked out.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="Preview labels, issues and branch names; no mutations")
    plan.add_argument("--include-done", action="store_true", help="Include completed work items")
    plan.set_defaults(func=cmd_plan)
    apply = sub.add_parser("apply", help="Create labels, issues and local branches")
    apply.add_argument("--confirm", action="store_true", help="Required mutation confirmation")
    apply.add_argument("--include-done", action="store_true", help="Also create issues/branches for done items")
    apply.add_argument("--base", help="Base branch or commit for new branches (default: current branch)")
    apply.add_argument("--push-branches", action="store_true", help="Push new branches to origin (opt-in)")
    apply.set_defaults(func=cmd_apply)
    args = parser.parse_args()
    try:
        return args.func(args)
    except (RuntimeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
