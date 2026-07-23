# Repository Family Alignment

Use this procedure when the maintainer names peer repositories, asks for a
horizontal rollout, or expects a new mod to follow an established repository
family.

## Establish the comparison

1. Record the target repository, every maintainer-designated peer, and the exact
   reviewed revision of each repository. Do not choose a different exemplar
   because it appears newer or more complete.
2. Preserve repository visibility. Inspect a private target through its local
   checkout or authenticated tooling, and do not copy its unpublished source,
   logs, or configuration into public issues, pull requests, or repositories.
   Privacy can block an external publication side effect; it does not by
   itself justify omitting package assets, validation, or an inert publisher
   action needed to make the repository publication-ready.
3. Inventory tracked paths, directory shape, file order and section structure,
   portable file contents, toolchain selectors, CI composition, package-host
   assets, and line-ending attributes. Compare content structure and newline
   policy, not only filenames.
4. Treat content shared by all designated peers as the presumptive family
   baseline. When peers differ, prefer a documented canonical template, then a
   peer whose role the maintainer designated. If neither exists, preserve the
   target until the difference is resolved or promote a portable improvement
   to a new canonical source and roll it out to compatible peers. Do not stop
   unrelated work, select by apparent recency, or silently blend peers.

## Build a delta ledger

Classify every target difference before editing:

| Difference | Required question |
| --- | --- |
| Missing from target | What target constraint makes the shared file or section inapplicable? |
| Extra in target | What product, runtime, test, host, visibility, or maintenance requirement needs it? |
| Changed in target | Why can the portable peer content not be reused unchanged? |

For each row, record the exact target path, peer path, disposition, and reason.
Use one of these dispositions:

- `match`: copy or render the canonical content exactly;
- `target-specific`: keep the smallest necessary difference and name the
  concrete constraint;
- `canonical-improvement`: change the canonical source first, validate it, and
  roll it out to every compatible consumer;
- `remove`: delete an unexplained target-only addition after preserving any
  still-required facts in their canonical owner.

"Stricter", "cleaner", "newer", "more explicit", and "best practice" are not
sufficient reasons to fork a shared file. If a stricter control is portable,
propose it in the canonical source and roll it out; if it is not portable, name
the target-specific threat or compatibility condition.

## Apply the minimum difference

1. Copy exact portable files from the canonical template or render only the
   declared variables. Do not rewrite wording, comments, step names, ordering,
   indentation, or metadata outside those variables.
2. Preserve shared files that the target does not need to execute directly when
   they are part of the family governance contract, such as `AGENTS.md`, APM
   metadata, notices, contributor policy, ownership, and template drift checks.
3. Keep product code, game integration, test projects, active publication
   steps, and private/public release paths different only where the delta
   ledger names the requirement. Keep portable package assets, final-archive
   validation, and publication tooling aligned even when an external publish
   step remains disabled pending authorization or credentials.
4. Apply the shared `.gitattributes` before broad edits and renormalize tracked
   text. Verify the worktree newline policy separately from Git's normalized
   index representation.
5. Do not add documentation categories or evidence machinery merely because a
   general baseline permits them. Match the family document map and add a
   concern only when it has a distinct owner, audience, and change lifecycle.
6. Keep the family workflow entry points and ownership boundaries. When the
   family uses `pull-request.yml` and `main.yml`, add target-specific jobs or
   values inside that split instead of inventing a combined workflow. Keep
   packaging in CI, preserve stable publication while version `0.0.0` blocks
   it, and remove duplicate packagers only after CI owns every required step.

## Documentation and history hygiene

1. For Lethal Company build identity in public compatibility documentation,
   use the Steam Build ID and Steam Manifest ID. Document loader, dependency,
   and runtime facts separately; do not expose local extraction paths, private
   repository details, or redundant handoff hashes.
2. Match the family document names, section hierarchy, prose granularity, and
   terminology. Avoid repeating the game version in filenames, headings, and
   prose when one compatibility owner already establishes it. Use direct
   domain wording instead of foregrounding analysis or trace mechanics.
3. When the maintainer explicitly requests a history rewrite, treat unwanted
   private names, machine paths, or incorrect license text as a reachable-ref
   audit. Correct the current tree, rewrite only the authorized repository,
   inspect all branches and tags, then re-scan exact strings before pushing.
   Coordinate any force-push for already-shared history, and do not reproduce
   the removed private text in a public change description.

## Independent review loop

When the maintainer requests convergence review, give a fresh evaluator only
the raw target, peer revisions, privacy boundary, and comparison rule. Do not
provide the intended fixes or earlier findings. After each correction round,
use a new evaluator and repeat until a complete pass reports no actionable
material difference. Record genuine target-specific differences so reviewers
do not repeatedly propose destructive parity.

## Completion contract

Report:

- peer revisions and canonical template revisions;
- shared files matched exactly;
- every remaining target-specific difference and its concrete reason;
- canonical improvements and their rollout status;
- line-ending, template-drift, build, test, CI, package, and privacy checks; and
- any difference still lacking a disposition.

Do not call family alignment complete while an addition, omission, content
fork, or newline-policy change lacks a ledger disposition.
