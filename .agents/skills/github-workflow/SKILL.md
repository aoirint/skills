---
name: github-workflow
description: >-
  Quality-check GitHub Actions workflows, repository issues, pull requests, and
  their comments. Use when creating, editing, reviewing, or documenting CI
  automation, issue text, PR text, reviews, replies, or squash merges.
---

# GitHub Workflow

## When to Use

Use this skill to create, update, or review a GitHub artifact. First identify
the artifact and apply only its relevant workflow:

- GitHub Actions workflow, composite action, or CI policy: use **Actions**.
- Issue title, body, comment, or thread note: use **Issues**.
- Pull request title, body, review, reply, thread note, or squash merge: use
  **Pull requests**.

Use `security-check` for security- or supply-chain-sensitive content and
`prose-quality-check` for nuanced explanatory prose.

## Goals

- Keep automation deterministic, least-privilege, and reviewable.
- Keep issue and pull request artifacts concise, accurate, and explicitly
  AI-assisted when significant AI assistance was used.
- Preserve repository templates and policies without inventing unavailable
  requirements.

## Workflow

### Actions

1. Inspect changed workflow or action files and the repository guidance that
   describes them.
2. Check triggers, branch filters, merge-queue behavior, and
   `workflow_dispatch` against the intended responsibility. Preserve
   established publication triggers and canonical version sources unless the
   request explicitly replaces them. Design boundaries around events,
   privilege, and lifecycle:
   - A pull-request entry workflow validates untrusted proposed source and
     includes `merge_group` when a merge queue uses required checks.
   - An integration-branch entry workflow re-runs required validation on the
     exact pushed commit. Use a read-only `plan` job only for canonical version
     or publication state, and make build and publication use direct `needs`
     dependencies.
   - Name jobs for visible responsibility: `lint`, optional `test`, optional
     `plan`, `build`, and `release`. Use a precisely named Composite Action
     only for a reusable same-runner sequence.
   - Do not emulate a direct dependency with API polling, an `await-quality`
     job, or an unrelated workflow. Add `workflow_dispatch` only for a
     documented diagnostic or recovery operation. Use `workflow_run` only for
     a separately reviewed trust boundary.
3. Check workflow and job `permissions`. Start from `contents: read`, grant
   only required access, and document unusual write access. Check concurrency
   groups and cancellation rules for PRs, pushes, releases, merge queues, and
   publishing.
4. Check runner labels, local composite actions, expressions, comments, cache
   paths, and suppressions. Read
   [runner-selection.md](references/runner-selection.md) when selecting or
   changing a GitHub-hosted runner. Validate action inputs against documentation
   or metadata for the exact pinned version. Use a Composite Action for a
   stable same-runner sequence; use a reusable workflow only when job-level
   matrix, outputs, or permission boundaries require it.
5. Pin third-party actions and reusable workflows to complete commit SHAs with
   accurate version comments. For external actions, downloaded tools, or
   containers, use `security-check` to review provenance, release age, pinning,
   permissions, and runtime behavior.
6. Run documented `actionlint`, ShellCheck, and `pinact` checks. Use
   `pinact run --check --min-age 7` and `GITHUB_TOKEN` when available. Check
   standalone changed automation shell scripts with ShellCheck; record an empty
   target scope when none exist.
7. For publishing workflows, gate immutable publication on all required quality
   and build results for the exact source commit. Retain verified build
   artifacts, derive release identity from the canonical version source, make
   retries idempotent, verify existing immutable releases and expected assets,
   isolate credentials, and use `security-check` for final artifacts.
8. For repository enforcement, compare required status-check contexts with
   current workflow job names and verify integration freshness, merge-queue
   compatibility, release immutability, tag rules, Actions permissions, and
   protected environments. Mark inaccessible settings as unverified.
9. Summarize actionlint, ShellCheck, pinact, other automated checks,
   AI-assisted inspections, and skipped checks separately.

### Issues

1. Identify whether the artifact is an issue title, body, reply, or combined
   update. For significant AI assistance, put the applicable alert at the very
   top:

   ```markdown
   > [!WARNING]
   > This issue was created with assistance from LLMs.
   ```

   Use `This comment was created with assistance from LLMs.` for replies.
2. Make titles concise and specific. Keep bodies and replies concise, using
   only useful sections such as `Summary`, `Details`, `Acceptance Criteria`,
   `Verification`, `Notes`, `Findings`, or `Next Steps`. For bugs, state
   expected and actual behavior and useful reproduction steps.
3. Write in English except for exact source material. Use bullets, backticks,
   explicit uncertainty, and summaries rather than large logs or diffs. Never
   describe AI-performed work as manual.
4. Add `Update Note` or `Discussion Note` only when requested. Put
   `Request addressed: ...` after the required alert and before the note
   heading; label inferences and omit secrets and private paths.
5. With `gh`, write Markdown to a temporary file and pass `--body-file`.
   Verify stored issue bodies with `gh issue view --json body` and stored
   replies when possible, then remove temporary files.

### Pull requests

1. Identify the artifact: title, body, review, reply, thread note, or squash
   merge. For titles, enforce
   `<type>[optional scope][optional !]: <description>` and use
   `commit-message-quality-check` for type and breaking-change notation.
2. Before drafting or replacing a body, read the current PR template and
   contributor guidance. Follow only visible headings, required checkboxes, and
   applicable sections. If no template exists, use
   [fallback-pr-body.md](references/fallback-pr-body.md). Never infer a CLA,
   contributor agreement, checklist, sign-off, or policy from the fallback.
3. For significant AI assistance, put this alert at the absolute top of PR
   bodies:

   ```markdown
   > [!WARNING]
   > This pull request was created with assistance from LLMs.
   ```

   Use `This comment was created with assistance from LLMs.` for reviews,
   replies, and thread notes. Preserve any existing alert after a blank line;
   the LLM alert must be exactly once and first.
4. Keep automated commands, CI results, non-AI manual checks,
   screenshots/videos, and AI-assisted inspections distinct. Under
   `## Testing`, put AI-assisted work in `### AI-assisted inspections` after
   automated checks with `Request: ...` and nested `AI-assisted result: ...`.
   State skipped verification and never describe AI work as manual.
5. Use `Update Note`, `Discussion Note`, or `Review Note` only when requested.
   Put `Request addressed: ...` after the required alert; group retrospective
   notes by meaningful theme, label inferences, and omit secrets, private
   paths, and hidden reasoning.
6. Before writing an AI-assisted body or comment, run
   `scripts/check_llm_disclosure.py` against the candidate. For a
   disclosure-only repair, pass the exact prior body. After writing, fetch the
   complete JSON response and run the helper against that response and the
   candidate. For multi-artifact work, preflight every candidate, verify each
   write immediately, audit all targets at the end, and report success only
   when every target has exactly one required top alert and a matching body.
7. With `gh`, use `--body-file`. Verify the complete JSON `body` as one string
   against the candidate, allowing only terminal-newline normalization; in
   PowerShell do not assign line-oriented `--jq` output to verify multiline
   bodies. Remove temporary files.
8. Before `gh pr merge` creates a squash or merge commit, resolve and pass the
   exact head SHA with `--match-head-commit`. Build and validate the exact
   multiline candidate commit message in a file with
   `git interpret-trailers --parse`, require each expected trailer exactly
   once, test the stored-message JSON parser with a fixture, merge with the
   same body file, then verify `commit.message` from
   `repos/{owner}/{repo}/commits/{sha}` using raw JSON. Treat post-merge
   verification as secondary to pre-mutation validation.

## Resources

- [runner-selection.md](references/runner-selection.md): GitHub-hosted runner
  selection and image-lifecycle guidance.
- [fallback-pr-body.md](references/fallback-pr-body.md): fallback PR template
  when no repository template applies.
- `scripts/check_llm_disclosure.py`: validate required LLM disclosure,
  disclosure-only repairs, and stored-body preservation.
