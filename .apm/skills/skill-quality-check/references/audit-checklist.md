# Skill Audit Checklist

Use this reference for a collection audit or a review informed by historical usage.
Keep a focused edit on its requested scope; an audit does not itself authorize repairs,
publication, or a new evaluation system. Use the existing validation workflow in
`SKILL.md` for individual skill checks and scenarios.

## Establish scope and evidence

- Name the requested question, included skills and resources, exclusions, and source
  revision. Identify canonical sources and generated deployments separately.
- Inventory the selected inputs before drawing collection-wide conclusions. Record
  which files or records were read, unavailable, excluded, or only partially inspected.
  Keep the denominator explicit when reporting coverage; do not silently extend a
  bounded sample to the whole collection.
- Distinguish a skill's availability or trigger promise from observed selection,
  returned instructions, and application. A current source can establish the current
  contract; it does not prove what an earlier executor received or followed.
- When historical material is available and authorized, record its relevant source
  version and evidence limits. Separate the original request, later changes,
  superseded instructions, retries, and delegated work. Avoid counting the same work
  repeatedly or using an executor's own completion claim as independent verification.
- Preserve missing evidence as unknown. Do not reconstruct unavailable instructions,
  tool results, intent, or behavior from a current file or an incomplete summary.

## Assess findings and proposed changes

- Check the skill against its trigger promise, applicability, mandatory conditions,
  exceptions, references, resources, and metadata using the existing quality workflow.
  Distinguish an absent rule from a rule that was available but not applied.
- Give each finding a location, observed problem, affected decision or behavior,
  supporting evidence, uncertainty, and smallest corrective action. Separate a
  structural design proposal from a demonstrated operational defect.
- Check the current canonical owner before proposing another rule or helper. Prefer
  an existing reference or a narrow correction when it already supplies the contract.
- Separate detection from repair scope. Surface a serious newly discovered problem,
  but obtain authorization when fixing it would expand the requested work. Keep an
  intentional baseline or documented exception distinct from an accidental omission.
- For a restructuring, map retained requirements and entry scenarios to their new
  destinations. Check normal, exceptional, missing-dependency, and out-of-scope paths,
  including stop conditions and verification. Shorter text alone does not establish
  preserved meaning or improved results.
- Use fresh scenario evaluators as required by `SKILL.md`. Inspect the resulting
  artifacts as well as check results: a mechanical pass does not establish factual
  correctness, useful output, or appropriate scope.
- Record quality, effort, required references, and available measurements separately.
  Mark unavailable metrics unavailable; do not estimate savings from file length,
  assume causation from co-occurrence, or optimize for zero findings at the expense
  of relevant detection.

## Report and resume safely

- Keep target-skill findings, input gaps, quality-check ambiguity, and unavailable
  measurements separate using the report categories in `SKILL.md`.
- State what was verified, inferred, proposed, skipped, or blocked. Include the
  source revision and remaining uncertainty needed to repeat the assessment.
- Prioritize by demonstrated impact, confidence, scope, and maintenance cost. Make
  dependencies between recommendations explicit; do not count a shared change twice.
- Keep any resumption note limited to scope, current evidence, decisions, open issues,
  and the next check. Follow the user's instructions about whether to retain notes;
  do not turn an optional checklist into automatic persistence.
- Apply `security-check` before publishing any finding, fixture, report, or derivative.
  Justify public changes independently from public sources or clearly labeled design
  reasoning. Private names, source excerpts, logs, statistics, timestamps, identifiers,
  and internal cases do not become public evidence through anonymization.
