---
name: local-model-agent-workflow
description: >-
  Select, prepare, run, and calibrate locally executable language or
  vision-language models as bounded assistants for agent work. Use when
  offloading repeatable text or image tasks to a local model, preparing a
  revision- and hash-pinned model bundle, running inference without outbound
  network access, replacing the example model profile, or deciding when local
  inference must escalate to a stronger model or human review.
---

# Local Model Agent Workflow

Use a local model as an untrusted, bounded worker inside an agent workflow.
Optimize for useful verified work, not for maximizing how much work is local.

## When to Use

- Use for high-volume extraction, closed-label classification, bounded
  summarization, OCR, visual inspection, or candidate generation whose result
  can be checked cheaply.
- Do not delegate authorization, destructive decisions, security conclusions,
  release approval, or other judgments whose mistakes are difficult to detect
  or reverse.
- Pair with `security-check` when handling downloaded artifacts, untrusted
  inputs, container permissions, or supply-chain changes.
- Pair with `docker-quality-check` when changing the offline runner image or
  claiming accelerator compatibility.

## Workflow

1. **Bound the task and failure cost.**
   - Define the input limit, output schema, allowed labels or coordinates,
     uncertainty representation, and independent acceptance check.
   - Keep final authority with the parent agent. If verification would cost as
     much as doing the task directly, do not delegate it.
   - Read [delegation and calibration](references/delegation-and-calibration.md)
     before designing a new task or relying on model quality.

2. **Select a locally executable model.**
   - Measure the available memory, runtime, accelerator support, input size,
     modality, and required latency. Do not use parameter count alone as a
     fit test.
   - Start with the smallest candidate that passes a representative calibration
     set. Escalate individual uncertain or invalid cases before enlarging the
     default model.
   - Read [model selection](references/model-selection.md). The supplied Qwen
     profile is a dated, practical example, not a requirement or permanent
     recommendation.

3. **Prepare a pinned bundle while networking is allowed.**
   - Use a reviewed profile under `scripts/profiles/`, or create a new profile
     that pins the repository revision and SHA-256 of every required artifact.
   - Run `scripts/prepare_model_bundle.py` with the profile's independently
     checked SHA-256. Never replace a profile while retaining old calibration
     evidence.
   - Keep acquisition separate from inference. Do not place access tokens in
     profiles, arguments, logs, model bundles, or tracked files.

4. **Build and run the isolated worker.**
   - Follow [offline container operation](references/offline-container.md).
   - Build the locked runner while networking is allowed. At inference time use
     `--network none`, a read-only root filesystem, read-only model and input
     mounts, a non-root user, and an explicit writable output or temporary area.
   - Treat `uv --offline`, `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, and
     `local_files_only=True` as defense in depth. They are not the network
     isolation boundary.

5. **Use a prepared recipe and validate every result.**
   - Read [task recipes](references/task-recipes.md) for extraction,
     classification, summarization, image inspection, OCR, and localization.
   - Reject malformed JSON, extra fields, disallowed labels, invalid
     coordinates, unsupported evidence spans, or inconsistent uncertainty.
   - Record the profile, revision, manifest, input, and prompt hashes with the
     result. Treat valid syntax as necessary but not sufficient evidence.

6. **Calibrate and escalate.**
   - Evaluate a representative labeled set before enabling automated use.
     Measure task-specific accuracy and uncertainty coverage, not anecdotes.
   - Escalate invalid output, low confidence, contradictory evidence, or
     out-of-distribution input to a stronger model or human review. A stronger
     model remains advisory; high-impact cases require an authorized reviewer.
   - Recalibrate after any model, revision, quantization, runtime, prompt,
     preprocessing, generation setting, or hardware execution-path change.

## Core Invariants

- Local does not mean trusted, private by construction, or accurate.
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

- Task boundaries, schema, uncertainty, verifier, and escalation path are named.
- Model fit was measured on the intended execution path.
- Revision and artifact hashes are pinned in a reviewed profile.
- The prepared bundle passed complete file-set and hash verification.
- Runtime networking was disabled independently of uv and model-library flags.
- Representative calibration passed, and recalibration triggers are recorded.
- No output received authority beyond its independently verified evidence.
