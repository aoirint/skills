# Adoption and Calibration

## Delegation gate

Routine agent work stays with the agent's normal model. Local inference is not a
default optimization and must not be introduced opportunistically merely because
a model is available. Before delegating, test these alternatives in order:

1. direct completion by the normal agent model, preserving the current context;
2. deterministic parsing, search, validation, or transformation;
3. a well-established statistical, machine-learning, or conventional CV method;
4. a local LLM or VLM only when an earlier option is unsuitable or has failed on
   representative inputs, or when local inference is itself a product requirement.

Document the specific exception: an established reason online inference is
unsuitable, evidence that simpler methods are inadequate, or an application
requirement to develop and exercise local inference.

Evaluate the whole harness, not just the model call. Frequent local delegation
can reduce accuracy and speed, consume memory, storage, network bandwidth, and
local compute, split context and cause forgetting, and add unstable differences
in prompting or inference behavior. Include prompt construction, serialization,
model loading, handoff, validation, retries, and reintegration in the comparison.
If the net benefit is not demonstrated, do the task directly or use the simpler
tool.

## Delegation contract

Before invoking a local model, record:

- the bounded input and maximum size;
- the exact output schema or allowed labels;
- how absence and uncertainty are represented;
- the independent validation method;
- which transient failures are retryable, their maximum attempts, backoff, and
  resource budget, and which failures are escalated or rejected without retry;
- whether any sensitive input may enter the model process; and
- the final decision-maker that retains authority.

Prefer tasks where false output is mechanically detectable or cheap to sample.
Keep inputs self-contained and return enough evidence for the parent agent to
reconstruct why the result applies. Do not use chained local-model calls as a
substitute for preserving the agent's working context.
Do not regenerate invalid schema, unsupported evidence, or a semantic failure
until an answer happens to pass. Record the failed attempt, then abstain or use
the predeclared escalation path.
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
