# Status and Qualifying Wording

Use these examples when a status or process term may be unnecessary, ambiguous,
or stronger than the evidence. The issue is the information added in context,
not the presence of a particular word.

## Editorial examples

- If the surrounding workflow already identifies the document under review,
  prefer its subject as the title rather than adding "reviewed version."
  A real distinction between a reviewed revision and a changed revision can
  still matter; retain it where readers need to choose between them.
- Replace "the approved version in the lockfile" with "the version pinned in
  the lockfile" when the pin is the relevant fact. If the instruction already
  says to use the lockfile and no version distinction matters, omit the extra
  phrase. A pin alone is not evidence of approval.
- A repository's own usage guide ordinarily belongs to the revision being read.
  Do not add "reviewed version," "approved version," or "default-branch
  version" merely to identify that context. Remove the qualification when
  unnecessary. Name a branch or revision when a real distinction matters,
  such as a branch workflow, release procedure, or CI target. Presence on the
  default branch alone does not establish review or approval.
- A pull request proposing a version update must not describe that proposal
  as already approved merely because approval is expected before merge.
  Use the version or proposed change, or state the pending decision when
  readers need it. Preserve an actual approval of the same revision when
  supported and relevant.
- "Get approval before publishing" needs an approver if readers cannot tell
  whose decision is required. "Ask the user to review the draft. Publish only
  after approval" already identifies the approver; repeating "by the user"
  need not help.
- A test report may need the checked environment, revision, and result.
  Include only the detail needed to interpret that result, rather than giving
  every use of "verified" a fixed date-and-version template.
  A needed "reviewed" claim must have an identifiable review basis; a needed
  "latest" claim must have a meaningful reference point or release channel.
  If the basis is unavailable, flag the consequential gap instead of inventing
  criteria or replacing the label with another unsupported assurance.
- In parallel installation requirements, "Install A, the latest B, and C"
  implies that B has a distinct freshness requirement. If no such difference
  is intended or needed, use "Install A, B, and C" rather than extending
  "latest" to all three. Preserve genuine minimum versions, security update
  requirements, or release-channel differences, making their scope clear.
  A literal `latest` tag or command argument is not a stylistic qualifier;
  do not change its operational meaning as part of a prose edit.
- If "latest" really applies to each item in "the latest A, B, and C," make
  that shared scope explicit, for example "the latest supported releases of A,
  B, and C." Repeat a necessary modifier in each independently read list item.
  Do not rely on readers guessing whether the first item's modifier extends
  to later items. Use different modifiers when different requirements apply.

## Repository example

[CruiserJumpPractice's installation guide](https://github.com/aoirint/CruiserJumpPractice/blob/9019e8bfd5e560bc64f1097fc72153b2b0cf62fa/README.md#L11-L15)
qualified the .NET 10 SDK with "latest" while neighboring PowerShell and Visual
Studio requirements did not. Its
[SDK configuration](https://github.com/aoirint/CruiserJumpPractice/blob/9019e8bfd5e560bc64f1097fc72153b2b0cf62fa/global.json)
sets a version and roll-forward behavior rather than requiring the newest SDK.
Removing the prose modifier avoids an unintended difference; the literal
`latestFeature` setting has an operational meaning and must be preserved.

## External cases

- [obra/superpowers, writing-skills](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/writing-skills/SKILL.md#L347)
  uses "Skill Creation Checklist (TDD Adapted)." Earlier sections already
  explain the application of test-driven development and its stages to Skill
  creation. The parenthetical is a low-impact redundancy candidate in that
  context; "Skill Creation Checklist" identifies the section without losing
  a needed distinction. This is not an unsupported approval claim.
- [ComposioHQ/awesome-claude-skills, instantly-automation](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/composio-skills/instantly-automation/SKILL.md#L78-L81)
  uses "Verified working" for timezone values beside mapped and unsupported
  values. The distinction helps configuration, but the file does not identify
  the observation's environment or method. Check the supporting evidence and
  clarify the relevant scope rather than simply removing the distinction or
  inventing a test result. This prose inspection did not test the API.
- [anthropics/skills, build-eval](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/claude-api/shared/evals/build-eval.md#L56-L64)
  pairs "Get the inputs approved" with "Do not proceed until the user has
  looked and said yes." The neighboring instructions establish the approver,
  subject, and gate. Keep the requirement; the heading need not repeat the user.
- [openai/skills, Playwright notice](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/NOTICE.txt#L1-L14)
  states "Adapted for the Codex skill collection" alongside the source,
  copyright, license, and changes. This identifies a derivative relationship
  in a notice, not a quality endorsement. Preserve the attribution and notice.

The pull-request and lockfile examples above are illustrative, not quotations
from the external sources.
