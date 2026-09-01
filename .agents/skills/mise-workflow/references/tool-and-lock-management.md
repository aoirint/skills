# Tool and lock management

## Contents

- [Sources of truth](#sources-of-truth)
- [Adoption and update](#adoption-and-update)
- [Lock and install](#lock-and-install)
- [Migration](#migration)

## Sources of truth

- `mise.toml` owns exact repository tool selections and task declarations.
- `mise.lock` owns platform-specific resolved artifacts, URLs, checksums,
  provenance, backends, and specifier bindings.
- A language version file remains only when an ecosystem tool, editor, or
  hosting platform consumes it. Keep its value equal to the mise selection and
  validate that equality; do not give it an independent range or update flow.
- A package-manager lock owns libraries. Do not represent Python packages,
  npm packages, Cargo crates, or equivalent application dependencies as mise
  tools merely to centralize configuration.

`min_version` rejects older parsers but permits every newer mise release. When
one reviewed mise implementation is required, add an exact preflight used by
all public tasks and use the same exact version in CI installation.

mise is the bootstrap and cannot install itself through one of its own tasks.
Obtain or select the reviewed mise executable first. Only then may locked-mode
mise resolve managed tools and run repository tasks.

## Adoption and update

Apply `security-check` before resolution or execution.

1. Identify the canonical publisher and repository for mise or the managed
   tool, its exact version, release time, supported platforms, runtime behavior,
   and license.
2. Require the repository cooldown for both the logical tool release and the
   final platform artifact. Backends may repackage an older release in a newer
   executable bundle.
3. Inspect release notes and compatibility before changing `mise.toml`.
4. Resolve only the intended tools. Review backend changes and every `mise.lock`
   platform delta; a backend change is a new distribution path.
5. Treat floating selectors as discovery inputs only. Replace them with exact
   reviewed versions before committing.

Do not use `mise up`, `mise upgrade`, `mise use ...@latest`, or
`mise self-update` as an ordinary reproduction command. They are update
operations and require an explicit reviewed scope.

## Lock and install

Generate locks with the exact reviewed mise executable. When selecting from a
fuzzy candidate list, apply mise's minimum-release-age option before choosing a
version, then replace the selector with the exact result. The age option does
not protect an already exact selector; retain independent release evidence.

Lock every platform that the repository claims to support. Enable locked mode
only after the first candidate lock exists and has been reviewed. Thereafter:

```shell
mise lock --dry-run
mise install --locked
```

Use a targeted `mise lock <tool>` only for an authorized update. Reject:

- missing platform entries;
- mutable or unexpected download URLs;
- absent or changed checksums without source review;
- provenance downgrade;
- a newly selected backend or installer;
- newly published repackaged artifacts still inside cooldown; or
- a frozen install that rewrites configuration or locks.

For a foreign platform, inspect the lock metadata against the publisher's
release API, checksums, and provenance, then require a native CI or maintainer
run before claiming install/runtime compatibility. Resolving a foreign URL on
one host is not execution evidence for that target.

Locked auto-install may populate the tool directory before a task. Permit that
only from the reviewed `mise.lock`; otherwise disable task auto-install and run
the explicit locked install first. Never describe a validation task as free of
all filesystem effects when its prerequisite intentionally synchronizes a tool
or package environment. Its non-mutating contract applies to maintained source,
configuration, and lockfiles.

Archive checksums do not make extraction safe by themselves. Apply
`security-check` artifact inspection before directly extracting or distributing
a downloaded archive.

## Migration

Inventory the current tool-version files and every consumer before adopting
mise. Add exact mise tool entries and verify them first. Retain a secondary
version file only for a current consumer, align it with mise, and document which
system still needs it. Remove old installers, shims, or update jobs only after
their complete responsibility has moved and local plus CI execution pass.

Do not silently modify a user's global mise configuration, trust store, PATH,
or active installation. Repository work may document the required bootstrap or
use a task-scoped reviewed executable; persistent user-environment changes need
explicit authorization.
