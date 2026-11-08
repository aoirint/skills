---
name: dependency-update-workflow
description: >-
  Discover repository dependencies and evaluate, propose, or apply scoped updates
  to libraries, tools, runtimes, GitHub Actions, and containers. Use for dependency
  inventories and cooldown-aware update work; pair with security-check and the
  applicable ecosystem Skills for adoption gates and implementation.
---

# Dependency Update Workflow

## When to Use

Use for a dependency inventory, update proposal, or authorized update across
one or more repository surfaces, including embedded installers and templates.
For a focused ecosystem operation, use its owning Skill directly; this Skill
adds repository-wide discovery and candidate comparison when needed.
It does not authorize installing tools globally, changing update automation,
deploying a release, or merging a pull request.
Use `development-environment-update-workflow` for developer-machine updates;
this Skill supplies repository compatibility requirements and owns repository
dependency changes, not host installation or manager migration.

## Goals

- Find update targets beyond top-level manifests without rewriting historical
  examples or generated output by hand.
- Distinguish the newest published version from the newest suitable candidate
  that meets compatibility, cooldown, and security requirements.
- Keep evidence, approval, implementation, and verification separate.

## Workflow

### Establish scope and ownership

1. Read repository guidance, the requested base revision, dependency policy,
   existing update proposals, and local changes. Distinguish inventory-only,
   proposal-only, and apply requests. Preserve unrelated work and use the
   repository's isolated-worktree procedure for implementation.

   For a broad "update dependencies" request, inventory all applicable surfaces,
   not just application libraries. Propose a coherent scope from actual use,
   compatibility, and risk: routine compatible updates to the active project
   can belong together; independent products, major migrations, provider swaps,
   changed support policy, or user-environment changes need a separate decision.
   Respect explicit exclusions. State included and deferred surfaces and ask
   only about ambiguities that materially change the work. Discovery alone
   does not authorize modifying everything it finds.
2. Read `security-check` for adoption, cooldown, provenance, integrity,
   execution, disclosure, and exception requirements. This Skill collects and
   compares evidence; it does not redefine those gates or grant exceptions.
   Read the applicable implementation Skills before choosing commands:

   | Surface | Owning Skill and responsibility |
   | --- | --- |
   | Language packages and runtimes | `node-quality-check`, `python-quality-check`, or the relevant ecosystem Skill: compatibility, resolver policy, lockfiles, and tests |
   | mise tools and tasks | `mise-workflow`: bootstrap, tool pins, platform locks, and task behavior |
   | Agent dependencies | `apm-workflow`: CLI eligibility, proposal/approval ordering, source and deployment ledgers, and notices |
   | Actions and reusable workflows | `github-actions-quality-check`: immutable action refs, workflow structure, permissions, and CI validation |
   | Images and bundled software | `docker-quality-check`: image/build/runtime validation; `security-check`: final-artifact and licensing review |
   | PR publication | `github-workflow`: disclosure, attribution, and publication checks |

3. Resolve companion Skills from the available catalog or repository guidance,
   not a presumed sibling installation. A missing required procedure blocks
   the dependent execution or adoption, not safe read-only inventory. Report
   the missing contract. Apply stronger applicable requirements; if procedures
   conflict or the required approval is unclear, stop that operation for
   maintainer resolution rather than choosing the more permissive path.
   If an owning procedure requires a broader policy or CI migration, identify
   it as an update prerequisite and obtain the necessary scope decision.
   Do not silently expand a routine update or omit a required control.

### Discover and compare

1. Read [repository discovery](references/repository-discovery.md) and build
   an inventory linking each dependency identity to its canonical declaration,
   exact resolved artifact, consumers, and generated copies. Record coverage
   gaps; an update bot or one manifest is not a complete repository inventory.
2. Read [candidate evaluation](references/candidate-evaluation.md) to find
   candidates from canonical publishers and registries, check release and
   artifact age, and collect trust evidence. Give `security-check` the current
   and candidate identities and resolved graph for advisory-source selection,
   applicability review, and adoption findings. Do this before fetching or
   executing candidate code.
   Metadata-only discovery must not silently self-update a tool or resolve
   executable hooks; verify the command's actual scope and behavior.
3. Compare compatible candidates within the requested scope. Preserve the
   project's supported release channels, runtime/platform matrix, version-range
   policy, and linked package families. Treat a major update or provider change
   as a migration. Explain when the newest release is deferred for age,
   compatibility, support, provenance, or an advisory rather than calling an
   older selection unconditionally "latest."
4. For an affected current dependency, distinguish a normally eligible fix
   from a fix that still needs an exception. Use `security-check` and the
   ecosystem's narrower rules to evaluate urgency, exposure, alternatives,
   and the exact unmet gate. Present the exact candidate, evidence, residual
   risk, approver, and removal/recheck condition for a proposed exception.
   An advisory does not grant approval; a waiting period does not prohibit
   discussing an explicitly approvable emergency exception. Retain every
   non-waived gate and never lower a repository-wide threshold to admit one fix.
5. Produce a reviewable decision for each target: update candidate, deferred
   candidate with eligibility date or prerequisite, no suitable update found,
   or blocked by missing evidence. Include old and proposed immutable identities,
   relevant source links, compatibility impact, advisory findings, affected
   files, verification plan, and any exact approved or pending exception.
   Keep the proposal read-only when requested or required by the owning Skill.

### Apply and verify

1. Apply only the authorized candidate and scope after its gates pass.
   Recheck mutable release/advisory metadata before adoption; do not substitute
   a newer candidate discovered during implementation. A changed artifact,
   publisher, target, or unmet gate requires a new decision.
2. Update canonical inputs and regenerate locks and managed output with the
   owning tools. Keep matching versions, SHAs, digests, checksums, platform
   artifacts, executable examples, and required notices consistent. Review
   the entire resolved diff, including transitive dependencies and newly
   introduced fetch/build/lifecycle behavior, before executing the result.
   Stop on unrelated resolver churn or an unexpected dependency/provider change.
3. Run the ecosystem's frozen/locked reproduction and relevant tests, builds,
   workflow checks, or container smoke checks. Inspect final resolved versions
   and immutable identities, ensure reproduction did not rewrite locks, and
   recheck advisories against the resulting graph. A successful install or
   version print alone does not establish compatibility or vulnerability status.
4. On failed resolution, integrity mismatch, unavailable evidence, or partial
   mutation, stop the affected operation. Record the exact step, observed
   changes, and whether anything executed; inspect state before retrying.
   Restore only task-owned changes whose prior state is known, preserving user
   work. Do not bypass controls, broaden an exception, hand-edit a managed
   lockfile, or retry through another delivery mechanism to make the check pass.
5. Before handoff, reconcile the inventory with the final diff and read-back.
   Report applied versions, deferred/blocked targets, source coverage, actual
   checks and results, skipped checks with reasons, and remaining risk or
   exception follow-up. Use `github-workflow` for an authorized draft PR;
   creation, successful CI, and merge authorization are separate states.
