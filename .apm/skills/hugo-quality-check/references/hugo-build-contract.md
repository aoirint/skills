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

- Inventory `module.mounts` source and target pairs. A package-directory mount
  requires the package to be installed before Hugo runs.
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

Before copying the bundled workflows, ensure the project has a `.node-version`,
`packageManager`, `pnpm-lock.yaml`, `lint` script, and `build` script. Keep a
submodule checkout only when the configured theme uses one. Pass
`package-directory` and optional `lockfile-path` to the composite action for a
package below the repository root or a shared lockfile.
