---
name: bepinex-mono-mod-quality-check
description: Review or create a BepInEx Mono mod for C# project and module structure, plugin identity, game compatibility, dependency boundaries, GitHub CI and release automation, packaging, release metadata, and verification. Use when implementing, reviewing, preparing a release for, or diagnosing quality gaps in a BepInEx 5 Mono plugin or its build and release workflow.
---

# BepInEx Mono Mod Quality Check

## Goals

- Preserve a loader-visible plugin identity that agrees with the assembly, generated metadata, and package metadata.
- Keep C# project and module boundaries aligned with gameplay policy, framework integration, and composition responsibilities.
- Keep game and BepInEx compatibility explicit, evidence-backed, and scoped to what was actually tested.
- Produce reproducible builds and installable release packages without committing local game or build output.
- Keep GitHub Actions and release automation pinned, least-privilege, and traceable to the built artifact.
- Report findings as actionable evidence, not assumed conventions from another mod.

## Workflow

1. Establish the repository contract before proposing changes.
   - Read `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, the project file, lockfile, package assets, and relevant CI or release scripts.
   - Identify the intended BepInEx major version, game/runtime baseline, package host, and release path from repository evidence. Do not infer them from this skill or a different mod.
   - Classify the request: implementation review, project setup, package/release review, or a plan when the repository is unavailable.
   - For a new repository or a template-alignment review, read [repository-quality-template.md](references/repository-quality-template.md) and apply only the entries that match the chosen game, package host, and automation scope.
2. Check C# project and module structure.
   - Start from the repository's existing layout. Do not introduce projects, layers, or folder taxonomy solely to resemble another mod.
   - Keep the loader entry point and composition root small. It may create the controller, adapters, state, and use cases, but it must not become the location for gameplay policy or framework callbacks.
   - Put gameplay policy, state transitions, result values, and use cases in framework-free Core modules when the mod has enough behavior to benefit from a boundary. Core may depend on ports it defines, but not on BepInEx, Harmony, Unity, or game-specific types.
   - Put BepInEx configuration/logging, Harmony callbacks, Unity/game-object access, networking, and concrete port adapters in Interop modules. Keep callbacks thin: validate or guard the framework boundary, translate data, and delegate to Core-facing controller methods.
   - Introduce a Core port and an Interop implementation when a use case needs game or framework access. Do not hide that access behind static singletons in Core.
   - Keep a module cohesive around one responsibility. Split a module when it mixes policy with framework access or when its lifecycle/state ownership cannot be stated clearly; do not split it merely by file type or pre-emptive reuse.
   - Keep one plugin project when it enforces the needed boundary. Add separate C# projects only when a concrete test, reuse, build, or dependency-isolation need outweighs the added target-framework and packaging complexity.
3. Check the plugin boundary.
   - Ensure the assembly name, plugin GUID, plugin name, and loader-facing version have one documented source of truth or a verified synchronization path.
   - Confirm the plugin entry point uses BepInEx metadata and that generated plugin-info values, if used, agree with the project configuration.
   - Keep Harmony or equivalent patch registration deliberate: use a stable identifier, a bounded assembly/patch scope, and lifecycle behavior that does not duplicate registration.
   - Treat game API calls, patches, serialized names, and timing assumptions as compatibility-sensitive. Preserve the exact tested game baseline and request runtime evidence when a code-only review cannot establish it.
4. Check build and dependency boundaries.
   - Match the target framework and language version to the repository's documented BepInEx and game runtime compatibility; do not upgrade either opportunistically.
   - Keep game and loader references compile-only when the release package relies on the player's installed runtime. Keep development analyzers and code generators private to the project.
   - Use the committed lockfile and `dotnet restore --locked-mode` where the project provides one. Review dependency, lockfile, CI action, container, or downloaded-tool changes with `$security-check`.
   - Do not commit game installations, mod-manager profiles, generated plugin metadata, `bin/`, `obj/`, or machine-local paths.
5. Check package and release consistency.
   - Trace the release artifact from the built DLL to its archive. Confirm that the archive layout and every required file match the package host and repository documentation.
   - Reconcile package manifest identity, version, dependencies, compatibility claims, README, changelog, icon, and license with the release intent.
   - Keep developer changelog entries and user-facing release notes in their repository-defined roles. Do not claim untested game compatibility or publish a version already represented by an immutable release.
   - When the project derives manifest or package versions in CI, verify that the project version, generated version, and loader-compatible version are deliberately handled for stable, prerelease, and edge builds.
6. Check GitHub repository settings, CI, and release automation when the repository uses GitHub Actions or GitHub Releases.
   - Require the repository or organization Actions setting that enforces full-length commit-SHA pins. Independently verify every third-party `uses:` reference has a full commit SHA and an accurate version comment; inspect reusable workflows, container digests, and downloaded-tool checksums too.
   - When the repository publishes GitHub Releases, require repository-level immutable releases where GitHub makes the setting available. Automation must attach every asset before publishing the release and must fail rather than replace an existing tag, release, or asset. If the setting is unavailable, record the residual risk and require an explicit fail-on-existing-release/tag/asset path instead of silently treating releases as immutable.
   - Trace one release from its source commit through locked restore, build, archived artifact, and release asset. Publish only the artifact produced by that build; do not rebuild a separately checked-out revision in the release job. Create and verify an artifact digest across the build and release jobs.
   - Separate validation artifacts, prereleases, and stable publishing according to the repository's version rules. Gate external package-host publication on the intended stable release mode and require exactly one reviewed package artifact.
   - Default workflow permissions to read-only. Scope `contents: write` and publishing secrets to the release job that needs them, and never expose a publish credential to pull-request validation.
7. Run the narrowest relevant checks, then widen for the changed surface.
   - For C# or project changes, run the documented locked restore, formatter/analyzer check, and build. Use `--no-restore` after a successful locked restore when the repository does so.
   - For documentation or package text, run the repository Markdown check.
   - For workflows, composite actions, or shell scripts, use `$github-actions-quality-check` and run the repository's action, shell, and pin checks.
   - For release or compatibility changes, perform the repository's documented package inspection and runtime validation. State exactly what environment, game version, loader version, and mod set were tested; record missing runtime evidence as a blocker rather than guessing.
8. Report the result in this order: scope and evidence consulted; findings grouped by structure/plugin/build/CI/package/runtime; checks passed or skipped; and remaining compatibility or release risks. Pair code-level findings with `$code-quality-check`, GitHub workflow findings with `$github-actions-quality-check`, gameplay-mechanics claims with `$lethal-company-analyze` when applicable, and user-facing release text with `$release-note-workflow`.

## Reference Baseline

Read [repository-derived-baseline.md](references/repository-derived-baseline.md) when starting a new BepInEx Mono project or when the repository does not already document its structure and quality gates. It records the transferable practices observed in AutoTerminalScanClassic, CruiserJumpPractice, and SkipDropshipCompany; it is a baseline, not a replacement for the target repository's contract.

Read [repository-quality-template.md](references/repository-quality-template.md) when creating or aligning a repository. It turns that baseline into a checklist for ignore rules, APM, NuGet, Markdown, CI, composite actions, and conditional Thunderstore publishing.
