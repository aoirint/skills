# Canonical Repository Templates

Use the bundled templates only when the target repository adopts the matching
release contract. They are exact reusable files, not examples to rewrite per
repository.

## Bundled templates

The mapping in `assets/template-map.json` installs these template groups:

- `github-generate-version`: derive stable, prerelease, and edge versions and
  synchronize project and Thunderstore manifest versions.
- `github-publish-thunderstore-action` and
  `github-publish-thunderstore-script`: submit one prebuilt package to
  Thunderstore without rebuilding it.

The version template requires the marker and file contract it documents. The
Thunderstore templates apply only when the evidence ledger selects
Thunderstore and the release workflow supplies the required reviewed inputs.

## Initial provenance

The canonical assets were seeded from portable files that matched across
reviewed first-party consumers. Their initial Git blob identities are recorded
without making those consumers part of the quality contract:

| Template | Initial Git blob |
| --- | --- |
| `github-generate-version` | `0535faef6bfa4195e015c3a8c1e6c575d3e2c9ec` |
| `github-publish-thunderstore-action` | `18dbef7efb310fe4cf03d7318cbd779c45ea5638` |
| `github-publish-thunderstore-script` | `0e3bcb2ae5ff850e1a25db6591565ec0f67af0ee` |

After this import, `aoirint/skills` is the source of truth; consumer history is
evidence, not an upstream to copy automatically.

## Adopt or verify

Run the script from the installed Skill. Select only templates enabled by the
repository contract; omitting `-Template` selects all bundled templates.

```powershell
& .agents/skills/bepinex-mono-mod-quality-check/scripts/sync_templates.ps1 `
  -RepoRoot . -Apply `
  -Template github-generate-version
```

Use the same selection in contributor documentation and CI, replacing
`-Apply` with `-Check`. The check fails when a selected destination is missing
or modified. YAML must match exactly after Git-policy line-ending
normalization; executable shell files must match byte-for-byte, including LF.

## Improve without drift

1. Name `aoirint/skills` and the files under this Skill's `assets/` directory
   as the canonical source. Treat consumer copies as generated from it.
2. Inspect all known consumers before changing the template. Separate a
   portable improvement from target-specific paths, names, credentials,
   categories, or policy.
3. Edit the canonical asset first. Do not promote an unvalidated consumer copy
   merely because it is newer.
4. Apply the candidate to a scratch consumer and run its parsing, ShellCheck,
   actionlint, pinact, build, package, archive, and dry-run checks as applicable.
5. Apply the validated asset to every opted-in consumer with the sync script.
   Keep a target-specific variation outside the template and document why that
   consumer cannot use exact synchronization.
6. Run `-Check` with the same template selection in every consumer, followed
   by its repository checks. Every selected file must satisfy the comparison
   mode declared in `template-map.json`; do not weaken that mode downstream.
7. Commit the canonical change before or with linked rollout PRs. Record the
   canonical commit, consumer list, intentional exclusions, and validation
   results so later maintenance can find the complete rollout set.

Never edit `.agents/skills/` in this repository directly. Change the canonical
`.apm/skills/` asset, then regenerate deployed Skill files with APM.
