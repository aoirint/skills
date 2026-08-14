# S3 backup repositories

Use this reference when an AWS change creates or changes S3 storage for a
backup tool.

## Establish the contract

Record the owning system, region, bucket and optional prefix, expected writers,
restore readers, retention, recovery time, expected object churn, and deletion
owner. Generate a globally unique bucket name without embedding account IDs,
usernames, email addresses, or sensitive project names.

## Baseline controls

- Block public access at the bucket. Inspect account-level controls too, but do
  not change them unless that broader scope is authorized.
- Deny requests that do not use TLS.
- Enable default server-side encryption. Choose SSE-S3 unless an established
  requirement needs KMS key policy, audit, or separation of duties.
- Add a rule to abort incomplete multipart uploads after a bounded interval.
- Grant the backup identity only required bucket-listing and object actions,
  scoped to the exact bucket and prefix.
- Keep delete permissions separate from write permissions when the backup
  workflow supports that split.

Bucket versioning and Object Lock are decisions, not universal defaults. A
content-addressed backup repository already has its own history; S3 versions can
multiply storage and deletion complexity. Object Lock can protect against
malicious deletion but can also prevent repository maintenance. Adopt either
only with a tested recovery and cost model.

## Storage class

Start with a storage class the backup software can read directly. Lifecycle
transition to a delayed-retrieval archival class can make repository indexes or
content unavailable to normal operations. Intelligent-Tiering also has fees and
archive-access behaviors that must be checked against the current workload and
tool support. Measure before adding transitions.

## Verification

Read back public-access block, encryption, lifecycle, bucket policy, and IAM
policy. Where authorized, use the backup principal for a small create, read,
list, and delete canary in the allowed prefix, plus a denied action outside it.
Clean up only the canary objects. This verifies access boundaries; it does not
replace the backup tool's repository and restore checks.
