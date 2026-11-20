# TODO, Checklist and Inventory Automation

## Commands

| Command | Effect |
|---|---|
| `python3 scripts/i2n.py status` | Summarize task and implementation state |
| `python3 scripts/i2n.py checklist` | Validate task graph and show checklist |
| `python3 scripts/i2n.py checklist --write` | Regenerate `TODO.md` and checklist report |
| `python3 scripts/i2n.py inventory` | Validate crate boundaries and show inventory |
| `python3 scripts/i2n.py inventory --write` | Regenerate inventory reports |
| `python3 scripts/i2n.py baseline verify` | Check protected baseline contracts |
| `python3 scripts/i2n.py baseline capture --write` | Intentionally refresh structural baseline |
| `python3 scripts/i2n.py all --write` | Regenerate all project reports |
| `python3 scripts/i2n.py validate` | Run JSON, task, boundary, baseline and doc-link checks |

The `--write` flag updates generated files. Without it, commands verify that checked-in generated views are current.
