---
name: english-prose-quality-check
description: >-
  Draft or revise English prose for natural phrasing, clear grammar, appropriate
  register, and consistent usage. Use for English text or translations into
  English, including documentation, PRs, comments, and messages.
---

# English Prose Quality Check

## When to Use

Use for English expression within an established audience, purpose, and scope.
Use `prose-quality-check` for language-independent structure, durable context,
references, and status wording when available; this Skill owns English-specific
phrasing. Copyediting does not authorize changing technical facts or publishing.

## Goals

- Make grammatical relationships and intended meanings clear.
- Replace awkward or translation-shaped phrasing without flattening the voice.
- Distinguish grammatical errors from valid regional and editorial choices.

## Workflow

### Establish usage

Read the surrounding text and any glossary or house style. Preserve its English
variety, register, and audience rather than defaulting every document to US
English or formal prose. Use established spelling and punctuation consistently,
but retain deliberate differences in quotations, labels, and speakers. For a
local edit, do not standardize the whole document without a reason.

### Clarify grammar

- Check agreement, countability, articles, and number. Choose `a`, `an`, `the`,
  or no article from the noun phrase and intended referent, not from neighboring
  items' appearance. Product names and common nouns can behave differently;
  preserve official naming and consider the whole phrase before changing it.
- Check pronoun antecedents, modifier attachment, and relative clauses. Place
  `only` and other limiting words where their scope is clear. Repair dangling
  modifiers without inventing an actor. Punctuation around a relative clause
  can change which objects are included; do not add commas merely for rhythm.
- Keep coordinated items grammatically parallel without making distinct actions
  or requirements identical. Repeat a preposition, determiner, or verb when
  readers would otherwise be unsure which items it governs.
- Preserve tense, aspect, and modality. Distinguish capability, permission,
  advice, and obligation instead of treating `can`, `may`, `should`, and `must`
  as stylistic alternatives. Keep meaningful differences between a completed
  event, an ongoing state, and a hypothetical condition.

### Refine phrasing

Use idiomatic verb–noun combinations and prepositions rather than translating
individual words or retaining the source language's order. Unpack noun strings
when their relationships are hard to follow. Prefer a direct verb over a heavy
nominalization when the meaning and emphasis stay intact.

Use active voice when it clarifies who acts. Keep passive voice when the actor
is unknown, irrelevant, or less important than the result; never invent an actor
to satisfy a style preference. In instructions, distinguish what the reader does
from what the system does.

For a broad technical audience, prefer precise, familiar expressions over
culture-specific idioms or ornamental phrasing. Retain useful technical terms
and natural expressions such as `sign in`; do not replace every phrasal verb or
contraction mechanically. Avoid imposing blanket bans on passive voice, split
infinitives, sentence-final prepositions, or singular `they`.

### Check consistency

Keep terminology, capitalization, hyphenation, and punctuation consistent where
they serve the same function. Preserve literal UI labels, identifiers, commands,
and quoted material. A valid difference in grammar is not an inconsistency;
conversely, grammatical wording can still imply an unintended contrast. Revise
for the intended reading, not visual symmetry.

Consult [English writing guidance](references/writing-guides.md) when resolving
a substantive usage choice. Apply relevant guidance rather than importing an
entire publisher's house style or requiring a lookup for every edit.

### Verify meaning

Read the result as English, then compare it with the source or factual context.
Check actors, reference, restrictive clauses, negation, conditions, and modality.
If an ambiguity changes the claim, ask or flag it rather than choosing the most
fluent interpretation. Return the requested text and explain only consequential
choices. Natural English must not turn a tentative claim into a guarantee.
