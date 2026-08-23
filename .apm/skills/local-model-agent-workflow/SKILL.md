---
name: local-model-agent-workflow
description: >-
  Select, prepare, run, and calibrate locally executable language or
  vision-language models as exceptional, bounded components for agent work.
  Use when online model use is unsuitable for an established requirement,
  deterministic or classical methods have failed on a bounded analysis, a
  local-model application is being developed or tested, a pinned offline model
  bundle is required, or an existing local inference workflow must be calibrated
  or migrated. Do not use for routine delegation that the agent's normal model
  or a simpler tool can perform directly.
---

# Local Model Agent Workflow

Default to the agent's normal model for ordinary agent work and to deterministic
or classical tools for problems they solve well. Use a local model only as an
untrusted, purpose-built component with a measured advantage for the specific
task. Treat it like selecting a computer-vision or statistical library, not like
adding a general-purpose subordinate agent.

## When to Use

- Use when a concrete constraint makes online model execution unsuitable, such
  as a required offline boundary or a deployment target whose application must
  run a local model.
- Use as a measured fallback for bounded extraction, classification, OCR,
  visual inspection, or candidate generation only after suitable deterministic,
  rule-based, statistical, or conventional CV methods are inadequate.
- Use when developing, testing, calibrating, or migrating an application whose
  product requirement explicitly includes local LLM or VLM inference.
- Do not introduce local inference merely to offload routine agent work. Keep
  the work in the normal agent context unless the delegation gate below passes.
- Do not delegate authorization, destructive decisions, security conclusions,
  release approval, or other judgments whose mistakes are difficult to detect
  or reverse.
- Pair with `security-check` when handling downloaded artifacts, untrusted
  inputs, container permissions, or supply-chain changes.
- Pair with `docker-quality-check` when changing the offline runner image or
  claiming accelerator compatibility.

## Workflow

1. **Justify local inference.**
   - First ask whether the agent's normal model should perform the task directly.
     For a narrow computable problem, try an established parser, rule, search,
     CV routine, statistical method, or other deterministic tool before an LLM.
   - Name the requirement that makes local inference preferable and compare
     end-to-end quality, latency, memory, storage, network transfer, local
     compute, operational complexity, and verification cost against the simpler
     baseline.
   - Reject delegation when its model handoff fragments relevant context,
     duplicates reasoning, or introduces an uncalibrated inference boundary
     without a compensating task-specific benefit.

2. **Bound the task and failure cost.**
   - Define the input limit, output schema, allowed labels or coordinates,
     uncertainty representation, and independent acceptance check.
   - Keep final authority with the parent agent. If verification would cost as
     much as doing the task directly, do not delegate it.
   - Read [delegation and calibration](references/delegation-and-calibration.md)
     before designing a new task or relying on model quality.

3. **Select a locally executable model.**
   - Measure the available memory, runtime, accelerator support, input size,
     modality, and required latency. Do not use parameter count alone as a
     fit test.
   - Start with the smallest candidate that passes a representative calibration
     set. Escalate individual uncertain or invalid cases before enlarging the
     default model.
   - Read [model selection](references/model-selection.md). The supplied Qwen
     profile is a dated, practical example, not a requirement or permanent
     recommendation.

4. **Prepare a pinned bundle while networking is allowed.**
   - Use a reviewed profile under `scripts/profiles/`, or create a new profile
     that pins the repository revision and SHA-256 of every required artifact.
   - Run `scripts/prepare_model_bundle.py` with the profile's independently
     checked SHA-256. Never replace a profile while retaining old calibration
     evidence.
   - Keep acquisition separate from inference. Do not place access tokens in
     profiles, arguments, logs, model bundles, or tracked files.

5. **Build and run the isolated worker.**
   - Follow [offline container operation](references/offline-container.md).
   - Build the locked runner while networking is allowed. At inference time use
     `--network none`, a read-only root filesystem, read-only model and input
     mounts, a non-root user, and an explicit writable output or temporary area.
   - Treat `uv --offline`, `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, and
     `local_files_only=True` as defense in depth. They are not the network
     isolation boundary.

6. **Use a prepared recipe and validate every result.**
   - Read [task recipes](references/task-recipes.md) for extraction,
     classification, summarization, image inspection, OCR, and localization.
   - Reject malformed JSON, extra fields, disallowed labels, invalid
     coordinates, unsupported evidence spans, or inconsistent uncertainty.
   - Record the profile, revision, manifest, input, and prompt hashes with the
     result. Treat valid syntax as necessary but not sufficient evidence.

7. **Calibrate and escalate.**
   - Evaluate a representative labeled set before enabling automated use.
     Measure task-specific accuracy and uncertainty coverage, not anecdotes.
   - Escalate invalid output, low confidence, contradictory evidence, or
     out-of-distribution input to a stronger model or human review. A stronger
     model remains advisory; high-impact cases require an authorized reviewer.
   - Recalibrate after any model, revision, quantization, runtime, prompt,
     preprocessing, generation setting, or hardware execution-path change.

## Core Invariants

- Local does not mean trusted, private by construction, or accurate.
- Local inference is an exceptional dependency, not the default agent execution
  path. Repeated ad hoc delegation is a harness regression unless measurements
  show a task-specific net benefit over direct agent work and simpler tools.
- Delegation must preserve enough source context and provenance for the parent
  agent to verify and integrate the result; a local model does not become an
  independent memory or authority boundary.
- A model profile is accepted only when its expected SHA-256 is supplied and
  all bundle artifacts match the profile.
- Offline inference is evidenced by an enforced network boundary, not by a
  package-manager flag or successful imports.
- Import checks do not prove inference, accelerator execution, output quality,
  or isolation. Make only the claims supported by the executed checks.
- Model replacement preserves the workflow only after compatibility checks and
  fresh calibration; it never inherits the previous model's acceptance record.
- Any destructive follow-up is outside this advisory workflow. It requires
  separate authorization and an independently resolved, exact target list.

## Completion Checklist

- The local-inference requirement and rejected simpler alternatives are named.
- End-to-end benefit was measured against direct agent work or the appropriate
  deterministic, statistical, or conventional CV baseline.
- Task boundaries, schema, uncertainty, verifier, and escalation path are named.
- Model fit was measured on the intended execution path.
- Revision and artifact hashes are pinned in a reviewed profile.
- The prepared bundle passed complete file-set and hash verification.
- Runtime networking was disabled independently of uv and model-library flags.
- Representative calibration passed, and recalibration triggers are recorded.
- No output received authority beyond its independently verified evidence.
