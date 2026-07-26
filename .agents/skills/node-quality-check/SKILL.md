---
name: node-quality-check
description: >-
  Quality-check pnpm-managed Node.js application, package, and build-tool changes.
  Use when creating, editing, or reviewing Node.js source, dependencies,
  configuration, pnpm-lock.yaml, or pnpm-based validation workflows.
---

# Node Quality Check

## When to Use

- Use for Node.js or JavaScript/TypeScript source, package manifest, lockfile,
  build-tool, framework, or validation-workflow changes.
- Use before committing or publishing a Node.js change.

## Goals

- Install dependencies reproducibly with pnpm and the committed lockfile.
- Run the smallest meaningful checks first, then expand validation when the change has
  wider production impact.
- Review dependency and automation changes as supply-chain-sensitive work.

## Workflow

1. Read the changed files, `package.json`, `pnpm-lock.yaml`, workspace and pnpm
   configuration, and repository guidance. Use pnpm; do not substitute npm or another
   package manager.
2. For source-only validation, install dependencies with `pnpm install --frozen-lockfile`
   when dependencies are missing or stale. Do not modify `pnpm-lock.yaml` during a
   verification install. If the task changes dependencies, update the manifest and
   lockfile together using the repository's documented pnpm command, review the lockfile
   diff, then replay the result with `pnpm install --frozen-lockfile`.
3. Run the repository's documented type checking, linting, tests, and build commands
   with pnpm.
   Start with checks closest to the changed code, then run a production build when the
   change affects routing, bundling, rendering, application configuration, or another
   cross-cutting behavior.
4. For a dependency change, inspect the manifest and lockfile together. Confirm that
   additions and updates are intentional, compatible with the supported runtime, and
   do not introduce unexpected install or lifecycle-script behavior.
5. For newly introduced or updated packages, GitHub Actions, or downloaded tools, use
   `security-check` to assess provenance, release age, integrity pins, permissions, and
   execution behavior. Pin GitHub Actions to full commit SHAs with accurate version
   comments.
6. If a check fails, isolate and correct the narrow cause, then rerun that same check
   before widening validation. Record environmental blockers instead of claiming a
   skipped check passed.
7. Summarize the pnpm commands, checks run, results, supply-chain review
   scope, and each skipped check with its reason.

## Default Validation Shape

Use the repository's script names. A typical sequence is:

```shell
pnpm install --frozen-lockfile
pnpm run typecheck
pnpm run lint
pnpm test
pnpm run build
```

Run only scripts that the repository defines, and record intentionally omitted commands.
