---
name: bepinex-mono-mod-quality-check
description: Review or create a BepInEx Mono mod for plugin identity, game compatibility, dependency boundaries, packaging, release metadata, and verification. Use when implementing, reviewing, preparing a release for, or diagnosing quality gaps in a BepInEx 5 Mono plugin or its build and release workflow.
---

# BepInEx Mono Mod Quality Check

## Goals

- Preserve a loader-visible plugin identity that agrees with the assembly, generated metadata, and package metadata.
- Keep game and BepInEx compatibility explicit, evidence-backed, and scoped to what was actually tested.
- Produce reproducible builds and installable release packages without committing local game or build output.
- Report findings as actionable evidence, not assumed conventions from another mod.

## Workflow

1. Establish the repository contract before proposing changes.
   - Read `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, the project file, lockfile, package assets, and relevant CI or release scripts.
   - Identify the intended BepInEx major version, game/runtime baseline, package host, and release path from repository evidence. Do not infer them from this skill or a different mod.
   - Classify the request: implementation review, project setup, package/release review, or a plan when the repository is unavailable.
2. Check the plugin boundary.
   - Ensure the assembly name, plugin GUID, plugin name, and loader-facing version have one documented source of truth or a verified synchronization path.
   - Confirm the plugin entry point uses BepInEx metadata and that generated plugin-info values, if used, agree with the project configuration.
   - Keep Harmony or equivalent patch registration deliberate: use a stable identifier, a bounded assembly/patch scope, and lifecycle behavior that does not duplicate registration.
   - Treat game API calls, patches, serialized names, and timing assumptions as compatibility-sensitive. Preserve the exact tested game baseline and request runtime evidence when a code-only review cannot establish it.
3. Check build and dependency boundaries.
   - Match the target framework and language version to the repository's documented BepInEx and game runtime compatibility; do not upgrade either opportunistically.
   - Keep game and loader references compile-only when the release package relies on the player's installed runtime. Keep development analyzers and code generators private to the project.
   - Use the committed lockfile and `dotnet restore --locked-mode` where the project provides one. Review dependency, lockfile, CI action, container, or downloaded-tool changes with `$security-check`.
   - Do not commit game installations, mod-manager profiles, generated plugin metadata, `bin/`, `obj/`, or machine-local paths.
4. Check package and release consistency.
   - Trace the release artifact from the built DLL to its archive. Confirm that the archive layout and every required file match the package host and repository documentation.
   - Reconcile package manifest identity, version, dependencies, compatibility claims, README, changelog, icon, and license with the release intent.
   - Keep developer changelog entries and user-facing release notes in their repository-defined roles. Do not claim untested game compatibility or publish a version already represented by an immutable release.
   - When the project derives manifest or package versions in CI, verify that the project version, generated version, and loader-compatible version are deliberately handled for stable, prerelease, and edge builds.
5. Run the narrowest relevant checks, then widen for the changed surface.
   - For C# or project changes, run the documented locked restore, formatter/analyzer check, and build. Use `--no-restore` after a successful locked restore when the repository does so.
   - For documentation or package text, run the repository Markdown check.
   - For workflows, composite actions, or shell scripts, use `$github-actions-quality-check` and run the repository's action, shell, and pin checks.
   - For release or compatibility changes, perform the repository's documented package inspection and runtime validation. State exactly what environment, game version, loader version, and mod set were tested; record missing runtime evidence as a blocker rather than guessing.
6. Report the result in this order: scope and evidence consulted; findings grouped by plugin/build/package/runtime; checks passed or skipped; and remaining compatibility or release risks. Pair code-level findings with `$code-quality-check`, gameplay-mechanics claims with `$lethal-company-analyze` when applicable, and user-facing release text with `$release-note-workflow`.

## Reference Baseline

Read [repository-derived-baseline.md](references/repository-derived-baseline.md) when starting a new BepInEx Mono project or when the repository does not already document its quality gates. It records the transferable practices observed in AutoTerminalScanClassic, CruiserJumpPractice, and SkipDropshipCompany; it is a baseline, not a replacement for the target repository's contract.
