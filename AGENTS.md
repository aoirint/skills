# Repository Guide

## Layout

- `src/<skill-name>/SKILL.md` is the canonical instruction file for a skill.
- `src/<skill-name>/agents/openai.yaml` supplies the Codex interface metadata.
- Put detailed, optional material in `references/` and deterministic helpers in
  `scripts/`.
- Keep the repository-level [README.md](README.md) as the public skill index.

## Maintaining Skills

When adding or substantially changing a skill:

1. Keep the directory name and the `name` in `SKILL.md` in lowercase
   hyphen-case.
2. Make the frontmatter description state both the capability and its trigger
   conditions. Keep `agents/openai.yaml` aligned with that description.
3. Keep the default workflow in `SKILL.md`; move detailed variants and
   examples to files directly linked from `references/`.
4. Add, update, or remove the corresponding row in the README skill table.
   The table must link to the canonical `SKILL.md`.
5. For a new or materially revised skill, run the applicable quality check and
   scenario-based validation. Test changed scripts with a representative
   invocation.

## Documentation Checks

Before handing off documentation changes:

1. Confirm every `src/*/SKILL.md` has one README table row and no stale row
   remains.
2. Confirm each listed link resolves to the canonical skill file.
3. Run `git diff --check` and review the rendered Markdown tables.

## Git Practice

- Treat uncommitted or untracked files outside the task as user work.
- Use an isolated worktree for implementation work unless the user requests a
  different workspace arrangement.
- Keep commits focused. Do not rewrite published history unless explicitly
  requested.
