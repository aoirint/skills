# BepInEx Mono Implementation Runbook

Run this procedure in order. It is the reproducible implementation contract for
the quality baseline in this Skill. A target repository supplies values for the
evidence ledger; it does not choose which baseline controls are optional.

## Contents

- [1. Classify and inventory](#1-classify-and-inventory)
- [2. Evidence ledger](#2-evidence-ledger)
- [3. Required file inventory](#3-required-file-inventory)
- [4. Apply changes in dependency order](#4-apply-changes-in-dependency-order)
- [5. Conditional branches](#5-conditional-branches)
- [6. Verification matrix](#6-verification-matrix)
- [7. Completion report](#7-completion-report)

## 1. Classify and inventory

1. Set exactly one primary request type: `setup`, `alignment`,
   `implementation`, `release-readiness`, or `plan-only`.
2. List repository files before editing. Inspect `AGENTS.md`, `README.md`,
   `CONTRIBUTING.md`, all `*.sln` and `*.csproj`, `nuget.config`, every
   `packages.lock.json`, `.gitignore`, `.markdownlint-cli2.yaml`, package
   assets, `.github/workflows/`, `.github/actions/`, and release scripts.
3. For `alignment`, compare every item in the required inventory below with the
   repository. A missing baseline item is a finding. Do not mark it optional
   because a predecessor repository did not use it.
4. For `plan-only`, produce the same inventory and evidence ledger, label every
   uninspected item `unverified`, and do not claim a check passed.

## 2. Evidence ledger

Create this table before writing any target-specific value. `confirmed` must
cite a local file, package-host documentation, repository setting, or runtime
record. `blocked` stops only the dependent branch, not unrelated baseline work.

| Fact | Allowed status | Required before |
| --- | --- | --- |
| Game build, runtime, and supported platform | confirmed / blocked | target framework, compatibility claim, runtime pass |
| Exact BepInEx major and version | confirmed / blocked | loader reference, target framework, runtime pass |
| Plugin GUID, name, assembly name, owner, and version source | confirmed / blocked | plugin metadata, manifest, release identity |
| Game API, patch target, timing, and supported mod set | confirmed / blocked | patch implementation, compatibility claim |
| Package host and its authoritative contract | confirmed / blocked / none | host-specific archive rules or publishing |
| Release mode and version classification | confirmed / blocked / none | tag, GitHub Release, external publishing |
| GitHub Actions, GitHub Releases, Thunderstore, and APM use | yes / no / blocked | respective conditional branch |
| Repository/org settings and publish-secret scope | confirmed / blocked | CI/release readiness pass |

Never infer a `confirmed` value from a different game, mod, package host, or
repository. If a value is blocked, write the literal placeholder only in a
design document; do not commit it into executable metadata, manifests, or
publishing configuration.

## 3. Required file inventory

Create or retain each baseline artifact below unless its listed exception is
recorded in the evidence ledger and completion report.

| Artifact | Required content / invariant | Only valid exception |
| --- | --- | --- |
| Solution and SDK-style plugin project | explicit `TargetFramework`, `LangVersion`, identity/version synchronization path | `plan-only` has no repository to edit |
| `nuget.config` | `<clear />`; explicit approved sources; `packageSourceMapping` covering direct, transitive, and framework packages | no NuGet resolution is possible or required, with evidence |
| `packages.lock.json` | one committed lockfile per resolving project | project resolves no packages, with project-file evidence |
| `.gitignore` | narrow local/generated rules; never hides source, assets, lockfiles, or docs | none |
| `README.md` | setup, checks, debugging, packaging, compatibility evidence, release path | none |
| `CONTRIBUTING.md` | change-to-check matrix and contributor requirements | none |
| `CHANGELOG.md` and `LICENSE` | intentional release-history and license roles | repository has an explicit replacement, named in the report |
| `.markdownlint-cli2.yaml` | lint committed Markdown, respect `.gitignore`, narrow documented exceptions | none |
| versioned archive contract | host-neutral root/path/DLL/prohibited-content rules | no package/archive is produced, with evidence |
| APM files and deployed output | `apm.yml`, lock, generated target as one unit | ledger says APM `no` |
| GitHub workflows/actions | validation workflow and release workflow only when enabled | ledger says GitHub Actions `no` |
| Host manifest/publish action | exact selected-host extension only | host is `none` or blocked |

## 4. Apply changes in dependency order

Complete each numbered stage before beginning the next. If an enabled stage is
blocked, leave it unimplemented, record the blocker, and continue with later
independent stages.

### 4.1 Repository hygiene and documentation

1. Define intentional roles for solution/project files, `assets/`, `docs/`,
   package assets, and generated output.
2. Add `.gitignore` local rules first: game installs, profiles, `bin/`, `obj/`,
   IDE caches, logs, local work/build directories, agent worktrees, and only
   actually generated metadata. Keep any pinned upstream ignore template as a
   separate, commit-linked block below local rules.
3. Run `git status --short`. Stop and correct the ignore rules if a source,
   asset, lockfile, or document that must be committed becomes hidden.
4. Write README and CONTRIBUTING content from the evidence ledger. README names
   setup, restore, format, build, test, debugging, packaging, compatibility
   evidence, and release steps. CONTRIBUTING maps each changed surface to its
   required verification.
5. Add Markdown lint configuration. It must target committed `**/*.md`, honor
   `.gitignore`, exclude only transient agent/worktree paths, and explain every
   disabled rule inline.

### 4.2 Project, module, and dependency boundary

1. Create or preserve one SDK-style plugin project. Set `TargetFramework` and
   `LangVersion` only from confirmed game/loader evidence.
2. Establish one checked synchronization path for assembly name, project
   version, BepInEx GUID/name/version, generated plugin information, manifest,
   archive name, tag, and release title. Verify every enabled output uses it.
3. Keep the plugin entry point/composition root limited to wiring, lifecycle,
   configuration/logging, and bounded patch registration. Do not put gameplay
   policy or framework callbacks together in it.
4. Keep a small plugin cohesive. Add Core only when gameplay policy/state/use
   cases need to be isolated from BepInEx/Harmony/Unity/game access. Core owns
   policy, state, results, and its ports and has none of those framework/game
   references. Interop owns callbacks, configuration, logging, game access,
   networking, and port adapters. A callback validates/translates then
   delegates; Core never reaches a game singleton directly.
5. Add a separate Core or test project only for documented test, reuse, build,
   or dependency-isolation value. For every new project, repeat the target
   framework review, source mapping, lockfile, restore, format, build, and test
   coverage steps. Verify it is not included in the player package unless the
   archive contract explicitly requires it.
6. Configure game and BepInEx references compile-only when the player install
   supplies them. Mark analyzers, generators, and build-only metadata helpers
   `PrivateAssets="all"`. Do not use local game paths as a restore workaround.
7. Add `nuget.config`, then generate and commit the lockfile for every
   resolving project. Before accepting a new source/package/lock delta, review
   canonical URL, publisher, immutable version or digest, available hash,
   license, transitive graph, and seven-day release age.

### 4.3 Archive contract and package content

1. Create a small versioned archive contract in repository-owned documentation
   or a deterministic validator. Its host-neutral base specifies allowed root
   paths, required repository-owned files, the exact count and path of plugin
   DLLs, prohibited runtime/game DLLs, `bin/`, `obj/`, logs, profiles, local
   paths, secrets, and archive traversal/absolute-path/unsafe-link entries.
2. Build into a clean staging directory. Copy only files allowed by the archive
   contract. Create exactly one archive, inspect its entries, and compute a
   SHA-256 digest.
3. If a package host is confirmed, add only its authoritative extension:
   manifest fields, root layout, dependency syntax, namespace/category, version
   restrictions, authentication, and overwrite behavior. Do not use a
   Thunderstore manifest or GitHub asset convention for another host.
4. Block package publication when host contract, package identity, runtime
   evidence, or final-archive validation is blocked or failing.

### 4.4 Automation

1. If APM is `yes`, preserve/create `apm.yml`, pin remote sources to full SHAs,
   check provenance/license/last-changed-subdirectory cooldown, record third
   party notices, then commit manifest, lockfile, and generated output together.
2. If GitHub Actions is `yes`, create/align a validation workflow in this order:
   checkout; external-tool setup and verification; ShellCheck; actionlint;
   pinact; SDK setup; locked restore; format; no-restore build; tests; Markdown
   lint; archive validation when relevant. Use read-only permissions, explicit
   Bash, and PR-only cancellation concurrency.
3. Pin third-party actions by full SHA plus accurate version comment, containers
   by digest, and downloaded executable tools by adjacent version and checksum.
   Cache only verified archives and use committed lockfiles as NuGet cache keys.
4. If GitHub Releases is `yes`, create a build job that creates one archive and
   digest from the release commit; publish only a downloaded-and-verified copy.
   The release job alone receives `contents: write`; it creates a draft, adds
   all assets and checksum, then publishes. It fails on an existing tag,
   release, or asset and never rebuilds or replaces an artifact. Require
   immutable releases where available; otherwise record residual risk.
5. If external publishing is enabled, gate it to the confirmed stable mode,
   exactly one reviewed prebuilt archive, passing digest/archive/runtime checks,
   and a credential scoped to the one publish step. Never expose it to PR jobs.

## 5. Conditional branches

| Condition | Required action | Explicitly do not do |
| --- | --- | --- |
| APM = no | omit APM files/checks and record this | create empty APM configuration |
| GitHub Actions = no | document local checks | invent workflow YAML or pin rules |
| GitHub Releases = no | retain archive/digest validation if packaging | require draft/immutable-release behavior |
| Package host = none | define archive contract if an archive exists | create a host manifest or upload workflow |
| Package host = Thunderstore | apply Thunderstore section in the template | publish edge/prerelease without a supported contract |
| Custom package host | add only verified host extension | borrow Thunderstore/GitHub metadata |
| No automated tests | record no-test status and test strategy | invent a test command |
| New/changed automated tests | run documented test command after build | treat build as test evidence |
| Runtime evidence blocked | complete static checks | claim compatibility or approve stable publishing |

## 6. Verification matrix

Run every row whose trigger is true. A command that cannot run is `skipped`,
not passed; record the command, reason, and resulting risk.

| Trigger | Required verification | Pass condition |
| --- | --- | --- |
| C# or project change | `dotnet restore --locked-mode`; `dotnet format --no-restore --verify-no-changes`; `dotnet build --no-restore` | all exit 0; lockfiles unchanged after restore |
| Automated tests exist or changed | documented test command after build | exit 0 and relevant tests execute |
| Markdown/package text | checked-in Markdown linter over committed Markdown | exit 0 |
| `.gitignore` change | `git status --short` plus intended/unintended file review | no required file hidden |
| NuGet source/package/lock change | source/publisher/version/hash/license/transitive/age review | ledger records approval; mapping/locks cover every resolver |
| Workflow/action/shell change | ShellCheck, `actionlint`, `pinact run --check --min-age 7`, manual pin/permission/concurrency/secret review | all pass; every executable input is pinned/verified |
| APM change | `apm lock`; lock review; `apm install --frozen`; `apm audit --ci` | expected refs/hashes and no drift |
| Package/release change | clean staging, archive-contract inspection, SHA-256, exact-artifact handoff check | one valid archive; digest matches |
| Compatibility/release claim | clean-profile runtime test | record exact game build, BepInEx version, mod set, install path, scenario, result |
| GitHub Release | repository-setting review and fail-on-existing release path | settings/gaps recorded; no mutable overwrite path |

## 7. Completion report

Use this exact order:

1. Request type and repository state.
2. Evidence ledger, including every `blocked` fact and dependent blocked branch.
3. Baseline inventory: `present`, `added`, `finding`, or `valid exception` for
   every artifact in section 3.
4. Files changed and synchronization paths verified.
5. Verification matrix results: `passed`, `failed`, or `skipped` with the exact
   command/reason/risk.
6. Runtime and package-host evidence.
7. Remaining risks and the precise condition that prevents approval or
   publication.

Do not call the repository ready when any required baseline artifact is a
finding, any enabled verification is skipped/failed, a release artifact is not
verified, or a compatibility/publishing claim lacks its required evidence.
