---
name: node-quality-check
description: >-
  Quality-check pnpm-managed Node.js applications, packages, dependency updates,
  runtime/toolchain configuration, and GitHub Actions. Use when creating,
  editing, or reviewing Node.js source, package.json, pnpm-workspace.yaml,
  pnpm-lock.yaml, Next.js, MUI, Node.js, or pnpm-based CI and validation workflows.
---

# Node Quality Check

## When to Use

- Use for Node.js or JavaScript/TypeScript source, package manifests, pnpm
  configuration and lockfiles, framework or UI-library upgrades, runtime/toolchain
  changes, or GitHub Actions changes.
- Use before committing or publishing a Node.js change.

## Goals

- Use pnpm exclusively and install reproducibly from the committed lockfile.
- Keep the Node.js runtime, `@types/node`, declared engines, local version files,
  CI setup, and hosted build environment mutually compatible.
- Upgrade frameworks and UI libraries as compatible sets, including intentional
  major-version changes.
- Run the smallest meaningful checks first, then expand validation when the change has
  wider production impact.
- Review dependency and automation changes as supply-chain-sensitive work.

## Workflow

1. Read the changed files, repository guidance, `package.json`,
   `pnpm-workspace.yaml`, `pnpm-lock.yaml`, Node-version files, deployment/build
   configuration, and workflows. Use pnpm; do not substitute npm, Yarn, or another
   package manager. Read [`assets/pnpm-workspace.yaml`](assets/pnpm-workspace.yaml)
   before creating or repairing a project policy file. Read
   [`assets/lint-node/action.yml`](assets/lint-node/action.yml),
   [`assets/main.yml`](assets/main.yml), and
   [`assets/pull-request.yml`](assets/pull-request.yml) before creating or repairing
   GitHub Actions lint automation.
2. Establish the compatibility envelope before choosing versions:
   - Identify the Node.js major supported by every deployment/build environment and
     its current documented compatibility. Choose a supported LTS major; do not treat
     an arbitrary newer runtime as an upgrade target.
   - Keep `engines.node`, the local version file (such as `.node-version`), CI
     `setup-node`, and the hosted builder's configured runtime aligned. Keep
     `@types/node` on the matching runtime major unless the project documents a
     deliberate reason not to.
   - For Next.js, read its release notes and peer/runtime requirements, then update
     linked `next` packages together. For MUI, update the relevant `@mui/*` packages
     as a compatible family and verify React and styling peer requirements. Treat a
     major bump as a migration: inspect breaking changes and update code/configuration
     rather than accepting a lockfile-only change.
3. Keep pnpm's supply-chain policy in `pnpm-workspace.yaml`. Start from the bundled
   template and retain a seven-day gate (`minimumReleaseAge: 10080`), strict handling
   of missing publication times, `trustPolicy: no-downgrade`, and pnpm 11's default
   strict resolution and lockfile policy rechecking, plus an explicit `allowBuilds`
   list. Add a build-script allowlist entry only after
   reviewing that package's lifecycle behavior. Do not add registry credentials,
   disable these controls, or use broad exclusions in the committed policy.
4. For dependency updates, first inventory candidates, their release dates, provenance,
   peer dependencies, runtime requirements, changelogs, and lockfile impact. Select a
   stable, compatible release; do not blindly use a dist-tag or the highest version.
   Update manifests and the lockfile together with pnpm, review the resolved graph and
   lifecycle scripts, then replay the result using `pnpm install --frozen-lockfile`.
5. Apply a cooldown exception only when explicitly authorized. Limit it to exact
   `package@version` selectors in `minimumReleaseAgeExclude`, include any inseparable
   companion packages, record why and when it can be removed in the change record, and
   retain all other policy checks. Never replace the gate with a package-wide selector,
   a wildcard, a lowered global threshold, or a disabled strict mode.
6. Keep dependency remediation narrow and reviewable. Prefer an upstream compatible
   release. Use a root-level pnpm `overrides` entry only after verifying affected
   declared ranges, peer dependencies, release age, and runtime behavior; remove it
   when no longer needed. Do not hide an unresolved compatibility issue with an override.
7. For package, runtime, pnpm, or workflow changes, use `security-check` to assess
   provenance, release age, lockfile integrity, lifecycle scripts, permissions, and
   execution behavior. Pin GitHub Actions to full commit SHAs with accurate release
   comments; verify the referenced action release satisfies the same cooldown before
   adoption. For event-owned lint CI, install the bundled composite action at
   `.github/actions/lint-node/action.yml` and the two workflow templates at
   `.github/workflows/main.yml` and `.github/workflows/pull-request.yml`. Retire a
   superseded single lint workflow only after confirming it duplicates this lint job, so
   it cannot duplicate checks. Use this shape only
   when the repository has a `.node-version` file and a `lint` script; otherwise make
   the smallest explicit substitution for its documented runtime source and validation
   command. Preserve read-only permissions, frozen install, immutable action pins, and
   branch filters; replace `main` only after confirming the repository's default branch.
   The composite action accepts `package-directory` (default `.`); use it when those
   files live below the repository root. It reads `.node-version` and `packageManager`
   from that directory as the runtime and pnpm sources of truth, uses that directory's
   lockfile for caching, and removes only its `node_modules` before returning. Omit
   `workflow_dispatch`, keep default-branch pushes uncancelled, and cancel only
   superseded pull-request or merge-queue runs.
   After installation, run `actionlint` against both workflows and `pinact run --check
   --min-age 7` against the installed workflows and composite action. Treat a failure as
   a blocker. Record each external action's full SHA, release tag, publisher/provenance,
   release-age result, and the validation results in the pull request or equivalent
   change record.
8. Run the repository's documented type checking, linting, tests, and build commands
   with pnpm. Start with checks closest to the changed code, then run a production build
   for routing, bundling, rendering, deployment configuration, framework, UI-library,
   or other cross-cutting changes. If a check fails, isolate the narrow cause and rerun
   it before widening validation. Record blockers instead of claiming skipped checks
   passed.
9. Summarize the selected compatibility envelope, pnpm policy and exceptions, commands,
   checks and results, supply-chain review scope, and every skipped check with its reason.

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
