---
name: hugo-quality-check
description: >-
  Quality-check pnpm-managed Hugo sites, including content, layouts, theme
  submodules, build-time assets, runtime/toolchain configuration, and GitHub
  Actions. Use when creating, editing, or reviewing Hugo configuration, content,
  layouts, package.json, pnpm-lock.yaml, local static assets, or Hugo CI.
---

# Hugo Quality Check

## When to Use

- Use for a Hugo site’s content, configuration, layouts, themes, static assets,
  package-managed build tools, or validation workflows.
- Use before committing a Hugo build, deployment, or dependency change.

## Goals

- Build the same static site locally and in CI from a pinned pnpm lockfile.
- Keep themes, mounted assets, Node.js, pnpm, Hugo, and the hosted builder
  compatible and explicitly sourced.
- Keep browser runtime assets local, versioned, licensed, and reproducible.
- Reuse one least-privilege validation boundary across push, pull request, and
  merge-queue events.

## Workflow

1. Read repository guidance, the Hugo configuration, content mounts, layouts,
   `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, Node-version files,
   theme declaration, submodule metadata, and workflows. Use pnpm; do not
   substitute another package manager.
2. Inventory the build contract before editing it: content source and mount
   targets, theme source, build output, package scripts, local static assets,
   and hosted-builder runtime configuration. For a Git submodule theme, run
   `git submodule update --init --recursive` before validating the rendered site.
3. Keep `packageManager` and `.node-version` as the pnpm and Node.js sources of
   truth. Align `engines.node`, CI, and hosted builders. For Cloudflare Pages,
   confirm the configured build image and use `.node-version` or `NODE_VERSION`;
   read [`references/hugo-build-contract.md`](references/hugo-build-contract.md)
   before choosing a runtime or build tool version.
4. Treat a browser asset previously loaded from a CDN as a supply-chain change.
   Treat its URL and version as inventory evidence, not an approval to adopt that
   package release. Select an exact version only after registry/release-date,
   provenance, compatibility, and cooldown review, or an explicit maintainer
   exception; never invent a version. Prefer a fixed package and a Hugo module
   mount or asset pipeline that emits a local URL at build time. Do not add a
   copied distribution unless a committed artifact is explicitly required.
   Record source, exact version, integrity, license, and output path in
   `THIRD_PARTY_NOTICES.md`; use `security-check` for provenance, release age,
   integrity, and runtime behavior.
5. When package dependencies change, update the manifest and lockfile together,
   review the resolved graph, then replay it with `pnpm install --frozen-lockfile`.
   Run every defined check, normally `pnpm run lint` and `pnpm run build`.
   Inspect generated HTML for the intended local asset URLs and for absence of
   replaced CDN URLs; verify mounted CSS, JavaScript, and font files exist in
   the generated output.
6. For reusable CI, read
   [`assets/github/actions/lint-hugo/action.yml`](assets/github/actions/lint-hugo/action.yml),
   [`assets/github/workflows/main.yml`](assets/github/workflows/main.yml), and
   [`assets/github/workflows/pull-request.yml`](assets/github/workflows/pull-request.yml).
   Install the composite action at `.github/actions/lint-hugo/action.yml` and
   copy the two workflows unchanged except for the confirmed default branch or
   package directory. Retire a superseded lint workflow only after confirming
   it duplicates this job. The composite reads `.node-version` and
   `packageManager`, replays the lockfile, runs `lint` then `build`, and removes
   only the package directory’s `node_modules`.
7. Keep default-branch pushes uncancelled. Cancel only superseded pull-request
   and merge-queue runs. Use `contents: read`, checkout with persisted
   credentials disabled and `submodules: recursive`, full-SHA Action pins with
   release comments, named `uses:` steps, and no `workflow_dispatch` for normal
   validation. Run `actionlint` and `pinact run --check --min-age 7` after
   installing the templates.
8. Summarize the build contract, runtime compatibility evidence, external asset
   provenance, commands and results, and every skipped validation with its
   reason.

## Resources

- [`references/hugo-build-contract.md`](references/hugo-build-contract.md): Hugo
  mounts, runtime sources, local asset checks, and hosted-builder evidence.
- `assets/github/`: reusable event-owned Hugo validation action and workflows.
