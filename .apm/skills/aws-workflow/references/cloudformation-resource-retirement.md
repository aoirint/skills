# CloudFormation Resource Retirement

Use this reference when existing AWS resources must enter CloudFormation or CDK ownership before a
destructive retirement, or when a short-lived application stack depends on a retained CDK bootstrap
foundation.

## Establish the boundary

- Inventory direct resources and attachment edges before designing the stack. Classify each as
  stack-owned, shared and retained, service-managed, or deletion-generated such as an EC2 root
  volume.
- Read the current CloudFormation import support and identifier schema for every resource type.
- Keep account IDs, ARNs, physical IDs, private addresses, import mappings, and raw responses in an
  approved private evidence location, not reusable source or Skill text.
- Treat root-volume deletion, policy-version deletion, and stack deletion as separate destructive
  effects requiring exact-target evidence.

## Separate bootstrap from the application

CDK bootstrap creates account-region infrastructure used by deployments. A short-lived application
stack does not imply that the bootstrap stack is short-lived.

- Obtain explicit authority before the first bootstrap because it creates persistent IAM, S3, ECR,
  SSM, and CloudFormation resources according to the selected template version.
- Pin and review the CDK CLI, verify the account and region, and inspect trust, execution policies,
  public-access controls, and qualifier choices before applying.
- Prefer termination protection for a retained bootstrap stack and read back its status and
  bootstrap version after creation.
- If bootstrap is not authorized, do not disguise that gap. A reviewed CloudFormation import change
  set from a synthesized asset-free template can be a bounded fallback, but it is a different
  workflow with independently verified permissions and ownership.

## Import without replacement

1. Model the live resource with explicit deletion and update-replacement policies. Prefer low-level
   constructs when exact import properties matter.
2. Synthesize and compare the template with service and Cloud Control read-back.
3. Generate physical-resource mappings into ignored private storage.
4. Review the import change set. Every intended action must be `Import`; stop on an update, delete,
   replacement, unexpected logical resource, or unrelated stack change.
5. Execute the import, read back stack resources, and run drift detection before any update or
   destruction. Import success alone does not prove property parity.

## Respect service-managed IAM edges

IAM Identity Center owns permission sets and the generated `AWSReservedSSO_*` roles. Do not attach
or detach policies on those roles through IAM or a CloudFormation managed policy `Roles` property.

When retiring a customer-managed policy referenced by a permission set:

1. Preserve unrelated permission-set references.
2. Remove the retiring reference through Identity Center and provision the permission set to the
   target account.
3. Wait for provisioning success and verify the generated role's live attachment is absent.
4. Import the now-unattached managed policy with no `Roles` property, then delete it through the
   stack.

This order prevents CloudFormation from attempting a protected-role mutation. For future creation,
deploy the unattached policies first, then add their names to the permission set and provision it
through Identity Center.

## Destroy and recover safely

- Reconfirm the exact stack, owned physical resources, external dependencies, deletion policies,
  and irrecoverable data boundary immediately before destruction.
- IAM managed policies can have multiple versions. Before an authorized direct-policy deletion,
  delete every non-default version; deleting the policy removes its default version.
- If a legacy imported template contains `Roles` and stack deletion fails on a protected generated
  role, stop. Prove that the permission-set reference and live attachment are absent. Only then may
  an explicitly authorized recovery delete the exact policy versions and policy out of band before
  retrying stack deletion. Record the divergence.
- Do not treat stack deletion as sufficient evidence. Verify each owned resource is absent or in its
  terminal state, including deletion-generated storage, and read back every retained shared or
  service-managed dependency.

The handoff must distinguish recoverable retained prerequisites from irrecoverable deleted data and
state any stale descriptions, assignments, or access metadata that remain but do not grant the
retired permissions.
