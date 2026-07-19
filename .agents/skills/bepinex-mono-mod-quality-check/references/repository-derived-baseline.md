# Repository-Derived Baseline

This baseline was derived from AutoTerminalScanClassic, CruiserJumpPractice, and
SkipDropshipCompany. Apply it only after reading the target repository's own
instructions; the three projects are Lethal Company / Thunderstore examples,
not universal BepInEx requirements.

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

The three source repositories use a composition root plus `Core` and `Interop`
modules. Preserve the responsibility boundary rather than the exact folder
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

## Transferable verification shape

Start with the repository's documented commands. The three source repositories
commonly use the following categories:

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
