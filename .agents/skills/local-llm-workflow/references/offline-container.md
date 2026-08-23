# Offline Container Operation

Preparation and inference are separate trust phases. Network access is expected
during dependency and model acquisition; it is denied during task execution.

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

This phase needs network access and writes a new destination atomically. The
script refuses to overwrite an existing bundle.

```shell
uv run --no-config --locked --script scripts/prepare_model_bundle.py -- \
  --profile scripts/profiles/qwen35-4b.json \
  --profile-sha256 f54a51f5f748451e2679d46973d689b4597e8d619547d05b71030cb39c5d7e40 \
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
  --tag local-model-agent-runner:2026-08-23 \
  .
```

After building, record the immutable local image ID, not only the mutable tag:

```shell
docker image inspect local-model-agent-runner:2026-08-23 \
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
  local-model-agent-runner:2026-08-23 \
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
