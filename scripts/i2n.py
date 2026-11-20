#!/usr/bin/env python3
"""Image2Native repository automation: TODOs, boundaries, baseline and reports."""
from __future__ import annotations
import argparse
import json
import os
import hashlib
import re
import subprocess
import sys
import tomllib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "project"
REPORTS = ROOT / "reports"
VALID_STATUSES = {"todo", "in_progress", "blocked", "done"}


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_workspace():
    with (ROOT / "Cargo.toml").open("rb") as f:
        data = tomllib.load(f)
    members = data.get("workspace", {}).get("members", [])
    if not isinstance(members, list):
        raise ValueError("Cargo.toml workspace.members must be an array")
    return members


def load_boundaries():
    data = read_json(PROJECT / "boundaries.json")
    entries = data.get("entries", [])
    by_package = {entry["package"]: entry for entry in entries}
    by_path = {entry["path"]: entry for entry in entries}
    if len(by_package) != len(entries) or len(by_path) != len(entries):
        raise ValueError("Duplicate package or path in project/boundaries.json")
    return data, by_package, by_path


def inspect_members():
    members = load_workspace()
    boundary_data, by_package, by_path = load_boundaries()
    problems = []
    actual = {}
    for member in members:
        path = ROOT / member
        manifest = path / "Cargo.toml"
        if not manifest.is_file():
            problems.append(f"workspace member `{member}` has no Cargo.toml")
            continue
        with manifest.open("rb") as f:
            package = tomllib.load(f).get("package", {})
        name = package.get("name")
        if not name:
            problems.append(f"workspace member `{member}` has no [package].name")
            continue
        actual[name] = {"path": member, "package": package, "manifest": manifest}
        entry = by_package.get(name)
        if not entry:
            problems.append(f"workspace package `{name}` is missing from project/boundaries.json")
        elif entry.get("path") != member:
            problems.append(f"boundary path mismatch for `{name}`: {entry.get('path')} != {member}")
    for package, entry in by_package.items():
        if package not in actual:
            problems.append(f"boundary inventory package `{package}` is not a Cargo workspace member")
        if not (ROOT / entry["path"]).is_dir():
            problems.append(f"boundary path does not exist: {entry['path']}")
    return members, actual, by_package, problems


def dependency_edges(actual, by_package):
    edges, problems = [], []
    package_to_path = {name: info["path"] for name, info in actual.items()}
    for name, info in actual.items():
        entry = by_package.get(name)
        if not entry:
            continue
        allowed = set(entry.get("allowed_dependency_groups", []))
        with info["manifest"].open("rb") as f:
            manifest = tomllib.load(f)
        for section in ("dependencies", "dev-dependencies", "build-dependencies"):
            for alias, spec in manifest.get(section, {}).items():
                spec = spec if isinstance(spec, dict) else {}
                target_name = spec.get("package", alias)
                target_path = spec.get("path")
                if target_path:
                    resolved = (info["manifest"].parent / target_path).resolve()
                    expected_path = package_to_path.get(target_name)
                    if expected_path is None:
                        problems.append(f"{name}: local path dependency `{target_name}` is not a workspace package")
                    elif resolved != (ROOT / expected_path).resolve():
                        problems.append(f"{name}: path dependency `{target_name}` points outside its declared workspace path")
                target = by_package.get(target_name)
                if target:
                    edges.append({"from": name, "to": target_name, "section": section,
                                  "from_group": entry["group"], "to_group": target["group"]})
                    if target["group"] not in allowed:
                        problems.append(f"forbidden dependency edge: {name} ({entry['group']}) -> {target_name} ({target['group']})")
                    if target.get("kind") == "application" and entry.get("kind") != "application":
                        problems.append(f"core crate `{name}` must not depend on application `{target_name}`")
                elif not target_path and target_name not in set(entry.get("allowed_external_dependencies", [])):
                    problems.append(f"unapproved external dependency: {name} -> {target_name}; add it to allowed_external_dependencies after review")
    return edges, problems


def inventory_data():
    members, actual, by_package, problems = inspect_members()
    edges, edge_problems = dependency_edges(actual, by_package)
    problems.extend(edge_problems)
    rows = []
    components = load_boundaries()[0].get("components", [])
    seen_component_ids = set()
    for component in components:
        component_id = component.get("id", "<missing-id>")
        if component_id in seen_component_ids:
            problems.append(f"duplicate repository component id `{component_id}`")
        seen_component_ids.add(component_id)
        component_path = component.get("path")
        if not component_path or not (ROOT / component_path).is_dir():
            problems.append(f"repository component `{component_id}` has missing path `{component_path}`")
    for name in sorted(actual):
        entry = by_package.get(name, {})
        rows.append({"package": name, "path": actual[name]["path"], "kind": entry.get("kind", "unclassified"),
                     "group": entry.get("group", "unclassified"), "owner": entry.get("owner", "unassigned"),
                     "responsibility": entry.get("responsibility", ""),
                     "allowed_dependency_groups": entry.get("allowed_dependency_groups", []),
                     "allowed_external_dependencies": entry.get("allowed_external_dependencies", [])})
    return {"schemaVersion": 1,
            "workspaceMemberCount": len(members), "packageCount": len(actual),
            "componentCount": len(components), "components": sorted(components, key=lambda item: item["id"]),
            "dependencyEdgeCount": len(edges), "packages": rows, "dependencyEdges": edges,
            "problems": sorted(set(problems))}


def load_work_items():
    data = read_json(PROJECT / "work-items.json")
    items = data.get("items", [])
    by_id = {item["id"]: item for item in items}
    problems = []
    if len(by_id) != len(items):
        problems.append("duplicate work item IDs")
    for item in items:
        missing = [field for field in ("id", "title", "phase", "priority", "status", "owner", "scope", "boundary", "depends_on", "acceptance_criteria", "evidence") if field not in item]
        if missing:
            problems.append(f"{item.get('id', '<unknown>')}: missing required fields {missing}")
        if item.get("status") not in VALID_STATUSES:
            problems.append(f"{item.get('id')}: invalid status `{item.get('status')}`")
        if item.get("status") == "done" and not item.get("evidence"):
            problems.append(f"{item.get('id')}: done item requires evidence")
        if not item.get("acceptance_criteria"):
            problems.append(f"{item.get('id')}: acceptance_criteria must not be empty")
        for dep in item.get("depends_on", []):
            if dep not in by_id:
                problems.append(f"{item.get('id')}: unknown dependency `{dep}`")
            elif item.get("status") == "done" and by_id[dep].get("status") != "done":
                problems.append(f"{item.get('id')}: marked done while dependency `{dep}` is not done")
    # Detect dependency cycles with DFS.
    visiting, visited = set(), set()
    def visit(item_id):
        if item_id in visiting:
            problems.append(f"task dependency cycle includes `{item_id}`")
            return
        if item_id in visited or item_id not in by_id:
            return
        visiting.add(item_id)
        for dep in by_id[item_id].get("depends_on", []): visit(dep)
        visiting.remove(item_id)
        visited.add(item_id)
    for item_id in by_id: visit(item_id)
    return data, items, by_id, sorted(set(problems))


def render_todo(items):
    counts = Counter(i["status"] for i in items)
    lines = ["# TODO", "", "> Generated from [`project/work-items.json`](project/work-items.json). Do not edit this file directly.",
             "> Regenerate with `python3 scripts/i2n.py checklist --write` or `make todo`.", "",
             f"**Progress:** {counts['done']}/{len(items)} complete · {counts['in_progress']} in progress · {counts['blocked']} blocked · {counts['todo']} open", ""]
    for phase in sorted({i["phase"] for i in items}):
        lines += [f"## Phase {phase}", ""]
        for item in sorted((i for i in items if i["phase"] == phase), key=lambda x: (x["priority"], x["id"])):
            mark = "x" if item["status"] == "done" else " "
            lines.append(f"- [{mark}] **{item['id']} — {item['title']}** [{item['status']} / {item['priority']}] — owner: `{item['owner']}`; boundary: `{item['boundary']}`")
            for criterion in item["acceptance_criteria"]:
                lines.append(f"  - Acceptance: {criterion}")
            if item.get("depends_on"):
                lines.append(f"  - Depends on: {', '.join('`'+x+'`' for x in item['depends_on'])}")
            if item.get("evidence"):
                lines.append(f"  - Evidence: {', '.join('`'+x+'`' for x in item['evidence'])}")
        lines.append("")
    lines += ["## Update process", "", "Edit `project/work-items.json`, then run `python3 scripts/i2n.py all --write`. A task may be marked `done` only after its acceptance criteria are met and evidence paths are recorded.", ""]
    return "\n".join(lines)


def render_checklist(items):
    counts = Counter(i["status"] for i in items)
    lines = ["# Checklist Report", "", f"- Total: **{len(items)}**", f"- Done: **{counts['done']}**", f"- In progress: **{counts['in_progress']}**", f"- Blocked: **{counts['blocked']}**", f"- Open: **{counts['todo']}**", "", "| ID | Phase | Priority | Status | Owner | Boundary | Task |", "|---|---:|---|---|---|---|---|"]
    for i in sorted(items, key=lambda x: (x["phase"], x["id"])):
        lines.append(f"| {i['id']} | {i['phase']} | {i['priority']} | {i['status']} | {i['owner']} | `{i['boundary']}` | {i['title']} |")
    return "\n".join(lines) + "\n"


def render_inventory(data):
    lines = ["# Generated Boundary Inventory", "", f"- Workspace members: **{data['workspaceMemberCount']}**", f"- Packages indexed: **{data['packageCount']}**", f"- Local dependency edges: **{data['dependencyEdgeCount']}**", "", "| Package | Kind | Group | Owner | Path | Responsibility |", "|---|---|---|---|---|---|"]
    for p in data["packages"]:
        lines.append(f"| `{p['package']}` | {p['kind']} | {p['group']} | {p['owner']} | `{p['path']}` | {p['responsibility']} |")
    lines += ["", "## Non-Cargo repository components", "", f"- Components inventoried: **{data.get('componentCount', 0)}**", "", "| Component | Kind | Owner | Path | Responsibility |", "|---|---|---|---|---|"]
    for component in data.get("components", []):
        lines.append(f"| `{component['id']}` | {component['kind']} | {component['owner']} | `{component['path']}` | {component['responsibility']} |")
    lines += ["", "## Dependency edges", ""]
    if not data["dependencyEdges"]: lines.append("No local dependency edges detected.")
    for e in data["dependencyEdges"]: lines.append(f"- `{e['from']}` → `{e['to']}` ({e['section']})")
    lines += ["", "## Violations", ""]
    lines += [f"- {p}" for p in data["problems"]] if data["problems"] else ["No boundary violations detected."]
    lines += ["", "> Generated by `python3 scripts/i2n.py inventory --write`. Source: `project/boundaries.json` and Cargo manifests.", ""]
    return "\n".join(lines)


def required_baseline():
    boundaries, by_package, _ = load_boundaries()
    required_docs = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md"))
    protected = [
        "Cargo.toml", "Cargo.lock", "rust-toolchain.toml", "README.md", "WHITEPAPER.md", "BLUEPRINT.md",
        "TODO.md", "CHANGELOG.md", "Makefile", "CONTRIBUTING.md", "SECURITY.md", "project/project.json",
        "project/work-items.json", "project/boundaries.json", "schemas/work-items.schema.json",
        "schemas/boundaries.schema.json", "schemas/nir-v0.1.schema.json", "schemas/i2n-artifact-v1.schema.json",
        "scripts/i2n.py", "scripts/install_hooks.py", "tests/python/test_repo_automation.py",
        ".github/workflows/ci.yml", ".github/pull_request_template.md"
    ] + required_docs
    control_files = [
        "Cargo.toml", "Cargo.lock", "project/boundaries.json", "schemas/boundaries.schema.json",
        "scripts/i2n.py", ".github/workflows/ci.yml"
    ]
    control_hashes = {
        file_path: hashlib.sha256((ROOT / file_path).read_bytes()).hexdigest()
        for file_path in control_files
        if (ROOT / file_path).is_file()
    }
    return {"schemaVersion":1,"project":"Image2Native","baselineKind":"structural-contract","planningDate":"2026-11-20",
            "maturity":{"phase":"foundation-scaffold","compilerImplemented":False,"ociIngestionImplemented":False,"rootfsCompilerImplemented":False,"platformBackendsImplemented":False,"automationImplemented":True},
            "requiredWorkspacePackages":sorted(by_package),
            "requiredComponentIds":sorted(component["id"] for component in load_boundaries()[0].get("components", [])),
            "requiredFiles":sorted(set(protected)),"controlFileSha256":control_hashes,
            "policy":{"untrackedWorkspaceMembersFail":True,"unapprovedDependencyEdgesFail":True,"doneTasksRequireEvidence":True,"generatedReportsMustBeCurrent":True,"controlFileChangesRequireBaselineRefresh":True}}


def render_baseline(baseline, current=None):
    m = baseline.get("maturity", {})
    lines = ["# Repository Baseline", "", f"- Baseline kind: `{baseline.get('baselineKind')}`", f"- Planning date: {baseline.get('planningDate')}", f"- Required workspace packages: **{len(baseline.get('requiredWorkspacePackages', []))}**", f"- Required repository components: **{len(baseline.get('requiredComponentIds', []))}**", f"- Protected files: **{len(baseline.get('requiredFiles', []))}**", "", "## Maturity declaration", ""]
    for key, value in m.items(): lines.append(f"- {key}: **{str(value).lower()}**")
    if current:
        lines += ["", "## Current structural observations", "", f"- Workspace packages present: {current.get('workspacePackageCount', 0)}", f"- Required packages missing: {len(current.get('missingPackages', []))}", f"- Unapproved packages added: {len(current.get('unexpectedPackages', []))}", f"- Repository components present: {current.get('componentCount', 0)}", f"- Required components missing: {len(current.get('missingComponents', []))}", f"- Unapproved components added: {len(current.get('unexpectedComponents', []))}", f"- Required files missing: {len(current.get('missingFiles', []))}", f"- Control files changed: {len(current.get('changedControlFiles', []))}"]
    lines += ["", "Refresh only after reviewed structural changes: `python3 scripts/i2n.py baseline capture --write`.", ""]
    return "\n".join(lines)


def verify_baseline():
    path = PROJECT / "baseline.json"
    if not path.is_file():
        return ["project/baseline.json is missing"], {"workspacePackageCount": 0, "missingPackages": [], "unexpectedPackages": [], "componentCount": 0, "missingComponents": [], "unexpectedComponents": [], "missingFiles": [], "changedControlFiles": []}
    baseline = read_json(path)
    members, actual, _, _ = inspect_members()
    boundary_data, _, _ = load_boundaries()
    current_names = set(actual)
    required_names = set(baseline.get("requiredWorkspacePackages", []))
    missing_packages = sorted(required_names - current_names)
    unexpected_packages = sorted(current_names - required_names)
    current_components = {component.get("id") for component in boundary_data.get("components", [])}
    required_components = set(baseline.get("requiredComponentIds", []))
    missing_components = sorted(required_components - current_components)
    unexpected_components = sorted(current_components - required_components)
    missing_files = sorted(f for f in baseline.get("requiredFiles", []) if not (ROOT / f).exists())
    changed_control_files = []
    for file_path, expected_hash in baseline.get("controlFileSha256", {}).items():
        current_path = ROOT / file_path
        actual_hash = hashlib.sha256(current_path.read_bytes()).hexdigest() if current_path.is_file() else None
        if actual_hash != expected_hash:
            changed_control_files.append(file_path)
    problems = []
    if missing_packages:
        problems.append("missing baseline workspace packages: " + ", ".join(missing_packages))
    if unexpected_packages:
        problems.append("unapproved workspace packages (review boundaries and refresh baseline): " + ", ".join(unexpected_packages))
    if missing_components:
        problems.append("missing baseline repository components: " + ", ".join(missing_components))
    if unexpected_components:
        problems.append("unapproved repository components (review boundaries and refresh baseline): " + ", ".join(unexpected_components))
    if missing_files:
        problems.append("missing protected files: " + ", ".join(missing_files))
    if changed_control_files:
        problems.append("baseline control files changed (review and recapture explicitly): " + ", ".join(changed_control_files))
    return problems, {"workspacePackageCount": len(actual), "missingPackages": missing_packages,
                      "unexpectedPackages": unexpected_packages, "componentCount": len(current_components),
                      "missingComponents": missing_components, "unexpectedComponents": unexpected_components,
                      "missingFiles": missing_files, "changedControlFiles": sorted(changed_control_files)}


def markdown_link_problems():
    problems = []
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for md in ROOT.rglob("*.md"):
        if any(part in {"target", ".git"} for part in md.parts): continue
        text = md.read_text(encoding="utf-8")
        for raw in pattern.findall(text):
            target = raw.strip().split()[0].strip("<>")
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part: continue
            dest = (md.parent / path_part).resolve()
            try: dest.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(f"{md.relative_to(ROOT)}: link escapes repository: {target}")
                continue
            if not dest.exists(): problems.append(f"{md.relative_to(ROOT)}: broken local link: {target}")
    return problems


def render_project_status(inv, items, task_problems, base_issues):
    counts = Counter(i["status"] for i in items)
    status = ["# Project Status", "", "**Image2Native — foundation scaffold**", "", f"- Workspace packages: {inv['packageCount']}", f"- Tasks: {len(items)} total · {counts['done']} done · {counts['in_progress']} in progress · {counts['blocked']} blocked · {counts['todo']} open", f"- Boundary violations: {len(inv['problems'])}", f"- Task validation problems: {len(task_problems)}", f"- Baseline problems: {len(base_issues)}", "", "## Product implementation status", "", "The compiler, OCI ingestion, RootFS reconstruction and platform execution backends are **not implemented**. This scaffold provides workspace structure, contracts, project automation and CI definitions.", "", "## Generated reports", "", "- [TODO checklist](../TODO.md)", "- [Boundary inventory](boundary-inventory.md)", "- [Checklist report](checklist.md)", "- [Baseline](baseline.md)", ""]
    return "\n".join(status).rstrip() + "\n"


def generate_all():
    REPORTS.mkdir(exist_ok=True)
    _, items, _, task_problems = load_work_items()
    inv = inventory_data()
    base = read_json(PROJECT / "baseline.json") if (PROJECT / "baseline.json").exists() else required_baseline()
    base_issues, base_current = verify_baseline() if (PROJECT / "baseline.json").exists() else ([], {})
    write_text(ROOT / "TODO.md", render_todo(items))
    write_text(REPORTS / "checklist.md", render_checklist(items))
    write_text(REPORTS / "boundary-inventory.md", render_inventory(inv))
    write_text(REPORTS / "boundary-inventory.json", json.dumps(inv, indent=2) + "\n")
    write_text(REPORTS / "baseline.md", render_baseline(base, base_current))
    write_text(REPORTS / "project-status.md", render_project_status(inv, items, task_problems, base_issues))
    return inv, task_problems, base_issues


def check_generated():
    _, items, _, task_problems = load_work_items()
    inv = inventory_data()
    if not (ROOT / "TODO.md").is_file(): return ["TODO.md is missing"] + task_problems + inv["problems"]
    base = read_json(PROJECT / "baseline.json")
    baseline_problems, baseline_current = verify_baseline()
    base_render = render_baseline(base, baseline_current)
    expected = {
        ROOT / "TODO.md": render_todo(items),
        REPORTS / "checklist.md": render_checklist(items),
        REPORTS / "boundary-inventory.md": render_inventory(inv),
        REPORTS / "boundary-inventory.json": json.dumps(inv, indent=2) + "\n",
        REPORTS / "baseline.md": base_render,
        REPORTS / "project-status.md": render_project_status(inv, items, task_problems, baseline_problems),
    }
    problems = list(task_problems) + inv["problems"] + baseline_problems
    for path, content in expected.items():
        if not path.exists(): problems.append(f"generated file missing: {path.relative_to(ROOT)}")
        elif path.read_text(encoding="utf-8") != content: problems.append(f"generated file stale: {path.relative_to(ROOT)}; run `python3 scripts/i2n.py all --write`")
    return sorted(set(problems))


def tool_status():
    result = {}
    for exe in ("python3", "cargo", "rustc", "git"):
        try:
            p = subprocess.run([exe, "--version"], text=True, capture_output=True, timeout=5)
            result[exe] = (p.stdout or p.stderr).strip().splitlines()[0] if p.returncode == 0 else "present (version check failed)"
        except (FileNotFoundError, subprocess.TimeoutExpired): result[exe] = "not found"
    return result


def command_status(_args):
    _, items, _, task_problems = load_work_items()
    counts = Counter(i["status"] for i in items)
    inv = inventory_data()
    print("Image2Native project status")
    print(f"Workspace packages : {inv['packageCount']}")
    print(f"Tasks              : {len(items)}")
    for state in ("done", "in_progress", "blocked", "todo"): print(f"  {state:14}: {counts[state]}")
    print(f"Boundary violations: {len(inv['problems'])}")
    print(f"Task graph issues  : {len(task_problems)}")
    print("\nTooling:")
    for k, v in tool_status().items(): print(f"  {k:8}: {v}")
    print("\nCompiler implementation: NOT IMPLEMENTED (scaffold only)")
    return 1 if inv["problems"] or task_problems else 0


def command_inventory(args):
    data = inventory_data()
    if args.write:
        REPORTS.mkdir(exist_ok=True)
        write_text(REPORTS / "boundary-inventory.md", render_inventory(data))
        write_text(REPORTS / "boundary-inventory.json", json.dumps(data, indent=2) + "\n")
    print(render_inventory(data))
    stale = []
    if getattr(args, "check", False):
        expected = {REPORTS / "boundary-inventory.md": render_inventory(data), REPORTS / "boundary-inventory.json": json.dumps(data, indent=2) + "\n"}
        stale = [f"generated inventory is stale or missing: {p.relative_to(ROOT)}" for p, content in expected.items() if not p.exists() or p.read_text(encoding="utf-8") != content]
        for problem in stale: print(problem, file=sys.stderr)
    return 1 if data["problems"] or stale else 0


def command_checklist(args):
    _, items, _, problems = load_work_items()
    if args.write:
        write_text(ROOT / "TODO.md", render_todo(items))
        REPORTS.mkdir(exist_ok=True)
        write_text(REPORTS / "checklist.md", render_checklist(items))
    print(render_checklist(items))
    if problems:
        print("\nChecklist validation errors:", *problems, sep="\n- ")
    return 1 if problems else 0


def command_baseline(args):
    if args.baseline_command == "capture":
        if not args.write:
            print("Refusing to update baseline without --write. Re-run: baseline capture --write", file=sys.stderr)
            return 2
        inv = inventory_data()
        _, _, _, task_problems = load_work_items()
        if inv["problems"] or task_problems:
            print("Refusing to capture baseline while inventory/task errors exist:", *(inv["problems"] + task_problems), sep="\n- ", file=sys.stderr)
            return 1
        baseline = required_baseline()
        write_text(PROJECT / "baseline.json", json.dumps(baseline, indent=2) + "\n")
        generate_all()
        print("Structural baseline captured and project reports regenerated. Review project/baseline.json and reports/.")
        return 0
    problems, current = verify_baseline()
    baseline = read_json(PROJECT / "baseline.json")
    REPORTS.mkdir(exist_ok=True)
    if args.write: write_text(REPORTS / "baseline.md", render_baseline(baseline, current))
    print(render_baseline(baseline, current))
    if problems: print("\nBaseline violations:", *problems, sep="\n- ")
    return 1 if problems else 0


def command_all(args):
    if args.write:
        inv, task_problems, base_problems = generate_all()
        print("Generated TODO.md and reports/*.md, reports/*.json")
    else:
        problems = check_generated()
        if problems:
            print("Generated output validation failed:", *problems, sep="\n- ")
            print("Run `python3 scripts/i2n.py all --write` to refresh generated files.")
            return 1
        print("Generated project views are current.")
    return command_validate(argparse.Namespace(require_rust=False, skip_rust=False, quiet=False))


def command_validate(args):
    problems = []
    # Validate all project JSON files and parse all Cargo manifests.
    for path in list(PROJECT.glob("*.json")) + list((ROOT / "schemas").glob("*.json")):
        try: read_json(path)
        except Exception as e: problems.append(f"invalid JSON {path.relative_to(ROOT)}: {e}")
    try:
        members, actual, by_package, p = inspect_members(); problems.extend(p)
        edges, p = dependency_edges(actual, by_package); problems.extend(p)
    except Exception as e: problems.append(f"workspace/boundary inventory error: {e}")
    _, _, _, task_problems = load_work_items(); problems.extend(task_problems)
    baseline_problems, _ = verify_baseline(); problems.extend(baseline_problems)
    problems.extend(check_generated())
    problems.extend(markdown_link_problems())
    if not args.skip_rust:
        cargo = shutil_which("cargo")
        if cargo:
            for cmd in ([cargo, "fmt", "--all", "--", "--check"], [cargo, "test", "--workspace"], [cargo, "clippy", "--workspace", "--all-targets", "--", "-D", "warnings"]):
                try:
                    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=600)
                    if p.returncode:
                        problems.append("command failed: " + " ".join(cmd) + "\n" + (p.stdout + p.stderr)[-6000:])
                except subprocess.TimeoutExpired: problems.append("command timed out: " + " ".join(cmd))
        elif args.require_rust:
            problems.append("Rust toolchain not found; install stable cargo/rustfmt/clippy or omit --require-rust for structural-only validation")
        elif not args.quiet:
            print("NOTE: Cargo not found; Rust fmt/test/Clippy checks were skipped. CI runs them with Rust installed.")
    if problems:
        print("VALIDATION FAILED")
        for p in problems: print("- " + p)
        return 1
    print("VALIDATION PASSED: JSON, workspace membership, boundaries, task graph, baseline and local documentation links are valid.")
    return 0


def shutil_which(name):
    from shutil import which
    return which(name)


def main():
    parser = argparse.ArgumentParser(description="Image2Native repository automation")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="show TODO, boundary and toolchain status")
    inv = sub.add_parser("inventory", help="inspect workspace crate boundaries")
    inv.add_argument("--write", action="store_true", help="write generated inventory reports")
    inv.add_argument("--check", action="store_true", help="fail when generated inventory reports are stale")
    todo = sub.add_parser("checklist", help="validate work items and show TODO checklist")
    todo.add_argument("--write", action="store_true", help="write TODO.md and checklist report")
    base = sub.add_parser("baseline", help="manage structural project baseline")
    base_sub = base.add_subparsers(dest="baseline_command", required=True)
    cap = base_sub.add_parser("capture", help="capture current structural contract")
    cap.add_argument("--write", action="store_true", help="confirm baseline mutation")
    ver = base_sub.add_parser("verify", help="verify current repo against baseline")
    ver.add_argument("--write", action="store_true", help="refresh rendered baseline report")
    all_cmd = sub.add_parser("all", help="generate or check every project report")
    all_cmd.add_argument("--write", action="store_true", help="regenerate all generated files")
    val = sub.add_parser("validate", help="validate project configuration and optional Rust workspace")
    val.add_argument("--require-rust", action="store_true", help="fail if Cargo is unavailable")
    val.add_argument("--skip-rust", action="store_true", help="skip Rust checks even if Cargo is available")
    val.add_argument("--quiet", action="store_true", help="suppress optional-tool notes")
    args = parser.parse_args()
    if args.command == "status": return command_status(args)
    if args.command == "inventory": return command_inventory(args)
    if args.command == "checklist": return command_checklist(args)
    if args.command == "baseline": return command_baseline(args)
    if args.command == "all": return command_all(args)
    if args.command == "validate": return command_validate(args)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
