---
name: japanese-prose-quality-check
description: >-
  Draft or revise Japanese prose for natural phrasing, clear grammatical
  relationships, appropriate register, and consistent notation. Use for Japanese
  text or Japanese translations, including documentation, PRs, comments, and
  messages; not for changing technical facts or translating code identifiers.
---

# Japanese Prose Quality Check

## When to Use

Use for Japanese expression within an established audience, purpose, and scope.
Use `prose-quality-check` for language-independent structure, durable context,
references, and status wording when available; this Skill owns Japanese-specific
phrasing. Preserve the requested voice rather than making every text formal.

## Goals

- Make grammatical relationships clear without spelling out every omitted subject.
- Replace translation-shaped phrasing without changing the claim or its force.
- Keep notation consistent with the document's audience and conventions.

## Workflow

### Establish the register

Read the surrounding prose and any glossary or style guide. Choose 常体 or 敬体
for the audience and keep it consistent within the relevant text. Headings,
labels, quotations, and separate speakers can have their own forms. Do not turn
ordinary developer documentation into bureaucratic language, or rewrite a
speaker's distinctive voice merely for uniformity.

### Clarify relationships

- Check that the topic or subject fits the predicate, including after long
  qualifications. Repair a mismatch by restoring the intended relationship,
  not by inventing an actor. Keep a naturally omitted subject when it is clear;
  name it when a change of actor or an important responsibility would be ambiguous.
- Check particles and the attachment of modifiers. Put a modifier near what it
  qualifies, or reorder/split the sentence when that resolves ambiguity. Do not
  mechanically swap は and が, or use commas alone to hide a disputed reading.
- Make the scope of negation, conditions, quantities, and parallel expressions clear.
  Preserve distinctions such as できる, してよい, する必要がある, and しなければならない.
  When multiple readings would change the facts, ask or identify the ambiguity
  instead of choosing the smoothest interpretation.
- Use punctuation to reveal the intended groups. Reduce chains of の, long
  prenominal clauses, and repeated について／において when they obscure relationships;
  retain them when they express a useful distinction.

### Refine phrasing

Prefer familiar verbs and concrete expressions over unnecessary nominalization,
loan translations, or inflated politeness. For example, 変更を行う may become
変更する when no contrast is lost. Do not treat expressions such as こと,
もの, 対応, or させていただく as forbidden words: judge their role in context.
Keep useful technical terminology rather than replacing it with vague everyday
language. Do not translate literal UI labels, commands, identifiers, or citations
without authorization.

For a translation, reconstruct the Japanese sentence from the intended relation
rather than preserving source-language word order. Check it against the source
for actors, exceptions, certainty, and obligations. Fluent Japanese must not
strengthen a tentative claim, create causality, or erase a restriction.

### Align notation

Follow the document's glossary and domain conventions for spelling, kana,
kanji, okurigana, numbers, units, punctuation, and spacing around Latin text.
Use one form for the same concept unless the difference is meaningful. Keep
product names, quoted text, paths, and code exact. Do not apply a mechanical
漢字-to-ひらがな conversion or a universal character-width rule.

Consult [Japanese writing guidance](references/writing-guides.md) when choosing
between conventions or explaining a substantive revision. Adopt only the parts
that fit the text; do not require a guide lookup for every ordinary edit.

### Verify the result

Read the Japanese without the source beside it, then compare meaning with the
source or factual context. Check omitted actors, modifier scope, negation,
modality, and notation. Avoid punctuation or line breaks that merely make a
long sentence look shorter. Return the requested text; explain only consequential
ambiguities or changes, not a catalog of every stylistic preference.
