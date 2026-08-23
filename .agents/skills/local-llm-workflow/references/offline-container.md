# Offline Container Operation

Preparation and inference are separate trust phases. Network access is expected
during dependency and model acquisition; it is denied during task execution.

## Contents

- [Plan storage before acquisition](#plan-storage-before-acquisition)
- [Prepare the model bundle](#prepare-the-model-bundle)
- [Build the locked runner](#build-the-locked-runner)
- [Run with networking disabled](#run-with-networking-disabled)
- [Accelerator use](#accelerator-use)
- [Replace the model at runtime](#replace-the-model-at-runtime)

## Plan storage before acquisition

Use one durable model store and one shared download cache for all evaluations on
the host. Do not place either under a task directory, Git worktree, or disposable
container layer. Key bundle directories by the reviewed profile ID so repeated
runs resolve the same destination.

Before downloading, inventory the store and cache, check free space, and account
for peak acquisition space. The reference preparer retains the shared Hub cache
and materializes one independently verified bundle, so the same model data may
temporarily or permanently occupy both locations. Atomic staging also needs
space for the bundle until its final rename.

The preparer returns `status: reused` when the requested destination already
contains the exact verified profile and artifacts. It rejects altered or extra
files instead of creating another destination. Pass the same `--cache-dir` and
`--destination` on every run; do not generate either path from a run ID.

Track which profiles, evaluations, applications, and rollback records still
reference each cache or bundle. Cleanup is a separate destructive operation:
resolve exact unreferenced paths, review the inventory, and obtain authorization
before deletion. Never let an evaluation agent delete a broad cache or model
store automatically.

The commands below assume the skill directory is the current directory. The
included example profile has SHA-256:

```text
f54a51f5f748451e2679d46973d689b4597e8d619547d05b71030cb39c5d7e40
```

Recompute that value from the checked-out profile with a trusted tool and
compare it with the value recorded by review or a separate trusted source. Do
not compute a value from an unreviewed profile and immediately treat that same
value as approval. A changed profile requires review and new calibration.

## Prepare the model bundle

This phase needs network access when artifacts are absent. It writes a new
destination atomically or returns `status: reused` for an existing bundle only
after the profile, manifest, complete file set, and artifact hashes match. It
rejects a mismatched destination without downloading or overwriting it.

```shell
uv run --no-config --locked --script scripts/prepare_model_bundle.py -- \
  --profile scripts/profiles/qwen35-4b.json \
  --profile-sha256 f54a51f5f748451e2679d46973d689b4597e8d619547d05b71030cb39c5d7e40 \
  --cache-dir /srv/local-model-cache \
  --destination /srv/local-models/qwen35-4b
```

The profile pins an immutable repository revision and the SHA-256 of every
retained artifact. The output manifest binds the bundle to that profile.
Authentication is intentionally absent from the example. If a reviewed model
requires credentials, inject them through an approved process-scoped mechanism
and do not record them in arguments or the bundle.

## Build the locked runner

The image build resolves only the adjacent PEP 723 lock and installs it into a
virtual environment. The uv base image is pinned by multi-platform digest.

```shell
docker build \
  --file assets/offline-runner/Dockerfile \
  --tag local-llm-reference-runner:2026-08-23 \
  .
```

After building, record the immutable local image ID, not only the mutable tag:

```shell
docker image inspect local-llm-reference-runner:2026-08-23 \
  --format '{{.Id}}'
```

For a published image, record the registry digest as well.

Review the lockfile and base-image digest before rebuilding. A successful build
and import check establish dependency availability only; they do not prove model
inference, accelerator use, or runtime isolation.

## Run with networking disabled

```shell
docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid,size=1g \
  --mount type=bind,src=/srv/local-models/qwen35-4b,dst=/models,readonly \
  --mount type=bind,src=/absolute/input,dst=/input,readonly \
  local-llm-reference-runner:2026-08-23 \
  --profile /opt/skill/scripts/profiles/qwen35-4b.json \
  --profile-sha256 f54a51f5f748451e2679d46973d689b4597e8d619547d05b71030cb39c5d7e40 \
  --model-directory /models \
  classify --input /input/source.txt --labels relevant irrelevant uncertain
```

Resolve the host paths before running the command. Keep model and input mounts
read-only. Add a narrowly scoped writable output mount only if shell redirection
outside the container is unsuitable.

The runner also sets library offline flags and uses `local_files_only=True`.
Those controls reduce accidental downloads, but `--network none` is the actual
network boundary. `uv --offline` would only constrain uv and is therefore not
used as evidence that inference is offline.

## Accelerator use

Add `--gpus all` only on a host with a reviewed container runtime and compatible
driver stack. Do not claim GPU compatibility from image construction, imports,
device discovery, or a requested flag. Evidence requires actual model inference
on the intended device, followed by output validation and representative
calibration. If that execution cannot be performed, report accelerator status as
unavailable rather than passing it by inference.

## Replace the model at runtime

To use another reviewed model profile, rebuild the runner if its model class or
Python dependencies differ, mount its verified bundle, and pass its independently
checked profile SHA-256. Always run compatibility checks and fresh calibration.
The profile override changes data and model selection; it does not grant network,
filesystem, or decision authority.

For a profile that is not baked into the image, add a read-only mount such as:

```shell
--mount type=bind,src=/absolute/new-profile.json,dst=/run/model-profile.json,readonly
```

and pass `--profile /run/model-profile.json`. If adapter code or dependencies
change, a profile mount is insufficient: assign or update the adapter contract,
review the adapter and lock, then build a new pinned runner image. Retain the old
image ID or digest, lock, adapter ID and implementation revision, profile,
bundle manifest, and calibration record for rollback.
