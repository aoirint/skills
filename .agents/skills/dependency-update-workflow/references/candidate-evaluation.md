# Dependency Candidate Evaluation

## Find candidates without adopting them

Start from the dependency's recorded registry, publisher, and upstream project.
Use registry version/publication metadata, official releases and security
advisories, changelogs, support schedules, and compatibility documentation.
Read-only ecosystem outdated/list commands and existing bot proposals can help
find candidates, but verify their behavior and corroborate their results.
Search engines and mirrors are discovery aids, not proof of publisher identity.

Compare the newest stable release, the newest compatible release that satisfies
the applicable policy, and any relevant security fix. Keep each release's own
clock and identity; a newer release does not reset an older candidate's age.
Respect intentional release channels and maintenance branches. Do not replace
an unsupported dependency with an unrelated provider or cross a requested major
boundary without making that migration explicit.

Resolve mutable tags to immutable commits/digests. Match a GitHub Action's
version comment to the actual pinned commit. For containers and runtime bundles,
identify the distributor and every selected platform artifact: an old language
release does not establish the age of a newly built image or binary.

## Supply evidence to security-check

`security-check` owns the acceptance criteria and exception policy. Collect
the evidence it needs rather than inventing a parallel trust score:

- **Identity and provenance:** corroborate the registry/project/publisher
  relationship through canonical sources. Investigate a registry redirect,
  ownership transfer, unexpected fork, renamed package, or new download host.
- **Artifact integrity:** record immutable refs, digests, checksums, and
  available signature/provenance verification. A checksum from the same
  untrusted download location detects mismatch but does not establish trust.
- **Release age:** record the actual selected artifact's publication evidence,
  check time, applicable cooldown, and earliest eligible time with timezone.
  Do not substitute a local file timestamp, download/cache date, or an unrelated
  upstream tag. Use an owning Skill's more specific rule where applicable,
  such as the last relevant subdirectory change for an APM virtual package.
- **Behavior and changes:** inspect release notes and the relevant source or
  artifact diff for install/build scripts, nested downloads, bundled code,
  permissions, licensing, support changes, and new resolved dependencies.
- **Limits:** record missing publication data, unverifiable identity,
  incomplete graphs, unsupported platforms, and unresolved advisory matches.

Popularity, elapsed cooldown, an official-looking name, an immutable hash, or
absence of scanner findings is not independently sufficient adoption evidence.
Use the stricter applicable policy. Missing or contradictory evidence blocks
the affected adoption until resolved; do not convert an unknown into a pass.

Check the exact resolver and command form before relying on an age gate.
An update bot's configuration does not prove that a package manager's lockfile
refresh applies the same gate to every transitive dependency. When Renovate is
part of the workflow, its [security preset limitations](https://docs.renovatebot.com/presets-security/)
explain why some update types need separate package-manager or artifact checks.
Do not install, reconfigure, or schedule a bot merely to make an update proposal.

## Hand off advisory review

Use `security-check`'s advisory-review procedure to choose trustworthy sources
for the dependency type and assess applicability. Resolve that resource through
the installed Skill. Supply current and proposed identities, distribution and
platform, resolved transitive paths, and available final-artifact evidence.
Bring its findings and evidence gaps into the update comparison; do not replace
the security review with an update bot's green status or keyword search.

If the current version is affected and the fixed version is not normally
eligible, compare waiting, a different eligible fixed version, and temporary
mitigation before proposing an exception through the owning security procedure.
State what the evidence establishes about urgency and impact without inventing
reachability or exploitation. Follow that Skill's disclosure boundary in the
update record.

## Keep the decision reviewable

For each proposed update, link the old and new immutable artifacts to release
and compatibility evidence, advisory findings, and the eligible adoption time.
Explain relevant rejected or deferred candidates without copying a release catalog.
For an exception, retain the exact artifact, unmet gate, rationale, authorized
approver and approval evidence, scope, residual risk, and expiration/removal or
recheck condition. A proposed exception is not an approved exception.

Before implementation, confirm that the selected artifact and authorization
still match. If new metadata changes the decision, return to review. After
resolution, inspect every changed dependency and repeat the relevant checks
against the final graph; the manifest-level proposal alone does not cover a
different transitive result.
