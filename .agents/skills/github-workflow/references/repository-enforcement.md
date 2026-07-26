# Repository Enforcement Recovery

Use this flow when a default-branch ruleset is missing or lacks required
pull-request or status-check rules. Run the commands from the target
repository with authenticated `gh`; replace `OWNER/REPO`, check contexts, and
full commit SHAs with observed values.

## 1. Inventory before changing policy

```powershell
$repo = 'OWNER/REPO'
gh api "repos/$repo" --jq '{default_branch,allow_squash_merge,allow_merge_commit,allow_rebase_merge,allow_auto_merge,allow_update_branch,delete_branch_on_merge,squash_merge_commit_title,squash_merge_commit_message}'
gh api "repos/$repo/immutable-releases"
gh api "repos/$repo/actions/permissions"
gh api "repos/$repo/actions/permissions/selected-actions"
gh api "repos/$repo/rulesets"
```

Treat an unavailable setting as unverified. Do not infer a fork-workflow
approval policy or ruleset bypass from another repository.

## 2. Apply the safe fallback ruleset

When no check context has been observed on a pull request, create or update
the `default` ruleset with every other baseline rule: target the default
branch, restrict deletions and force pushes, require pull requests, allow only
squash merging, and allow repository-admin bypass only on pull requests.
Omit only `required_status_checks`; record the ruleset as incomplete and do
not claim status-check enforcement.

Use the template in section 4 after removing its
`required_status_checks` object. For an existing ruleset, preserve unrelated
rules and send the complete reviewed replacement with `PUT`.

## 3. Make a required-check context safe to require

1. Add or adapt a validation workflow that runs the intended job on
   `pull_request`. Add `merge_group` when the repository uses a merge queue.
2. Give the job a stable visible name, such as `lint` or `test`.
3. Merge that workflow change to the default branch.
4. Open a pull request and wait for a successful run. Confirm the exact
   context before adding it to the ruleset:

   ```powershell
   gh pr checks <number> --required
   ```

Do not require a job that runs only on `push`, a release job, or a context
whose current name was not observed on a pull request.

## 4. Restrict Actions without breaking composites

Inventory `uses:` in workflow files and all reachable local composite actions
or reusable workflows. Preserve local actions and GitHub-owned actions; allow
only the exact full-SHA external references that the inventory finds.

```powershell
gh api --method PUT "repos/$repo/actions/permissions" `
  -F enabled=true -f allowed_actions=selected -F sha_pinning_required=true

gh api --method PUT "repos/$repo/actions/permissions/selected-actions" `
  -F github_owned_allowed=true -F verified_allowed=false `
  -f 'patterns_allowed[]=EXTERNAL_OWNER/ACTION@FULL_40_CHARACTER_SHA'
```

Repeat `patterns_allowed[]` only for additional observed external references.
Read back both endpoints after the change. Never use a wildcard pattern when
the inventory provides a full SHA.

## 5. Create or complete the default ruleset

Save the following JSON as `ruleset.json` after replacing `lint` with an
observed pull-request check context. Repository role ID `5` is the `admin`
role; its bypass mode is limited to pull requests. If no context is available,
remove the complete `required_status_checks` object and apply the fallback from
section 2.

```json
{
  "name": "default",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request" }
  ],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": { "allowed_merge_methods": ["squash"] } },
    { "type": "required_status_checks", "parameters": {
      "strict_required_status_checks_policy": true,
      "do_not_enforce_on_create": false,
      "required_status_checks": [{ "context": "lint" }]
    } }
  ]
}
```

```powershell
gh api --method POST "repos/$repo/rulesets" --input ruleset.json
```

For an existing ruleset, fetch it first, preserve every unrelated rule, and
send the complete reviewed replacement to `PUT repos/$repo/rulesets/<id>`.

## 6. Verify the stored policy

```powershell
gh api "repos/$repo/rulesets" --jq '.[] | select(.name == "default") | .id'
gh api "repos/$repo/rulesets/<id>"
```

Confirm the target is `~DEFAULT_BRANCH`, deletion and force pushes are
restricted, pull requests allow only squash merging, the observed check is
required, and the only baseline bypass is repository-admin with
`pull_request` mode.
