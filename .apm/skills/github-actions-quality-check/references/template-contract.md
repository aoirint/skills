# GitHub Actions Template Contract

## Purpose

Use the bundled baseline only when a repository needs event-owned source
validation. It intentionally does not define ecosystem setup, lint, test,
build, package, or release commands.

## Files

| Skill asset | Consumer path | Contract |
| --- | --- | --- |
| `assets/github/workflows/pull-request.yml` | `.github/workflows/pull-request.yml` | Validate proposed source and merge-queue commits; cancel superseded runs. |
| `assets/github/workflows/main.yml` | `.github/workflows/main.yml` | Revalidate the exact integrated commit; never cancel it. |
| `assets/github/actions/install-workflow-tools/action.yml` | `.github/actions/install-workflow-tools/action.yml` | Install checksum-verified ShellCheck, actionlint, and pinact in runner-temporary paths. |

Both workflows call `.github/actions/lint-source`. Supply that action from the
ecosystem Skill or repository contract. Keep its name narrow and its commands
equal to documented clean-clone validation.

## Allowed substitutions

- Replace `main` only with the confirmed protected integration branch.
- Replace `ubuntu-slim` only after applying `runner-selection.md` and proving
  the job needs a different image or platform.
- Add a `test` job when tests require a distinct runner or responsibility.
- Add direct `needs` edges from later jobs to every required source gate.
- Update tool versions and SHA-256 values together only after `security-check`
  verifies provenance, runtime behavior, exact asset, and cooldown eligibility.

Do not combine the two entry workflows, remove `merge_group` while its checks
are required, add routine manual dispatch, enable broad write permissions, or
make consumer CI depend on an installed Skill path.

## Adoption checks

1. Inventory existing workflows and retire only a workflow whose full event and
   lifecycle responsibility is duplicated by the new files.
2. Copy the assets and add the repository-owned `lint-source` action.
3. Name all `uses:` steps for their responsibility.
4. Run ShellCheck for every standalone changed shell script, actionlint for all
   workflows and local actions, and `pinact run --check --min-age 7`.
5. Observe successful pull-request and integration-branch jobs before making
   their job names required status contexts.
