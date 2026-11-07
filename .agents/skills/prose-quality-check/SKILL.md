---
name: prose-quality-check
description: >-
  Review or revise explanatory prose for readability, local structure,
  audience fit, self-contained context, and preserved nuance. Use for wording
  in documentation, comments, release notes, issues, pull requests, changelogs, handoff notes,
  and Agent Skills after the document's purpose and factual ownership are known.
  Use domain-architecture-docs-workflow instead for repository-wide document
  maps, canonical ownership, technical evidence, coverage, or migration.
---

# Prose Quality Check

## When to Use

Use this Skill when the destination, factual source, and ownership are known
and the task is to improve how the text communicates. Use
`domain-architecture-docs-workflow` for repository-wide document maps,
canonical ownership, evidence, coverage, or migration decisions, then return
here to refine the prose. Flag unsupported technical claims rather than
silently repairing them through copyediting.

## Goals

- Make prose easy to scan without flattening meaning or adding distractions.
- Preserve nuance needed for decisions, safe implementation, or release interpretation.
- Fit the audience, document purpose, and local style.
- Make durable prose understandable without its originating conversation or an unstated date.

## Workflow

### Establish the edit

1. Identify the audience, purpose, intended claim, factual source, and destination.
   Reuse supplied context; resolve only gaps that could change the edit.
   Stop prose-only revision where ownership or evidence is disputed.
2. Select information for the reader's task. Retain what supports understanding
   or sound decisions; omit or separate distracting material. Brevity alone is
   not the goal.
3. Before editing prose intended for later independent use, read
   [durable context](references/durable-context.md) for conversation references,
   dates, versions, and history. This includes documentation, comments, Skills,
   and saved handoffs. A wording request does not authorize new publication or
   access changes.

### Review structure

Inspect the rendered text, not just physical source lines. Treat counts and
length as review cues, not quotas. Judge readability by meaning, relationships,
audience, language, and local format; do not impose fixed character, word,
sentence, paragraph, or item limits. Keep a longer coherent unit when splitting
would obscure its meaning, and avoid fragmented prose or excessive nesting.

1. Review each relevant level:
   - **Section:** Check how many paragraphs sit under a heading and how much
     material readers must scan. When distinct subtopics are hard to locate,
     shorten distractions, regroup paragraphs, or add meaningful subheadings.
   - **Paragraph:** Check sentence count and focus. Keep one coherent topic or
     reasoning unit; retain its useful evidence and consequences. Split at a
     genuine shift rather than turning every sentence into a paragraph.
   - **Sentence:** Check length, stacked clauses, and nested qualifications.
     Separate independently understandable ideas when this eases reading, while
     keeping conditions, causes, exceptions, and their consequences connected.
   - **List item:** Keep one independently reviewable point or action by default.
     Separate unrelated facts or independently actionable requirements. Related
     elements or supporting details may stay together; shorten or restructure
     an item when its length hides its point, not merely because it has several sentences.
   - **List:** Check item count, comparability, and scanning effort. Remove
     redundancy or group meaningful categories when that helps. Keep a coherent
     list intact when it is easier to use, preserving required items and sequence.
2. Choose the structure that helps the reader find and compare information.
   - Use familiar section patterns suited to the genre; do not force a report
     template onto every document.
   - Use concise, content-descriptive headings in a written register unless
     the genre or requested style calls for another tone. Prefer one clear
     expression over overlapping topics such as "Background and Purpose."
     Split topics when readers need to find them separately; do not ban
     punctuation within terms or meaningful enumerations. Add a short qualifier
     only when it distinguishes otherwise similar headings.
   - Prefer lists for enumerations, allowing inline wording when short and
     natural or clearer in the local style. Use subheadings, paragraphs,
     grouped bullets, or tables when they improve navigation or comparison.
3. Separate rendering from source wrapping. Prefer sentence-per-line source
   wrapping within an existing paragraph when the format permits it and review
   becomes easier. It is not a paragraph break. Do not disrupt short prose,
   links, lists, tables, or formatter-controlled comments, or change wording
   merely to accommodate wrapping.

For the rationale and limits of external guidance, consult
[writing guides](references/writing-guides.md).

### Preserve meaning

1. Preserve certainty, scope, timing, sequence, exceptions, limitations,
   dependencies, and compatibility. Keep original, backfilled, observed, inferred,
   planned, superseded, withdrawn, and unconfirmed statements distinguishable.
   - Name each independently readable spatial or state condition's subject and
     reference position; avoid an ambiguous "that position."
   - Keep independently evaluated conditions separate unless the factual
     source requires their conjunction. Splitting must not change AND to OR,
     detach a qualification, or change modality, tense, or voice without cause.
   - Preserve attribution and upstream relationships. A bare "official" must
     not transfer authority between projects. For example, describe the
     [Astral distributions used by uv](https://docs.astral.sh/uv/guides/install-python/)
     as Astral-published Python distributions, not official Python distributions.
2. Remove explanations or caveats that do not help readers act, decide, or
   understand. Prefer the current valid instruction when sufficient; do not
   narrate irrelevant rejected or legacy alternatives.
   - Disclose uncertainty that matters, without unrelated unknowns or
     precautionary "unverified" labels. Remove an unnecessary unsupported claim;
     flag a necessary evidence gap without implying verification.
   - Retain compatibility or migration context when the document owns the
     history or readers need it to update usage, interpret a release, or avoid
     a concrete transition risk.

### Verify in context

1. Re-read the edited passage with review depth proportionate to scope and risk.
   Compare its destination, claim, and retained wording with the request.
   Confirm each section, paragraph, and list has a clear job and still conveys
   the supported meaning without unnecessary caveats or repeated context.
2. Keep adequate surrounding headings and structure unless content or navigation
   gives a concrete reason to change them. Do not inflate a heading to squeeze
   in a new topic. Offer wider restructuring when needed rather than silently
   expanding a local edit into a full-document audit.
3. Use the owning domain Skill for document-specific checks. For a requested
   resumable handoff, use [handoff notes](references/handoff-notes.md), preserving
   factual ownership and the user's destination and level of detail.

## Markdown validation

When establishing repository-wide Markdown validation, copy
`assets/markdownlint-cli2.yaml` to `.markdownlint-cli2.yaml`, preserving rationale
comments and the rule baseline. Add a narrow override only for an evidenced
generated, vendored, submodule, renderer, or document-format requirement, and
document its reason beside the override. Prefer
an owning Skill's reviewed derived configuration, such as `hugo-quality-check`,
over recreating its exceptions. Use `github-actions-quality-check` for CI wiring.
