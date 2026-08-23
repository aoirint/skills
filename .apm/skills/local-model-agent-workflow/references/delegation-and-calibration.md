# Delegation and Calibration

## Delegation contract

Before invoking a local model, record:

- the bounded input and maximum size;
- the exact output schema or allowed labels;
- how absence and uncertainty are represented;
- the independent validation method;
- which failures are retried, escalated, or rejected;
- whether any sensitive input may enter the model process; and
- the final decision-maker that retains authority.

Prefer tasks where false output is mechanically detectable or cheap to sample.
Do not let a model expand its own permissions, choose destructive targets,
approve releases, suppress contradictory evidence, or declare its output safe.
Any later destructive operation is a separate workflow requiring fresh explicit
authorization and independently resolved exact targets.

## Validation layers

1. **Structural:** parse strict JSON and reject extra or missing fields.
2. **Domain:** enforce allowed labels, ranges, coordinate order, size limits, and
   null/uncertainty relationships.
3. **Evidence:** require text evidence to be an exact input span where
   applicable; independently inspect image-grounded evidence.
4. **Semantic:** compare against deterministic tools, tests, source material,
   or a reviewer appropriate to the risk.
5. **Operational:** retain input, prompt, profile, revision, and manifest hashes
   so a result can be reproduced and invalidated after change.

## Calibration

Create a representative set containing normal, ambiguous, missing, malformed,
and out-of-distribution cases. Keep a holdout that is not used while tuning
prompts or thresholds.

Use metrics that match the task:

| Task | Useful measures |
| --- | --- |
| Extraction | exact match, field precision/recall, null accuracy |
| Classification | per-label precision/recall, confusion matrix, abstention coverage |
| Summarization | factual error count, supported-claim rate, length compliance |
| OCR | character or word error rate, abstention quality |
| Localization | intersection over union, miss rate, false-positive rate |
| Ranking | Spearman correlation, pairwise agreement |

Define acceptance thresholds before looking at final holdout results. Report
invalid-output and abstention rates alongside accuracy so apparent quality is
not purchased by silently dropping difficult cases.

## Escalation and invalidation

Escalate when output is invalid, uncertainty is high, evidence conflicts,
inputs exceed calibrated bounds, or consequences are difficult to reverse.
Escalation to a stronger model remains advisory for high-impact decisions; an
authorized reviewer retains final authority.
Invalidate prior calibration after changing the model, revision, quantization,
runtime, prompt, preprocessing, generation settings, or effective hardware
execution path.
