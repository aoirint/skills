---
name: local-llm-workflow
description: >-
  Guides decisions and reproducible reference implementations for locally
  executable LLMs, including multimodal variants. Use when evaluating or
  developing a local-LLM dependency, enforcing an offline or data-local
  boundary, calibrating a bounded task, or migrating models; not for routine
  agent delegation or analyses better handled by deterministic or statistical
  methods.
---

# Local LLM Workflow

Treat a local LLM as a bounded software dependency whose value must be measured,
not as a default subordinate agent. This Skill supplies decision criteria,
evaluation practice, and an optional reproducible runner for learning and
prototyping. It does not prescribe a production architecture.

## When to Use

- Evaluate whether an application should depend on a locally executable LLM.
- Prototype or test a text, vision-language, or other multimodal LLM task on
  local hardware.
- Establish an offline or data-local execution boundary and reproducible model
  acquisition process.
- Calibrate a bounded local-LLM task or evaluate a model, runtime, quantization,
  prompt, preprocessing, or hardware change.
- Do not invoke this Skill merely to offload ordinary agent work. Use the
  agent's normal model unless a concrete requirement makes that unsuitable.
- Do not use an LLM for a problem adequately handled by parsing, search, rules,
  statistics, conventional machine learning, or computer vision.

## Goals

- Reach an evidence-backed adopt, reject, or investigate decision.
- Minimize total workflow cost, including handoff, startup, validation, retries,
  memory, storage, network transfer, local compute, and reintegration.
- Keep inputs, outputs, authority, failure handling, and acceptance tests
  explicit and bounded.
- Make only claims supported by the execution path and evaluation actually run.
- Preserve enough provenance to reproduce results and invalidate them after a
  relevant change.

## Workflow

1. **Classify the request before choosing a model.**
   - For ordinary agent work, keep the task in the normal agent context.
   - For analysis, establish a direct, deterministic, statistical, ML, or CV
     baseline first. Continue only if it is inadequate on representative input
     or local LLM execution is itself a requirement.
   - For product work, define the local-execution requirement and the inference
     component boundary. Treat this Skill's code and profiles as reference
     baselines, not as a product runtime.

2. **Write the decision and evaluation contract.**
   - Record the use case, rejected simpler alternatives, input and output
     bounds, acceptance metrics and thresholds, uncertainty representation,
     independent verifier, failure handling, and final decision-maker. Classify
     retryable transient failures and fix the maximum attempts, backoff, and
     resource budget before execution; schema, evidence, and semantic failures
     must abstain or escalate instead of being resampled until they pass.
   - Include privacy, licensing, hardware, latency, throughput, memory, storage,
     deployment, and operational constraints that affect adoption.
   - Define one durable model store and download cache outside per-task,
     per-worktree, and temporary directories. Inventory existing bundles and
     estimate peak acquisition space before downloading another model.
   - Read [adoption and calibration](references/adoption-and-calibration.md) for
     the delegation gate, validation layers, representative sets, and metrics.

3. **Select a candidate from evidence.**
   - Read [model selection](references/model-selection.md) when comparing model,
     quantization, runtime, or hardware options.
   - Benchmark the complete intended execution path. Parameter count, model-card
     claims, imports, device discovery, and successful startup are not evidence
     of usable quality, latency, accelerator execution, or memory fit.
   - Prefer the least costly candidate that clears the predeclared acceptance
     thresholds. Record an explicit reject or investigate result when none does.

4. **Choose only the implementation guidance the request needs.**
   - For common bounded task shapes, read [task recipes](references/task-recipes.md).
     The supplied Python runner is an inspectable reference implementation of
     strict schemas, provenance, batching, and abstention; adapt or replace it
     for the actual application.
   - For a pinned bundle or enforced offline run, read
     [offline container operation](references/offline-container.md). Network
     isolation must be enforced outside uv and model-library offline flags.
   - For model replacement, follow the migration procedure in
     [model selection](references/model-selection.md) and use
     `assets/migration-record.json` as a minimum evidence record.
   - For a complex product, design and measure its API, concurrency, persistence,
     observability, packaging, distribution, threat model, and user experience
     independently. These concerns are outside the reference runner.

5. **Validate the result and calibrate the claim.**
   - Reject malformed output, unsupported evidence, invalid coordinates or
     labels, inconsistent uncertainty, and inputs outside calibrated bounds.
   - Evaluate a representative calibration set and an untouched holdout. Report
     invalid-output and abstention rates alongside task-specific quality.
   - Escalate uncertain or high-impact cases to an appropriate stronger method
     or authorized reviewer. Do not let model output grant permissions, approve
     releases, choose destructive targets, or become its own verifier.
   - Recalibrate after changes to the model, revision, quantization, runtime,
     adapter, prompt, preprocessing, generation settings, or effective hardware
     path.

6. **Conclude with evidence and limits.**
   - State the decision: adopt, reject, or investigate.
   - Record the tested configuration, measurements, provenance, known failure
     modes, escalation path, and unverified claims.
   - Do not describe a reference example, dependency check, container build, or
     synthetic test as production readiness or real-model validation.

## Completion Checklist

- The reason to consider local execution and the simpler baseline are recorded.
- The task boundary, verifier, metrics, and thresholds were fixed before the
  final holdout evaluation.
- The model and runtime fit were measured on the intended execution path.
- Artifact, configuration, input, prompt, and result provenance is sufficient
  for the claimed reproducibility level.
- Repeated runs reuse a verified bundle and shared cache; temporary, retained,
  and removable storage have explicit owners and lifecycles.
- Offline, privacy, quality, accelerator, and product-readiness claims do not
  exceed the evidence obtained.
- The final decision and its remaining unknowns are explicit.
