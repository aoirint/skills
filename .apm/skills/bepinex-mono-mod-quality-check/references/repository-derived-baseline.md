# Repository-Derived Baseline

This baseline captures transferable BepInEx Mono repository practices. Apply it
only after reading the target repository's own instructions; game and package
host details remain repository-specific, not universal requirements.

## Transferable project shape

- Use an SDK-style project with an explicit target framework and language
  version compatible with the intended loader and game runtime.
- Keep the DLL identity, BepInEx plugin metadata, and package identity
  traceable. Prefer generated plugin metadata or another single synchronization
  path over independently edited duplicate strings.
- Keep loader and game API references out of the packaged dependency payload
  when the player environment supplies them. Keep analyzers and source
  generators private to the build.
- Commit the NuGet lockfile and restore in locked mode so CI and local builds
  resolve the same graph.

## Transferable module shape

Use a composition root plus `Core` and `Interop` modules when that separation
clarifies responsibilities. Preserve the boundary rather than the exact folder
names.

- The loader entry point and composition root assemble the plugin. They wire
  state, use cases, handlers, adapters, configuration, and logging, without
  becoming a second place for gameplay policy.
- Core owns the mod's policy: domain state, use cases, handlers, result values,
  and port interfaces. Keep it free of BepInEx, Harmony, Unity, and game types
  so lifecycle and game API concerns remain visible at its boundary.
- Interop owns framework and game integration: plugin configuration and
  logging, Harmony patches, game-object and network access, and concrete
  adapters. Let callbacks guard the external boundary and delegate; keep
  gameplay decisions in Core.
- Add a Core port plus an Interop adapter when Core needs external data or an
  effect. Make state ownership explicit rather than sharing mutable singleton
  access across callbacks and use cases.

Use this shape only when it clarifies a real separation. A small plugin can
remain one project and use a few cohesive modules. Create another C# project
only for a concrete test, reuse, build, or dependency-isolation requirement;
multiple target frameworks and release assembly layout are costs to validate,
not automatic quality improvements.

## Transferable release shape

- Treat the built DLL and package assets as one release unit. Inspect the final
  archive, not only the build directory.
- Include only the files required by the selected package host, commonly a
  manifest, user README, changelog, icon, and license alongside the plugin DLL.
- Keep package dependency strings, description, version, and compatibility
  claims synchronized with the tested release baseline.
- Keep development history and end-user release notes separate when the
  repository distinguishes them.

## GitHub CI and release automation

For repositories that use GitHub Actions to build an archive and publish
releases, apply the following review baseline:

- Enable the repository or organization policy requiring GitHub Actions to use
  full-length commit-SHA pins. Keep the exact SHA in each `uses:` reference and
  retain a version comment that a reviewer can verify. Pin containers by digest
  and verify checksums for downloaded executables.
- Keep ordinary CI read-only. Give the release job only the write permission it
  needs, and pass package-host tokens only to that publishing step.
- Build once from the release commit, upload the completed archive and its
  digest, then download and verify that exact artifact before publishing it.
  Do not publish a separately rebuilt archive or accept zero or multiple
  package artifacts.
- Enable GitHub immutable releases when available. Create the release as a
  draft, attach all assets, then publish it so its tag and assets cannot be
  changed afterward. If that setting is unavailable, record the residual risk;
  still keep automation fail-closed if the intended release, tag, or asset
  already exists.
- Distinguish edge validation artifacts, prereleases, and stable releases.
  Publish to external package hosts only for the repository's intended stable
  mode, after package inspection and runtime evidence are available.

GitHub documents the repository Actions setting for
[full-length commit-SHA pins](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
and [immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).

## Transferable verification shape

Start with the repository's documented commands. Common categories include:

```powershell
dotnet restore --locked-mode
dotnet format --no-restore --verify-no-changes
DOTNET_CLI_UI_LANGUAGE=en dotnet build
```

They also lint Markdown, and run shell, GitHub Actions, and action-pin checks
when those surfaces change. These are examples, not commands to invent in a
repository that has not adopted the corresponding tools.

For runtime validation, record the exact game build, BepInEx version, mod set,
and reproduction path. Build success alone does not establish patch timing,
API compatibility, multiplayer behavior, or package installability.
