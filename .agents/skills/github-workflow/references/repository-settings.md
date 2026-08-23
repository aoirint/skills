# Repository Settings

Use this reference for repository-wide settings outside GitHub Actions. Run
commands with authenticated `gh`, replace `OWNER/REPO` with the exact reviewed
public destination, and restrict output to the fields needed as evidence.

## Pull-request creation cap

For a public repository, enable **Limit open pull requests from users without
write access** and set **Maximum open pull requests per user** to `1`. This cap
affects only users without write access. Draft pull requests do not count.
Preserve the existing bypass list unless the maintainer explicitly requests a
separately reviewed change.

The REST endpoint requires repository administrator access. Use GitHub API
version `2026-03-10`, and record the requested payload as
`{"enabled":true,"max_open_pull_requests":1}` before applying it.

```powershell
$repo = 'OWNER/REPO'

$repository = gh api --method GET `
  -H 'Accept: application/vnd.github+json' `
  -H 'X-GitHub-Api-Version: 2026-03-10' `
  "repos/$repo" `
  --jq '{full_name,visibility,admin:.permissions.admin}' |
  ConvertFrom-Json

if ($repository.full_name -ne $repo) {
  throw "Target mismatch: expected $repo, got $($repository.full_name)"
}
if ($repository.visibility -ne 'public') {
  throw "Pull-request creation cap is not applicable to $repo"
}
if ($repository.admin -ne $true) {
  throw "Administrator access is not verified for $repo"
}

gh api --method GET `
  -H 'Accept: application/vnd.github+json' `
  -H 'X-GitHub-Api-Version: 2026-03-10' `
  "repos/$repo/interaction-limits/pulls/creation-cap" `
  --jq '{enabled,max_open_pull_requests}'

gh api --method PATCH `
  -H 'Accept: application/vnd.github+json' `
  -H 'X-GitHub-Api-Version: 2026-03-10' `
  "repos/$repo/interaction-limits/pulls/creation-cap" `
  -F enabled=true -F max_open_pull_requests=1 `
  --jq '{enabled,max_open_pull_requests}'
```

Run the PATCH only when the user explicitly requests an apply and every
preflight check succeeds. Stop on a target, visibility, or authority mismatch;
do not reinterpret it as permission to select a different repository.

Immediately repeat the GET and require both stored values to match the
requested payload. For a non-public repository, record the setting as not
applicable. If the endpoint or administrator evidence is unavailable, record
the setting as unverified; do not infer it from another repository or the
PATCH response alone.

Authoritative sources:

- [GitHub repository interaction limits](https://docs.github.com/en/communities/moderating-comments-and-conversations/limiting-interactions-in-your-repository)
- [REST API endpoints for repository interactions](https://docs.github.com/en/rest/interactions/repos?apiVersion=2026-03-10)
