# GitHub Issues, Labels and Branch Automation

The GitHub automation derives project work from `project/work-items.json`. That JSON file remains the source of truth; GitHub issues are a collaboration mirror, not a replacement for the repository checklist.

## Requirements

- Git and GitHub CLI (`gh`) installed.
- `gh auth login` completed with permission to administer repository labels and create issues.
- Repository initialized with Git and connected to the intended GitHub remote.
- Python 3.10+ (standard library only).

## Workflow

Always preview first:

```bash
python3 scripts/github_project.py plan
```

Apply after reviewing the target repository and generated issue/branch plan:

```bash
python3 scripts/github_project.py apply --confirm
```

By default, apply:

1. Resolves the GitHub repository from the current Git remote using `gh repo view`.
2. Creates or updates the required labels.
3. Creates one issue per non-completed work item.
4. Uses an embedded stable marker (`image2native-work-item:I2N-xxxx`) to avoid duplicate issues on reruns.
5. Creates one local branch per non-completed work item from the current branch.
6. Does not checkout branches and does not push them.

Optional controls:

```bash
# Use a known base branch/commit
python3 scripts/github_project.py apply --confirm --base main

# Include completed tasks too
python3 scripts/github_project.py apply --confirm --include-done

# Push newly created branches (explicit opt-in)
python3 scripts/github_project.py apply --confirm --push-branches
```

## Naming conventions

- Issue: `[I2N-0201] Finalize domain IDs, digest and target platform model`
- Branch: `feat/i2n-0201-finalize-domain-ids-digest-and-target-platform-model`
- Labels: `priority:P0`, `status:todo`, `area:compiler`, `type:feature`, `automation:managed`

Branches are created locally without checkout so the current working tree is not disturbed. If a branch already exists, it is left unchanged. The script does not automatically merge, close, assign, or modify existing issue bodies.

## Idempotency and safety

- `plan` is read-only.
- `apply` requires `--confirm`.
- Labels are reconciled with `gh label create --force`.
- Issues are matched by stable body marker, not title text.
- Existing branches are skipped.
- Remote branch pushes require `--push-branches`.
- The script never prints registry credentials or GitHub tokens.

If the GitHub repository is wrong, stop before `apply`; verify `git remote -v` and `gh repo view`.

## Suggested development loop

1. Update the task in `project/work-items.json`.
2. Run `python3 scripts/github_project.py plan`.
3. Apply GitHub synchronization.
4. Work on the task branch (checkout manually).
5. Implement tests and acceptance criteria.
6. Update task status/evidence in JSON.
7. Open a PR referencing `Closes #N` after the issue number is known.
8. Regenerate repository reports and run validation.
