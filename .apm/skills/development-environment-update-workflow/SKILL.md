---
name: development-environment-update-workflow
description: >-
  Inventory, compare, and apply scoped developer-machine toolchain updates on
  Windows, Ubuntu on WSL2, and native Ubuntu. Use for installed SDKs, CLIs,
  runtimes, tool managers, development OS packages, or manager migrations;
  use dependency-update-workflow for repository dependency updates.
---

# Development Environment Update Workflow

## When to Use

Use for developer-computer environment inventories, update proposals, authorized
updates, and comparisons between the existing tool-management setup and
alternatives.

Maintain procedures for Windows 11 25H2 or later, plus Ubuntu 24.04 or later
in WSL2 guests and native installations. These minima keep the maintained procedures focused;
for a requested older OS, verify applicability separately rather than treating
it as forbidden or adding unneeded legacy branches. Observe the actual release
and support status instead of assuming the newest version. Identify the actual
machines and Ubuntu distributions; these are separate environments, not three
names for one shared installation. Production server operations and macOS
procedures are outside this Skill's scope.

Repository manifests, lockfiles, runtime requirements, and CI belong to
`dependency-update-workflow` and the owning ecosystem Skills. Inspect them as
compatibility inputs here; changing them requires an authorized repository scope.

## Goals

- Establish which installation actually supplies each development command.
- Compare retention, updates, and migrations against real project requirements.
- Keep changes scoped, recoverable, and verified across affected environments.

## Workflow

### Establish scope and discover ownership

1. Distinguish inventory, proposal, and apply requests. Identify the named
   computers, users, shells, projects, and supported environments, including
   environments that cannot be inspected. Read local guidance and preserve
   uncommitted files, shell configuration, and user customizations.
   A broad update request does not authorize blanket system upgrades, manager
   migration, PATH or environment changes, security settings, restarts,
   uninstalls, or persistent startup changes. Resolve material scope gaps
   before those operations; continue safe inventory independently.
2. Read `security-check` for the common provenance, cooldown, advisory,
   execution, disclosure, and exception policy, including its
   `references/advisory-review.md`. Read `mise-workflow` for mise installation,
   pins, locks, and tasks when present; use `wsl-workflow` for host/guest
   configuration, interoperation, and restart procedures. Resolve companions
   from the available catalog or repository guidance, not assumed sibling
   paths. Missing required guidance blocks dependent execution, not read-only
   discovery. Do not replace a missing control with a weaker local rule.
3. Read [platform discovery and verification](references/platform-discovery.md)
   for the relevant targets. Build an inventory connecting each tool to:
    - Machine, Windows host or Ubuntu distribution, OS release, architecture,
      user, and shell or IDE execution context.
    - OS-, user-, and project-level installation owners, manager versions,
      install locations, configured sources, and global versus project scope.
    - Effective command resolution, aliases/functions, shims or links,
      reported version, and any competing installations or project selectors.
    - Representative consuming projects, supported runtime versions, global
      CLI packages, native extensions, and automation that depends on it.

   Inspect installed metadata and narrow configuration before invoking unknown
   binaries. A version probe can execute code; verify the execution path under
   `security-check` first. Avoid discovery commands that bootstrap tools,
   self-update, download plugins, or run project hooks implicitly.
4. Reconcile manager inventory with effective commands in the actual working
   directory and shell. An installed version is not necessarily the active
   version. Record unresolved ownership, inaccessible machines, and unknown
   consumers as gaps, not as proof that an installation is absent or unused.
   Keep private paths and system details out of public reports.

### Compare and plan

1. Compare keeping the current setup, updating within it, and migrating only
   where a concrete benefit warrants the work. Explain security/support status,
   project compatibility, platform coverage, operational simplicity, migration
   effort, disk/network or licensing costs, disruption, and recovery limits.
   Do not equate fewer managers or newer versions with a better environment.
   For example, nvm or nvm-windows versus pnpm-managed Node, and pyenv versus
   uv-managed Python, are possible comparisons, not assumed installations or
   required migrations. Verify the relevant versions and platform capabilities
   before recommending a replacement.
2. Collect candidate evidence from the actual publisher and distributor.
   Supply `security-check` with exact current/candidate identities, artifact
   age, source, architecture, resolved dependencies, and advisory evidence.
   OS-package revisions and backports must be assessed against their actual
   distribution. An urgent fix needs the owning policy's explicit exception
   decision when a gate is unmet; urgency does not authorize execution.
3. Produce an exact operation plan per environment: installation owner and
   scope, old/new versions and artifact identities, commands, affected files
   and selectors, dependency changes, permissions, restart needs, verification,
   and rollback. Check the command's actual behavior against installed-version
   help and current primary documentation. Include installer side effects and
   automatic dependency/service changes, not only the requested package.
   A preview is evidence for review, not an immutable execution guarantee.
   If pre-execution selection and required gates cannot be demonstrated, block
   installation rather than issue a broad package-manager upgrade.
4. Separate routine compatible updates from manager replacement, support-policy
   changes, OS release upgrades, and changes to shared project configuration.
   Obtain the required decision for each scope expansion. Record approved and
   pending operations distinctly. For migrations, plan coexistence or a staged
   switch where supported, preserve old selectors until consumers pass, and
   identify which changes cannot be reliably reversed before execution.

### Apply and verify

1. Execute only the authorized operations after their gates pass. Capture the
   relevant prior versions, configuration, and restoration information without
   overwriting existing backups or exposing secrets. Preserve file metadata
   where required by the owning procedure. Recheck candidate identity and the
   actual package transaction before mutation; stop on changed artifacts,
   unexpected removals, privilege requirements, or dependency expansion.
2. Apply a small coherent group, then verify before continuing. Confirm the
   effective executable path, owner, version, and project-selected runtime in
   the affected shell and project directories. Compare existing sessions with
   a fresh shell when initialization changed. Check relevant IDE/task contexts
   rather than claiming all launchers inherit the terminal's state.
3. Run representative affected projects' established frozen/locked checks,
   builds, and CLI smoke tests using reviewed dependencies. Verify native
   extensions or SDK integration where affected. Preserve project changes and
   confirm checks did not rewrite manifests or locks. Test each affected
   supported environment, or explicitly report unavailable coverage.
   Route required reboot or WSL restart through the owning procedure and
   authorization; mark verification pending if it cannot be performed.
4. On failure or partial mutation, stop the affected operation and inspect what
   actually changed before retrying or restoring. Restore only task-owned
   changes with known prior state, preserving later user edits. Do not claim
   rollback from a backup's existence alone; verify the restored resolution
   and representative workload. Report a recovery blocker if restoration is
   unavailable, destructive, or outside authorization.
5. Report observed baseline, decision, exact applied changes, effective versions,
   check results, deferred targets, coverage gaps, and remaining exception or
   restart follow-up. Distinguish a proposal, successful installer exit,
   verified command resolution, and demonstrated project compatibility.

### Retire tools only with evidence and scope

1. Before proposing retirement, check actual use across supported machines and
   projects, including global CLI consumers, shell/IDE launchers, scripts,
   documentation, CI, and migration or older-version compatibility needs.
   Local non-use is not evidence of global retirement; inaccessible consumers
   remain unknown. Do not run broad cleanup or autoremove to discover usage.
2. Suggest retention, scoped removal, or a separate retirement decision with
   affected consumers, replacement coverage, recovery needs, and evidence gaps.
   Remove only explicitly authorized installations after replacement checks.
   Removing one local tool does not authorize deleting Skills, shared
   configuration, documentation, or necessary history. For an authorized Skill
   consolidation, use `skill-quality-check` and its migration inventory rather
   than treating it as machine cleanup.
