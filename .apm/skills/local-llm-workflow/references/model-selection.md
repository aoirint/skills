# Model Selection

## Selection order

1. Establish a direct-agent or deterministic/classical baseline and record why
   it is unsuitable or inadequate. If it meets the requirement, stop without
   adding local inference.
2. Fix the task, modality, maximum input, output contract, and acceptance test.
3. Inventory RAM, accelerator memory, supported numeric formats and kernels,
   storage, startup time, throughput, and acceptable latency.
4. Shortlist models whose licenses and runtime support fit the environment.
5. Measure the real model, quantization, runtime, and hardware path on a
   representative calibration set.
6. Choose the smallest candidate that clears the quality and reliability gates
   and improves the end-to-end workflow enough to justify its added dependency.

Parameter count is only an initial sizing clue. Context length, image tokens,
KV cache, precision, quantization, runtime overhead, and fallback to CPU can
change feasibility materially. Record peak memory and latency from actual
execution instead of inferring them from a model card.

Measure total workflow cost, including model acquisition, startup, context
handoff, validation, retries, and result reintegration. A faster isolated model
call is not an improvement if the overall agent becomes slower, less accurate,
less reproducible, or more resource-intensive.

## Practical tiers

- Small models are useful for routing, extraction, closed-label classification,
  short summaries, OCR, and other narrow tasks with strict validators.
- Mid-sized locally executable models are useful when prompts or inputs require
  more nuance and the hardware still permits interactive iteration.
- Larger local models may improve difficult cases but increase startup,
  memory, calibration, and operational cost. Escalation per case is often more
  efficient than making the largest fitting model the default.

## Model profiles

The included `qwen35-4b.json` profile is a dated example of one contemporary,
general-purpose multimodal model that is practical on some local systems. It is
not mandatory, universally optimal, or automatically current.

To replace it:

1. Check current first-party model and runtime documentation.
2. Select an immutable repository revision.
3. Download into a disposable staging location and enumerate every runtime file.
4. Independently compute SHA-256 for every retained artifact.
5. Create a new profile ID; do not silently edit an established profile.
6. Review model-class compatibility and the no-remote-code requirement.
7. Prepare and verify a bundle through the supplied script.
8. Exercise real inference on the intended CPU or accelerator path.
9. Run fresh calibration and retain the old profile until migration evidence is
   complete.

An execution-time profile override changes the model, but it does not waive any
pinning, compatibility, isolation, or recalibration requirement.

## Runtime adapter contract

A profile can select only an adapter contract and model class already
allowlisted by the runner. The adapter ID binds processor inputs, chat-template
use, device placement, generation, and decoding behavior to reviewed runner
code. When a replacement needs a different class or runtime, review these
together:

- the explicit class allowlist and continued `trust_remote_code=False` policy;
- processor and chat-template inputs for both text and image cases;
- device placement, numeric type, quantization, and generated-token slicing;
- dependency declarations, adjacent lockfile, and runner image;
- a real inference test on every execution path that will be claimed; and
- task calibration on a fresh representative set and holdout.

Do not treat nominal Transformers compatibility as proof that message formats,
image preprocessing, generation output, or device placement are compatible.

For rollback, retain the old profile and its SHA, bundle manifest SHA, immutable
runner image ID or registry digest, dependency lock, adapter ID and
implementation revision, hardware path, generation settings, and calibration
record until migration is accepted.
Use `assets/migration-record.json` as the minimum record shape.
