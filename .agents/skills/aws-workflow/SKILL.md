---
name: aws-workflow
description: >-
  Plan, apply, audit, and document AWS CLI changes with explicit authorization,
  least privilege, secret-safe execution, and post-change evidence. Use when
  provisioning or changing AWS resources, IAM identities or policies, S3
  backup storage, lifecycle rules, encryption, public-access controls, or
  long-lived credentials for a tool that cannot use renewable credentials.
---

# AWS Workflow

Make the smallest authorized AWS change and leave enough non-secret evidence
to distinguish the intended state from an apparently successful command.

## When to Use

- Use this Skill for AWS account and resource changes made through the AWS CLI.
- Pair with `security-check` for IAM, credentials, bucket policies, encryption,
  public access, destructive actions, or downloaded tools.
- Pair with `bws-workflow` when Bitwarden Secrets Manager stores or injects an
  access key. Do not duplicate secret values in reports or repository files.
- Consult current official AWS documentation when syntax, service behavior,
  pricing, regional support, or defaults can have changed.

## Goals

- Establish the active account, principal, region, authority, and exact target
  before changing state.
- Prefer renewable credentials and narrow policies; create a long-lived access
  key only when the consumer cannot use a renewable mechanism.
- Keep credentials out of arguments, output, shell history, repository files,
  and long-lived environment state.
- Verify changes through read-back and bounded behavioral checks.

## Workflow

1. **Establish identity and scope.**
   - Check the AWS CLI version and the relevant command help.
   - Run `sts get-caller-identity`; record the account and principal only in an
     approved private record when they are environment-specific.
   - Identify the requested resources, region, allowed state changes, expected
     consumers, rollback boundary, and evidence available before execution.
   - If identity, authority, target, or destructive scope is ambiguous, stop
     before the write and report the missing evidence.

2. **Inspect existing state.**
   - Read the exact resource and account controls that can override it.
   - Resolve names to stable identifiers where ambiguity matters.
   - Preserve unrelated configuration. Do not replace a whole policy or
     lifecycle document without comparing the current document first.

3. **Design the minimum change.**
   - Prefer service roles, workload identity, IAM Identity Center, or another
     renewable credential source over an IAM user access key.
   - When a long-lived key is unavoidable, dedicate the identity to one trust
     boundary, grant only required actions and resources, and define rotation
     and revocation ownership before creating it.
   - For S3 backup storage, read
     [S3 backup repositories](references/s3-backup-repositories.md).
   - Do not enable bucket versioning, Object Lock, or delayed-retrieval lifecycle
     transitions unless the environment explicitly selects them with a tested
     recovery, deletion, compatibility, and cost model.
   - Separate retention, recovery time, durability, and cost decisions. Do not
     select an archival tier solely because it has a low storage price.

4. **Apply without exposing secrets.**
   - Use structured argument arrays or reviewed input documents instead of
     interpolated shell strings.
   - Keep secret-bearing responses in memory. Disable tracing and verbose HTTP
     logs, and redact access-key identifiers as well as secret values from
     shared output.
   - If a command creates a credential, transfer it directly to the approved
     secret store and clean up transient variables. AWS cannot later retrieve
     the secret half of an access key.
   - Stop after an unexpected result; do not continue a multi-step setup on the
     assumption that an earlier zero exit code proved the requested state.

5. **Verify in layers.**
   - Read back exact configuration and compare normalized values.
   - Use IAM policy simulation as supporting evidence, not as proof of every
     runtime condition.
   - Where authorized and inexpensive, perform a bounded canary action with
     the intended principal and clean it up. Include a negative check outside
     the allowed resource or prefix when that boundary is security-critical.
   - Do not run broad, expensive, or destructive verification merely for
     completeness. State what was not tested and why.

6. **Record and hand off.**
   - Report the CLI version, region, redacted identity class, requested change,
     observed read-back, behavioral evidence, rollback or revocation path, and
     unresolved gaps.
   - Put reusable AWS guidance in the Skill. Put account IDs, resource names,
     local paths, adopted retention values, and operator decisions in the
     private system or repository that owns that environment.

## Failure Handling

- Treat authentication, authorization, region, service-control policy,
  permissions-boundary, bucket-policy, and KMS failures as distinct causes.
- If credential storage fails after key creation, deactivate or delete the
  exact new key before retrying unless an approved recovery path exists.
- For ordinary retirement, prefer deactivating the exact key, observing the
  agreed validation interval, and deleting it only after known consumers and a
  replacement access path are verified. Suspected compromise can require
  immediate revocation under the applicable incident procedure.
- Never widen a policy to make an unexplained failure disappear. Identify the
  denied action and controlling policy first.
- Require explicit authorization and an exact target before deleting resources,
  credentials, versions, recovery points, or retention controls.

## Completion Checklist

- The active identity, account, region, target, and authority were established.
- Existing state and controlling policies were inspected.
- The applied change was no broader than the request.
- No credential value entered logs, arguments, tracked files, or the report.
- Read-back evidence exists, and behavioral verification was bounded to risk.
- Untested behavior, rollback, rotation, cost, and update ownership are stated.
