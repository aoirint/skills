# Repository Guide

## Layout

- `.apm/skills/<skill-name>/SKILL.md` is the canonical source for a skill.
- `.apm/skills/<skill-name>/agents/openai.yaml` supplies its Codex interface
  metadata.
- `.agents/skills/` is APM-managed deployment output. Do not edit it by hand;
  regenerate it with APM from the canonical source and reviewed dependencies.
- Keep detailed optional material in a skill's `references/` directory and
  deterministic helpers in its `scripts/` directory.
- Keep repository-level documents such as [README.md](README.md),
  [LICENSE](LICENSE), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) at
  the root. The README is the public skill index.

## Maintaining Skills

When adding or substantially changing a skill:

1. Keep the directory name and the `name` in `SKILL.md` in lowercase
   hyphen-case. When the target is identifiable, put it before the action or
   workflow (for example, `lethal-company-analyze` and `apm-usage`).
2. Make the frontmatter description state both the capability and its trigger
   conditions. Keep `agents/openai.yaml` aligned with that description.
3. Keep the default workflow in `SKILL.md`; move detailed variants and
   examples to files directly linked from `references/`.
4. Add, update, or remove the corresponding README table row. It must link to
   `.apm/skills/<skill-name>/README.md`.
5. Keep each skill's user-facing `README.md` limited to `Overview` and
   `Install`. Use a local `apm install aoirint/skills/.apm/skills/<skill-name>`
   command there. Put agent instructions only in `SKILL.md` and its resources.
6. Run the applicable skill and documentation quality checks. For a new or
   materially revised skill, also run scenario-based validation and test any
   changed scripts with a representative invocation.

## APM and Third-Party Content

- This repository publishes APM-managed skills for OpenAI Codex. Keep the
  `targets` entry in `apm.yml` scoped to `codex`; adding a target changes the
  public deployment scope and requires explicit maintainer approval.
- Keep the root README's collection command global. Individual skill READMEs
  use local installation so the dependency is recorded in the consumer project.
- Preserve the existing `apm.yml`; do not run `apm init --yes` in this
  repository.
- Treat `apm.yml`, `apm.lock.yaml`, and `.agents/` deployment output as one
  reviewable unit. After a source or dependency change, run `apm lock`, review
  the lockfile, run `apm install --frozen`, then run `apm audit --ci`.
- Remote dependencies require a full commit SHA, source review, and the
  seven-day cooldown. For a monorepo subdirectory, calculate the cooldown from
  the last commit affecting that subdirectory.
- Unless otherwise specified, repository content is MIT licensed. Before
  committing third-party APM-deployed content, record its source, pinned SHA,
  license, and required notices in `THIRD_PARTY_NOTICES.md`. A third-party
  license or notice overrides the default for that content.
- Do not place license notices inside `.agents/skills/`.

## Documentation Checks

Before handoff:

1. Confirm every `.apm/skills/*/SKILL.md` has one README table row and no stale
   row remains.
2. Confirm each listed link resolves to the corresponding skill README.
3. Run `git diff --check` and review Markdown tables and APM-generated diffs.

## Git Practice

- Treat uncommitted or untracked files outside the task as user work.
- Use an isolated worktree for implementation work unless the user requests a
  different workspace arrangement. Do not remove another worktree unless the
  user explicitly asks.
- Keep commits focused; do not combine unrelated changes or rewrite published
  history unless explicitly requested.
