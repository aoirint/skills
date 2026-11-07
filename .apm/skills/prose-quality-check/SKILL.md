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

## Goals

- Make prose easy to scan without flattening meaning or adding information the reader does not need.
- Preserve nuance that affects reader decisions, implementation safety, or release interpretation.
- Match structure to content: sentences for simple ideas, lists for enumerations, and nested bullets
  for grouped details.
- Keep wording aligned with the target audience and the local document style.
- Make durable prose understandable without the originating conversation or an unstated date.

## Responsibility boundary

Use this skill when the destination document, factual source, and ownership are already known and
the task is to improve how the text communicates. Do not use it to decide which repository
documents should exist, where a technical fact belongs, whether evidence is sufficient, or how a
documentation migration should preserve coverage. Use `domain-architecture-docs-workflow` for
those decisions, then return here to refine the resulting prose.

Do not silently repair unsupported technical claims while copyediting. Flag the evidence gap and
use the applicable documentation-system or domain-specific skill.

## Workflow

1. Classify the text audience before revising:
   - Developer-facing.
   - User-facing.
   - Maintainer-facing.
   - External-contract text.
2. Confirm the purpose, intended claim, factual source, and destination for this edit.
   Reuse context already supplied by the request or document; resolve only missing context that
   could change the edit. If ownership or evidence is disputed, stop prose-only revision at that
   boundary and report the gap. Use the document's purpose and intended message to select information:
   retain what the reader needs, and omit or separate lower-value material that distracts from the
   main point. Brevity alone is not the goal; preserve information needed for sound decisions.
3. Review context and time dependencies in prose intended for later independent use, including
   documentation, comments, Skills, and saved handoffs.
   - Replace references such as "this conversation" or "this chat" with the decision, subject,
     rationale, or scope the reader needs. Remove the reference when it adds no useful context.
   - Put essential context in the document, or cite an established source such as official
     documentation that supports the claim and is accessible to the intended readers. Check
     availability and audience access. A link alone does not make private or unavailable context
     usable. Do not publish a new external document or change access permissions merely to make
     the prose self-contained; those actions require separate authorization. Flag unresolved context
     or access gaps.
   - Treat "currently," "previously," "existing," and similar relative expressions as review cues,
     not banned strings. If the time distinction does not help the reader act or interpret the claim,
     remove it rather than attaching a date to an otherwise durable fact.
   - When a changing fact needs a time boundary, state the actual observation or effective date
     supported by the source. Use the coarsest unambiguous precision the claim needs: a year or
     month for a broad period, a full calendar date for a dated state, or a timestamp with time zone
     for a rapidly changing state. Include the year; do not invent precision or substitute the editing
     date for an unknown observation date. Flag missing temporal evidence instead of guessing.
   - State reader-relevant compatibility or applicability at the precision it needs, and omit version
     details that do not help the reader. Avoid duplicating incidental exact pins from authoritative
     configuration or lockfiles. Give human readers the needed version information in the document,
     even when an exact revision matters; do not send them to a lockfile for that information.
     Agent-facing instructions may direct the agent to authoritative lockfiles.
     Prefer major or minor version precision for human-facing scope when sufficient; retain exact
     revisions when behavior, compatibility, or reproduction needs them. Do not broaden a supported or tested range merely
     to simplify its notation. Consult authoritative pins when verifying the prose without shifting
     that lookup burden to human readers.
     Make human-facing runbooks self-contained for safe execution, retaining necessary exact commands
     and version constraints. Allow duplication needed for that purpose; weigh the reader's burden
     and execution safety against update drift, and keep the authoritative source and update needs
     clear. Use the owning workflow or domain Skill to verify the procedure and coordinate updates.
   - Preserve useful dated snapshots and qualified expectations about future change. Distinguish
     an observed state from a planned or possible state without turning a forecast into a guarantee.
   - After a behavior change, do not leave "existing behavior" dependent on the pre-change editing
     context. Retain earlier behavior only when the reader needs it, naming the relevant version,
     state, or date and why that distinction matters. Use `domain-architecture-docs-workflow` when
     deciding whether audience impact justifies retaining history in maintained documentation or
     referring readers to version-specific documentation. Preserve explicit compatibility, migration,
     and support requirements; do not remove a necessary transition step merely to avoid historical
     wording.
4. Identify overloaded prose:
   - Sentences carrying multiple ideas, conditions, time references, confidence levels, or
     relationships.
   - Paragraphs that mix context, decision, evidence, and consequence.
   - List items that contain several facts, exceptions, examples, or follow-up notes.
   - Spatial or state conditions whose thresholds use different subjects or reference positions.
     Name the subject and reference in every independently readable item; do not rely on a
     deictic phrase such as "that position" when it could refer to more than one value.
   - Independently evaluated conditions phrased as though they were one conjunction. Keep them
     separate unless the factual source establishes that every part is required together.
5. Choose headings and section patterns that fit the purpose, document type, and audience.
   - Prefer conventional structures, such as a report or research report when appropriate, so readers
     can find the sections they need. Do not force a report template onto every document.
   - Use content-descriptive headings in a written register by default, avoiding conversational
     phrasing. Preserve a different register when the genre or an explicit style requirement calls
     for it.
   - Keep headings concise; do not turn them into running summaries of the section. Prefer one
     clear expression over near-synonyms or overlapping topics joined by commas or middle dots.
     For example, avoid a combined heading such as "Background and Purpose" ("背景・目的").
     Choose "Background," "Purpose," or another single heading according to the section's main point
     when it covers both; split the headings when readers need to find each topic independently.
     Do not mechanically ban punctuation needed within a term or a meaningful enumeration.
     In a large document with similar neighboring headings, a short qualifier, such as text after
     a colon, can distinguish them. Use it only when the navigation benefit warrants it, not as a
     default.
   - Prefer lists when presenting enumerations.
     Use inline prose only when the enumeration is short enough to read naturally or when the local
     document style clearly favors inline wording.
6. Split or restructure dense text when it becomes hard to scan.
   - Use separate paragraphs, parent bullets with indented child bullets, tables, or another local
     document pattern that makes each idea easy to review.
   - When a sentence continues the same paragraph or comment block, prefer starting it on a new
     physical line if the local format allows that without changing the rendered structure.
   - Treat sentence-per-line wrapping as a reviewability aid, not as a paragraph break. Do not
     apply it when it would make short prose, Markdown links, lists, tables, or formatter-controlled
     code comments harder to read.
   - Do not change wording strength, modality, tense, or voice only to make sentence wrapping work.
     Keep wording unchanged unless an independent readability issue justifies rewriting it.
7. Remove explanations, caveats, and negative-space descriptions that do not help the reader act,
   decide, or understand the subject.
   - Disclose uncertainty that affects decisions, safety, or interpretation. Do not enumerate
     unrelated unknowns or add "unverified" labels as a precaution. If an unsupported claim is not
     needed, remove it; if it matters, flag the gap without implying the claim was verified.
   - Prefer the current valid instruction or example when it is sufficient on its own.
   - Do not add a disclaimer that an old or omitted form is rejected merely because the
     implementation no longer accepts it.
   - Retain compatibility or migration context when the document owns that history or the audience
     needs it to update existing usage, interpret a release, or avoid a concrete transition risk.
8. Preserve the nuance that made the original wording important:
   - Certainty or confidence level.
   - Scope and applicability.
   - Timing and sequence.
   - Exception or limitation status.
   - Dependency or compatibility relationships.
   - Attribution and upstream relationships. Avoid a bare "official" when it
     could transfer authority from one project to another. For example,
     [uv documents](https://docs.astral.sh/uv/guides/install-python/) that it
     uses Astral's `python-build-standalone` distributions because Python does
     not publish official distributable binaries. Describe those artifacts as
     "Astral-published Python distributions used by uv," not as "official
     Python distributions" or "uv's official Python distributions."
   - Whether a statement is original, backfilled, inferred, superseded, withdrawn, or still
     unconfirmed.
9. Use as many short sentences or nested bullets as needed. Do not force a fixed sentence count
   when the content needs a different shape.
10. Re-read the edited passage in context, scaling review depth to the change's scope and risk.
    Use the domain-specific skill when one owns the document type.
    - Preserve the surrounding structure by default, checking that it still fits the revised content.
      Keep headings that remain clear; changing them needs a concrete content or navigation reason.
      Do not append extra topics or qualifiers to an adequate heading merely to force new material
      into the same structure.
    - Review wider structure when the edit warrants it, rather than making every small correction
      trigger a full-document audit. Offer a broader review when needed instead of silently expanding
      a local edit.
    - Compare the actual edited destination and scope with the request and any wording or meaning
      the user asked to retain.
    - Confirm it still answers the same question as the original wording.
    - Confirm each list or paragraph has one clear job and reads naturally, without unnecessary
      caveats or repeated context.
    - Confirm the structure did not imply a stronger, weaker, broader, or narrower claim than the
      source material supports.
11. When establishing repository-wide Markdown validation, copy
    `assets/markdownlint-cli2.yaml` to `.markdownlint-cli2.yaml` without
    deleting its rationale comments or changing its rule baseline. Add a local
    ignore or exception only for an evidenced generated, vendored, submodule,
    renderer, or document-format requirement, and document that reason beside
    the narrow override. When an applicable domain Skill owns a reviewed derived
    configuration, such as `hugo-quality-check`, use that asset instead of
    recreating its exceptions in the consumer. Use `github-actions-quality-check`
    to wire the repository-owned configuration into CI.

## Optional handoff notes

For a requested resumable handoff, use [handoff-notes.md](references/handoff-notes.md) to select the
decisions and open questions the next reader needs. Keep the existing factual-ownership boundary
and preserve the user's choice of destination and level of detail.

## Output checklist

- Audience and document type were considered before rewriting.
- Factual ownership and evidence gaps were not silently decided through wording changes.
- Durable prose carries its needed context or an audience-accessible reference; no new publication
  or access change was inferred from a wording request.
- Unnecessary relative time was removed, and material time boundaries use source-supported dates
  at appropriate precision without losing useful history or uncertainty.
- Headings and section patterns fit the purpose and help the reader find relevant content.
- Enumerations are lists unless inline prose is clearer for the local context.
- Dense paragraphs or list items were split or intentionally left intact.
- Current instructions do not narrate irrelevant rejected or legacy alternatives.
- Important certainty, scope, timing, relationship, and status nuances were preserved.
- The final text is easier to scan and still communicates the same claim.
