# Composite Action Contracts

## Common contract

Use a Composite Action for one policy-neutral capability that always runs on
the caller's runner. Keep checkout, events, permissions, concurrency,
environments, and required-context policy in the entry workflow. Use a reusable
workflow instead when reuse needs a runner or matrix, job permissions, services,
secrets, environments, job outputs, or cross-job artifacts.

Keep the interface consistent without forcing implementations to be identical:

- Put the action at `.github/actions/<verb-object>/action.yml`.
- Use kebab-case for paths, input/output names, and step IDs.
- Name the action with an imperative, domain-qualified responsibility such as
  `Check Python package` or `Build Docker image`. Do not use bare `CI`, `Setup`,
  `Check`, `Test`, or `Build`.
- Name each step with a verb phrase for its observable result. Mention a tool
  only when the tool distinguishes the responsibility.
- Let callers own `working-directory` unless directory selection is a genuine
  reusable input. Do not add speculative inputs or outputs.
- Use `${{ github.action_path }}` to invoke files shipped beside the action;
  use `${{ github.workspace }}` only for consumer repository paths.
- Keep one blank line between sibling steps. Do not put a blank line between a
  list item and its `uses`, `with`, `shell`, `env`, or `run` properties.

The workflow context vocabulary and the action vocabulary answer different
questions. A job may have stable ID `check` and visible context `Check`, then
call `.github/actions/check-python` named `Check Python package`. Qualify a
visible context only when one event would otherwise emit duplicates, for
example `Python Check` and `Docker Check`. For matrices, qualify workers and
require one unqualified aggregate context when repository policy needs a stable
single gate.

## Embedded-code boundary

Treat `run:` as a program, regardless of YAML location. Keep only one command or
short, linear environment/output plumbing inline. Move code beside the action
when it contains parsing, loops, functions, multi-branch decisions, reusable
behavior, non-trivial quoting, or logic that merits focused tests.

Invoke a bundled program directly and preserve its exit status:

```yaml
- name: Check project metadata
  shell: bash
  env:
    EXPECTED_VERSION: ${{ inputs.expected-version }}
  run: python3 "${{ github.action_path }}/check_project.py"
```

Do not hide a language program in a Bash heredoc. Pass expressions through
`env:` instead of interpolating untrusted or syntactically significant values
into source text. Keep secrets out of command arguments and diagnostics.

## Language-specific contract

| Domain | Action example | Implementation and paired review |
| --- | --- | --- |
| Shell | `Check shell source` | Use strict failure propagation appropriate to the shell, quote expansions, and run ShellCheck. Put multi-step logic in a `.sh` file and apply `code-quality-check`. |
| Python | `Check Python package` | Put maintained logic in typed functions plus a thin `main()` returning an exit code. Run Ruff formatting/lint, strict mypy over the script, and focused tests with statement and branch coverage under `python-quality-check`. |
| Node.js | `Check Node source` | Derive Node and package-manager versions from committed metadata, replay the frozen lock, and call repository scripts. Apply `node-quality-check`; do not embed JavaScript in YAML or install unpinned tools ad hoc. |
| Docker | `Check Docker source` | Keep Dockerfile, Compose, build-context, and container checks in a Docker-owned action or script. Apply `docker-quality-check` and use a full runner when daemon access is required. |
| .NET / C# | `Test .NET package` | Derive the SDK from committed configuration, restore locked dependencies, and keep build/test/package commands aligned with the owning ecosystem or domain Skill. Put substantial PowerShell or Bash logic in tested scripts. |
| Hugo | `Check Hugo site` | Treat Hugo validation as a site responsibility while delegating Node/pnpm setup and lock semantics to `node-quality-check`; apply `hugo-quality-check` for mounts, themes, rendering, and build output. |

Add a language-specific action only when the repository has that responsibility.
Do not create one monolithic action that conditionally detects ecosystems, and
do not copy a common body across languages. Share the interface and naming
rules; let each ecosystem own its commands, lockfiles, runtime, cache, and tests.

## Verification

Run `actionlint` for workflows and use an action-aware validator or a temporary
`.github/actions/` fixture for action metadata. Run ShellCheck for embedded and
standalone shell, plus the formatter, linter, type checker, and tests required
by each maintained language. Run `pinact run --check --min-age 7` for external
actions. Finally, exercise every changed Composite Action through a
representative caller workflow; YAML parsing alone does not prove its path,
inputs, outputs, runner assumptions, or exit behavior.
