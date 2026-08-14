---
name: kopia-workflow
description: >-
  Design, configure, operate, migrate, and recover Kopia backup repositories
  with explicit source boundaries, retention, replication, secret handling,
  and cost-bounded verification. Use when choosing repository granularity,
  connecting filesystem or S3 storage, creating policies and snapshots,
  moving data between active and archive tiers, synchronizing repositories,
  expiring snapshots, or proving restore readiness.
---

# Kopia Workflow

Use Kopia as a versioned recovery system without making its repository format,
remote storage, or verification cost an invisible operational dependency.

## When to Use

- Use this Skill for Kopia CLI or KopiaUI repository lifecycle work.
- Pair with `security-check` when credentials, permissions, downloaded binaries,
  repository deletion, retention reduction, or remote storage are involved.
- Pair with `aws-workflow` for S3 buckets and IAM, and with `bws-workflow` when
  Bitwarden Secrets Manager provides repository or cloud credentials.
- Check current Kopia help and official documentation before relying on flags,
  compatibility, repository-format, or storage-provider behavior.

## Goals

- Define what a repository protects, where its independent copies live, and
  who can restore it before taking snapshots.
- Preserve whole-workspace history efficiently through content-addressed,
  incremental snapshots instead of manual full copies.
- Keep repository and cloud credentials out of logs and tracked files.
- Match verification depth to risk, transfer cost, and expected duration.

## Workflow

1. **Inventory sources and recovery needs.**
   - Identify source roots, active and inactive data, final deliverables,
     generated caches, exclusions, expected change rate, restore target, and
     acceptable data loss and recovery time.
   - Choose repository boundaries by trust, retention, destination, and failure
     domain rather than by every source directory. Read
     [repository lifecycle](references/repository-lifecycle.md).
   - Keep final deliverables separate when they need different retention,
     discovery, or restoration from editable workspaces.

2. **Establish software and storage.**
   - Verify the installed Kopia version, executable provenance, and the exact
     command help. Install or update only when requested.
   - For S3, read [S3 storage](references/s3-storage.md) and establish the bucket,
     region, prefix, encryption, access controls, and least-privileged identity
     before repository creation.
   - Prefer local active data plus an independent repository. A repository on
     the same physical device is useful for history but is not an independent
     disaster-recovery copy.

3. **Protect credentials.**
   - Inject repository and storage credentials at process scope from an
     approved secret store. Do not print environment values or put passwords
     in command arguments, scripts, workspace documents, or shell history.
   - Treat Kopia connection configuration as sensitive because it can contain
     storage credentials even when the repository password is held elsewhere.
   - Verify the resulting connection and source list directly. Wrapper success
     alone is insufficient when the wrapper may not propagate a child failure.

4. **Set policy before relying on snapshots.**
   - Configure retention, scheduling, compression, ignore rules, and error
     handling at the narrowest stable source boundary.
   - Exclude only reproducible data whose regeneration cost is acceptable.
   - Use pinned snapshots for intentional milestones, not as a substitute for
     a coherent retention policy.

5. **Create and classify snapshots.**
   - Snapshot stable source roots and record non-secret source identity,
     snapshot ID, start and end time, file and byte counts, errors, and policy.
   - Moving a directory between protected source roots creates new source
     metadata but can reuse repository content. Keep the earlier snapshot until
     the new classification and restore path are verified.
   - Do not infer success from command exit alone; inspect the snapshot and any
     incomplete-file or policy warnings.

6. **Replicate deliberately.**
   - Use repository synchronization only between compatible Kopia repositories.
     Read current `repository sync-to --help` before use.
   - Require the destination to exist, identify sync direction, and omit
     deletion propagation by default. A periodically attached external disk
     may lag safely if the missing-device case fails closed.
   - Repository synchronization copies backup history; moving a source between
     repositories does not inherently transfer its prior snapshot history.

7. **Verify at the required depth.**
   - Default routine verification to repository connection, snapshot listing,
     metadata, object/index consistency, and error review. A local content check
     must name its paths or byte limit and must not fetch remote content.
   - Do not perform large remote real-read verification or restore sampling by
     default. It can consume substantial time, egress, request volume, and local
     space. Run it only after the user explicitly requests it or approves a
     risk-justified proposal. Before every remote read, including one already
     requested, state the exact snapshot and subset, expected transfer and
     duration, local-space use, comparison method, and cleanup. Resolve any
     undefined or materially changed bound with the user before execution.
   - For restore-readiness tests, restore a named bounded subset to a separate
     location, compare expected files or hashes, then remove only the verified
     temporary target. Never restore over the source as a test.

8. **Expire and reclaim safely.**
   - Snapshot expiration changes logical retention; maintenance controls when
     unreferenced content can be physically reclaimed.
   - Before deleting snapshots or a repository, resolve exact targets, confirm
     remaining recovery coverage and replicas, and state whether the action is
     reversible.
   - Keep repository-format compatibility and Kopia installation instructions
     with long-lived archive records.

## Failure Handling

- Stop on a missing external destination, wrong repository connection, source
  mismatch, credential ambiguity, incomplete snapshot, or unexpected deletion.
- Distinguish a source read failure, repository write failure, network failure,
  maintenance failure, and restore mismatch before retrying.
- Do not create a replacement repository over an unrecognized existing prefix.
- Do not reduce retention or propagate deletes simply to resolve capacity
  pressure; inventory recoverable copies and obtain authorization first.

## Completion Checklist

- Source, repository, replica, retention, and restore responsibilities are named.
- Credentials are process-scoped or stored in an approved protected config.
- Snapshot IDs and errors were inspected after state-changing operations.
- Replication direction and deletion behavior are explicit.
- Verification depth is documented, including intentionally omitted remote reads.
- Destructive actions have exact targets, recovery coverage, and authorization.
