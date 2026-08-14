# Hugo build contract

Use this reference after identifying a pnpm-managed Hugo site.

## Runtime and builder

- Treat `.node-version` and `packageManager` as the committed Node.js and pnpm
  contracts. Keep `engines.node` compatible with them and validate with
  `engineStrict` enabled.
- Inspect the hosted builder rather than assuming its runner default. Cloudflare
  Pages supports `.node-version` and `NODE_VERSION`, but does not infer Node.js or
  package-manager versions from `package.json`. Use an officially supported LTS
  runtime and record the selected version and source in the change record.
- When Hugo comes from `hugo-extended` or another package, pin it in
  `package.json`, then invoke it through the repository script rather than a
  globally installed binary.

## Mounts, themes, and local assets

- Inventory configured and effective `module.mounts` source and target pairs.
  Hugo can suppress default mounts when custom mounts are defined, with
  different retention rules for project configuration and imported modules.
  Do not infer the effective graph from the configuration file or from another
  Hugo version. After the frozen dependency install, run the pinned Hugo,
  normally `pnpm exec hugo config mounts`, and confirm that every component
  directory the project uses is mounted. See the official
  [Hugo module mount documentation](https://gohugo.io/configuration/module/#mounts)
  for the current default-mount rules.
- Explicitly add a required default pair when it is absent from the effective
  graph. For example, preserve repository-owned files under `static/` with a
  `static` source mounted to the `static` target. Apply the same check to
  `archetypes`, `assets`, `content`, `data`, `i18n`, and `layouts` when the
  project uses those component directories. Do not mix mount configuration
  with the legacy component directory settings that Hugo documents as
  incompatible with mounts.
- Treat mount inspection as necessary but insufficient. Prefer a new empty
  temporary destination for validation. Use `--cleanDestinationDir` only after
  confirming that the destination is disposable generated output with no user
  work; do not delete an existing destination merely to prepare the check.
  Verify one or more project-owned sentinel files from source to output, using
  a byte comparison or digest where appropriate.
  A successful build, a nonzero static-file count, or similarly named files
  supplied by a theme or imported module does not prove that the project's
  mount is active.
- A package-directory mount requires the package to be installed before Hugo
  runs.
- Initialize a declared theme submodule recursively before a local build.
- For a replaced CDN asset, treat the URL's version as inventory only. Select a
  fixed package version after registry release-date, provenance, compatibility,
  and cooldown review, or an explicit maintainer exception; never invent a
  version. Mount the selected distribution to a stable static target when that
  avoids committing copied files. Verify the
  generated HTML references only local asset URLs and that each CSS-referenced
  font, script, and stylesheet exists in the output directory.
- Record the package version, registry integrity, source, license, and emitted
  path in `THIRD_PARTY_NOTICES.md`. Do not confuse article links or literal code
  examples with runtime dependencies when searching generated output.

## CI adoption

Before copying the bundled entry workflows from
`github-actions-quality-check`, ensure the project has a `.node-version`,
`packageManager`, `pnpm-lock.yaml`, `lint` script, and `build` script. Keep a
submodule checkout only when the configured theme uses one. Pass
`package-directory` and optional `lockfile-path` to the composite action for a
package below the repository root or a shared lockfile.
