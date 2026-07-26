---
name: node-quality-check
description: >-
  Quality-check Node.js application, package, and build-tool changes. Use when
  creating, editing, or reviewing Node.js source, dependency, configuration, or
  package-manager validation workflows.
---

# Node Quality Check

## When to Use

- Use for Node.js or JavaScript/TypeScript source, package manifest, lockfile,
  build-tool, framework, or validation-workflow changes.
- Use before committing or publishing a Node.js change.

## Goals

- Install dependencies reproducibly with the package manager and lockfile selected by
  the repository.
- Run the smallest meaningful checks first, then expand validation when the change has
  wider production impact.
- Review dependency and automation changes as supply-chain-sensitive work.

## Workflow

1. Read the changed files, package manifest, lockfile, package-manager configuration,
   and repository guidance. Use the package manager indicated by the committed lockfile
   and configuration; do not substitute another package manager.
2. Install dependencies with the package manager's lockfile-enforcing mode when
   dependencies are missing or stale. Do not modify the lockfile during a verification
   install unless the task explicitly changes dependencies.
3. Run the repository's documented type checking, linting, tests, and build commands.
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
7. Summarize the package-manager command, checks run, results, supply-chain review
   scope, and each skipped check with its reason.

## Default Validation Shape

Use the repository's script names. A typical sequence is:

```shell
<package-manager> install <lockfile-enforcing-option>
<package-manager> run typecheck
<package-manager> run lint
<package-manager> test
<package-manager> run build
```

Run only scripts that the repository defines, and record intentionally omitted commands.
