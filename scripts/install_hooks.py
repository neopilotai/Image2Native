#!/usr/bin/env python3
"""Install repository-managed Git hooks."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
try:
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        check=True,
        capture_output=True,
    )
except (FileNotFoundError, subprocess.CalledProcessError):
    print("Run `git init` in the repository before installing hooks.", file=sys.stderr)
    raise SystemExit(2)

hook = root / ".githooks" / "pre-commit"
hook.parent.mkdir(exist_ok=True)
hook.write_text(
    "#!/bin/sh\nset -eu\n"
    "if command -v python3 >/dev/null 2>&1; then PYTHON=python3; else PYTHON=python; fi\n"
    '"$PYTHON" scripts/i2n.py validate\n',
    encoding="utf-8",
)
hook.chmod(0o755)
subprocess.run(
    ["git", "config", "core.hooksPath", ".githooks"],
    cwd=root,
    check=True,
)
print("Installed .githooks/pre-commit")
