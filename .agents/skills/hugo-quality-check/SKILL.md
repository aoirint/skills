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
   substitute another package manager. Copy `assets/markdownlint-cli2.yaml` to
   `.markdownlint-cli2.yaml` for repository documentation and
   `assets/markdownlint-cli2-content.yaml` to
   `.markdownlint-cli2-content.yaml` for Hugo articles. The repository config
   preserves the shared prose baseline while excluding `content/` and Hugo's
   default `public/` output; the content config scopes renderer-owned HTML to
   `content/**/*.md`. If `publishDir` or the content directory differs, replace
   the corresponding path. Add a theme or broader renderer exception only
   after repository evidence shows that the narrower exception is required.
   Record every non-default content path, output path, theme exclusion, and
   renderer exception in the repository's `AGENTS.md`, including its evidence
   and ownership boundary. Keep a concise matching rationale beside the config
   rule so future maintainers can reconcile policy and implementation.
2. Inventory the build contract before editing it: content source and mount
   targets, theme source, build output, package scripts, local static assets,
   and hosted-builder runtime configuration. For a Git submodule theme, run
   `git submodule update --init --recursive` before validating the rendered site.
3. Keep `packageManager` and `.node-version` as the pnpm and Node.js sources of
   truth. Align `engines.node`, CI, and hosted builders. Choose a supported LTS
   runtime from official evidence and validate with `engineStrict` enabled. For
   Cloudflare Pages, confirm the configured build image and use `.node-version` or
   `NODE_VERSION`; Pages does not infer these contracts from `package.json`. Read
   [`references/hugo-build-contract.md`](references/hugo-build-contract.md) and apply
   `$node-quality-check` before choosing a runtime or build tool version.
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
5. When custom mounts exist or mount behavior changes, inspect the effective
   mount graph with the repository's pinned Hugo, normally
   `pnpm exec hugo config mounts`. Do not assume that component defaults remain
   active because their directories still exist. Compare every project-owned
   component directory the site uses with the effective mounts, and explicitly
   restore any required default source and target pair that is absent. Build to
   a clean destination and verify project-owned sentinel files in the output;
   theme or module files can otherwise make an incomplete static mount look
   successful. Follow the mount checklist in
   [`references/hugo-build-contract.md`](references/hugo-build-contract.md).
6. When package dependencies change, finalize the pnpm workspace policy before
   resolving the graph. Update the manifest and lockfile together, review direct and
   transitive changes, then replay it with `pnpm install --frozen-lockfile` and run
   the full `pnpm audit --json`. Keep a release-age exception only for an exact,
   reviewed vulnerability fix; do not use one for ordinary dependency updates. Run
   every defined check, normally `pnpm run lint` and `pnpm run build`.
   Inspect generated HTML for the intended local asset URLs and for absence of
   replaced CDN URLs; verify mounted CSS, JavaScript, and font files exist in
   the generated output.
7. For reusable CI, apply `github-actions-quality-check` and its event-owned
   workflow template contract. For an APM-managed repository, also apply
   `apm-workflow`; the outer Hugo source-check action must run `apm audit --ci`
   and Markdown lint alongside the site checks. Read
   [`assets/github/actions/check-hugo-site/action.yml`](assets/github/actions/check-hugo-site/action.yml),
   copy the Node-owned setup action from `node-quality-check`, and install them
   at `.github/actions/check-hugo-site/action.yml` and
   `.github/actions/setup-node-locked/action.yml`. Do not copy the setup
   implementation into this Skill. Retire a
   superseded workflow only after confirming its complete event and lifecycle
   responsibility is duplicated. The composite reads `.node-version` and
   `packageManager`, replays the lockfile, runs `lint` then `build`, and removes
   only the package directory’s `node_modules`.
8. Preserve `submodules: recursive` in every Hugo checkout.
9. Summarize the build contract, runtime compatibility evidence, external asset
   provenance, commands and results, and every skipped validation with its
   reason.

## Resources

- [`references/hugo-build-contract.md`](references/hugo-build-contract.md): Hugo
  mounts, runtime sources, local asset checks, and hosted-builder evidence.
- `assets/markdownlint-cli2.yaml` and
  `assets/markdownlint-cli2-content.yaml`: separate prose-baseline validation
  for repository documentation and Hugo articles. Regenerate both from the prose asset with
  `scripts/render_markdownlint_config.py`; run the script with `--check` to
  detect baseline drift.
- `scripts/render_markdownlint_config.py`: deterministic renderer and drift
  check for the Hugo Markdown configuration.
- `assets/github/actions/check-hugo-site/action.yml`: reusable Hugo validation
  action used with the Node setup action from `node-quality-check` and the
  entry workflows from `github-actions-quality-check`.
