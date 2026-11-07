# Repository Dependency Discovery

## Start from the repository contract

Inspect tracked paths, including hidden directories, before searching only for
well-known manifest names. Read repository instructions, workspace definitions,
build/test entrypoints, update-bot configuration, and packaging/release scripts.
Use the requested scope to bound the search; record excluded subprojects or
unavailable submodules instead of claiming complete coverage.

Trace references from each entrypoint to local actions, reusable workflows,
scripts, generated files, and install/download helpers. Search results are
leads: a version-shaped string is not necessarily an update target.
Do not execute a discovered script to learn what it installs until its
execution path passes `security-check`.

## Inspect applicable surfaces

| Surface | Look for |
| --- | --- |
| Package graphs | Root and nested manifests, workspaces, lockfiles, constraints, overrides, catalogs, build requirements, dev/test/optional dependencies, and inline script metadata |
| Toolchains | Runtime version files, SDK files, `packageManager`/engine fields, mise configuration and locks, tool manifests, compiler/tool versions, and CI setup inputs |
| GitHub Actions | Entry workflows, recursively reachable local actions and reusable workflows, external `uses:`, runner/container selections, and tools downloaded by `run:` steps |
| Containers | Every Dockerfile stage and syntax frontend, Compose/devcontainer images, image tags/digests, apt/apk/rpm packages and repositories, build arguments, and copied runtime bundles |
| Embedded dependencies | Shell/PowerShell/Python installers, release URLs, version defaults, checksums, vendored libraries, submodules, generated clients, plugins, and bootstrap scripts |
| Distributed examples | Templates, scaffold assets, executable documentation examples, generated deployments, and copied CI/install snippets that consumers will execute |
| Existing evidence | SBOMs, dependency graphs, audit output, bot proposals, release manifests, license/notice records, and prior scoped exceptions |

Include a dependency's development, CI, and build uses rather than considering
only production imports. For a container or compiled bundle, distinguish the
declared source version from the final shipped components and platform variants.
Use available lock/graph evidence for transitives; mark unresolved graph portions
as unknown until the owning resolver can inspect them safely.

Distinguish fixed source declarations from values resolved at build time.
An unversioned `apt-get install` or floating image tag may have no source version
to bump: assess a controlled rebuild or base-image refresh and explain what is
reproducible. Use reviewed metadata-only resolution to identify candidate package
versions and repository/snapshot inputs before installation. If the build cannot
enforce the reviewed selection and adoption gates, stop for an explicit resolution
plan rather than fetching packages to discover their identities afterward.
After an authorized build, verify the actual installed versions.
Do not invent version pins, add an indiscriminate OS upgrade, or
claim a rebuild adopted a fix without final-image evidence. A Dockerfile syntax
frontend, the build daemon, the base image, and a downloaded application binary
are separate dependencies with separate update and compatibility contracts.

Do not install another dependency scanner merely for discovery. Prefer reviewed
repository tools and read-only metadata. Before trusting an existing graph or
SBOM, check its generating revision, platform, enabled features, and coverage.
For GitHub-derived inventory, consult its
[supported ecosystem and file coverage](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems)
when deciding what it can miss, especially embedded templates and scripts.

## Establish ownership before editing

For each occurrence, classify its role:

- **Canonical input:** the manifest, version file, template, or source that owns
  the choice. Multiple consumers may intentionally use different versions.
- **Resolved or generated output:** a lockfile, deployed Skill, generated
  workflow, or bundle. Identify its generator and refresh from its source.
- **Consumer contract:** a runtime constraint, CI setup, tested platform,
  checksum, notice, or executable example that must stay consistent.
- **Historical or test material:** changelogs, migration examples, fixtures, and
  regression inputs. Preserve intentional old versions unless the task changes
  the behavior they document or test.

Follow references in both directions. A script default may drive several
templates; a generated copy can reveal a canonical source omitted by a bot.
Deduplicate by package/registry or publisher/artifact identity and consumer
constraints, not by basename or displayed version alone. Do not global-replace
version strings or infer one shared version merely because two files match.

## Inventory output

Keep enough information to revisit each decision without repeating discovery:

- Identity: ecosystem, registry, package/source repository, and publisher.
- Location and role: canonical declaration, resolved pin, generated consumers,
  runtime/build/CI/development use, and platform or workspace scope.
- Current state: declared constraint versus exact resolved version, commit,
  digest, or artifact hash; unresolved or floating references remain explicit.
- Update contract: owning Skill/tool, generation command, compatibility/support
  constraints, existing policy and scoped exceptions, and intended checks.
- Coverage: inspected paths/graphs and missing or deliberately excluded areas.

Use this inventory to plan coherent updates. Separate unrelated libraries,
toolchain migrations, runtime support changes, and automation-policy changes;
keep coupled packages and their generated consumers together.
