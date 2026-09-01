---
name: mise-workflow
description: >-
  Configure and review mise-managed tool versions, lockfiles, task interfaces,
  installation, updates, and CI execution. Use when creating or editing
  mise.toml, mise.lock, .mise/tasks, mise version policy, or repository task
  conventions; pair with the ecosystem Skill that owns language dependencies.
---

# mise Workflow

## When to Use

- Use for repository-owned mise configuration, tool pins, lockfiles, tasks,
  installation instructions, migrations from other tool-version managers, and
  CI that installs or invokes mise.
- Pair with the applicable ecosystem Skill for package-manager commands,
  language-version compatibility, tests, builds, and distribution behavior.
- Pair with `security-check` whenever mise or a managed tool is introduced,
  updated, downloaded, locked, or executed.

## Goals

- Make one reviewed repository configuration describe developer and CI tools.
- Resolve immutable artifacts with reviewer-visible URLs, checksums, provenance,
  platform coverage, and cooldown evidence.
- Give contributors a small, predictable task interface without hiding mutation
  or weakening ecosystem lockfiles.
- Keep secrets and unrelated parent variables outside application processes.

## Responsibility Boundaries

This Skill owns mise itself, `[tools]`, `mise.lock`, mise task composition, and
the mapping from repository operations to stable task names. It does not decide
which Python, Node.js, Java, or other runtime is compatible, nor which package
manager commands establish that ecosystem's quality baseline.

Use `github-actions-quality-check` for workflow events, permissions, runners,
and action pins. Use `bws-workflow` or another provider-specific Skill for
secret retrieval and credential lifecycle; this Skill owns only the task and
child-process exposure boundary.

## Workflow

1. **Inventory the existing contract.**
   - Read repository guidance, every mise configuration and task directory,
     version files, package-manager locks, workflows, and developer commands.
   - Before executing an existing mise binary, establish that its origin and
     exact version were already reviewed. Then run `mise --version`,
     `mise config ls`, `mise tasks ls`, and relevant help instead of relying on
     remembered syntax. Treat an unavailable reviewed binary as a bootstrap
     blocker, not permission to run an installer.
   - Distinguish the mise bootstrap version, managed tool versions, package
     dependencies, and task behavior. Do not collapse them into one update.
2. **Select and pin mise.**
   - Read [tool and lock management](references/tool-and-lock-management.md).
   - Select the newest compatible mise release that passed the repository's
     cooldown and provenance review. Record the exact version; do not use
     `latest`, an unbounded installer, or `mise self-update` as repository
     policy.
   - Use `min_version` for parser compatibility and an exact preflight or
     exact CI installer input when the repository requires one reviewed mise
     implementation. Make every public task depend on that preflight. A minimum
     alone is not an immutable execution pin.
3. **Manage tools through mise.**
   - Put supported developer and runtime tools in `[tools]` with exact reviewed
     versions. Keep required ecosystem version files aligned when another tool
     consumes them; do not create competing selectors.
   - Generate `mise.lock` for every supported platform, enable locked behavior,
     inspect its complete URLs, checksums, provenance, and backend identities,
     then install with `mise install --locked`.
   - Review the final downloadable artifact's own publication time. A mature
     language release can still resolve to a newly produced runtime bundle that
     has not completed cooldown.
4. **Define the task interface.**
   - Read [task conventions](references/task-conventions.md).
   - Preserve established compatible names. For a new baseline, use `sync`,
     `format`, and `check` with the semantics in that reference.
   - Keep update tasks explicit and separate from reproduction and validation.
     A routine task must fail rather than rewrite a tool or package lockfile.
5. **Contain execution.**
   - Prefer short declarative tasks. Move substantial branching or parsing to
     a portable tested repository-owned script. A security boundary may stay in
     a task only while its complete behavior remains short enough to exercise
     through fake executables without source-text assertions.
   - Use mise environment denial and explicit allowlists for commands that must
     not inherit the complete parent environment. Retrieve only required
     secrets, remove bootstrap credentials and identifiers, and re-enter the
     application task with only its declared values.
     Verify the exact syntax with the pinned mise version and inspect the final
     application process after every mise/config layer. If the denial cannot be
     demonstrated with a sentinel-variable probe, block the isolation claim.
   - Never place secret values in task definitions, command arguments, cache
     keys, generated lockfiles, or diagnostic output.
     Disable shell tracing and verbose output on secret-bearing paths.
6. **Align local and CI use.**
   - Make CI install the exact reviewed mise version and execute the same
     repository tasks as local development. Keep workflow-side trust controls
     with `github-actions-quality-check`.
   - Prefer `mise install --locked` followed by `mise run check`; do not let CI
     resolve a newer tool or use hidden validation flags.
7. **Verify and report.**
   - Run `mise tasks validate`, inspect `mise tasks info` for changed tasks,
     replay `mise install --locked`, and exercise every changed task with safe
     fixtures or sandboxed inputs.
   - Confirm reproduction tasks leave all lockfiles unchanged, validation tasks
     do not format or update, and secret-consuming child processes receive only
     the documented environment.
     Exercise live operator tasks only when explicitly authorized; routine
     `check` and CI use fake providers for secret-boundary tests.
   - Report exact mise and tool versions, supported platforms, artifact and
     cooldown review, task results, lockfile diff, unavailable evidence, and
     any approved exception.

## Completion Checklist

- mise and managed tools use exact reviewed versions and locked artifacts.
- Every supported platform has the required lock metadata and provenance.
- Secondary ecosystem version files agree with the mise tool contract.
- `sync`, `format`, `check`, and update tasks have distinct, documented effects.
- Local and CI commands use the same task interface without implicit updates.
- Secret-bearing tasks fail closed and constrain the application environment.
- The relevant ecosystem, security, test, and GitHub Actions checks passed or
  have concrete blockers.
