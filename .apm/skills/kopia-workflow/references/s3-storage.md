# S3 storage for Kopia

Use a dedicated bucket prefix and a dedicated least-privileged AWS identity.
The identity normally needs bucket location and prefix listing plus the object
operations required by Kopia under that prefix. Derive the exact policy from
current Kopia and AWS documentation and confirm it with a bounded canary.

Keep the bucket in a region that meets recovery, latency, compliance, and cost
requirements. Begin with directly readable storage. Do not lifecycle-transition
Kopia repository objects into a delayed-retrieval class unless the current
Kopia workflow explicitly supports their restoration and the repository can
tolerate partial unavailability during retrieval.

Kopia connection configuration may persist the S3 endpoint, bucket, prefix,
access-key identifier, and secret. Protect the config as a credential-bearing
file. These storage-provider credentials are separate from the repository
password that Kopia can persist in the operating-system credential store. Prefer
a secret store and process-scoped environment injection where the storage
provider and operating mode support it. When a desktop UI requires persistent
connection state, restrict filesystem access and document rotation and
disconnect steps.

Routine snapshot verification should inspect repository metadata and errors.
Remote file-content reads and sample restores are separate, opt-in evidence
because they can incur material transfer, request, duration, and local-space
costs. State the selected percentage or paths and obtain explicit user approval
before starting. Even when the user already requested the read, state the exact
snapshot, subset, expected transfer, duration, local-space use, and cleanup
before execution; never silently turn a metadata check into a multi-gigabyte read.
