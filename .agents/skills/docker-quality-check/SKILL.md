---
name: docker-quality-check
description: >-
  Quality-check Dockerfiles, Compose configurations, container startup scripts,
  image CI, and container documentation. Use when creating, editing, or reviewing
  container build, runtime, orchestration, or publication changes.
---

# Docker Quality Check

## When to Use

- Use for changes to Dockerfiles, Compose files, container entrypoints, image build
  automation, or container-facing documentation.
- Use before committing or publishing container changes.

## Goals

- Keep container builds reproducible, minimal, and suitable for the intended runtime.
- Validate both Dockerfile syntax and the changed build or Compose behavior.
- Make third-party images, downloaded tools, and CI actions traceable and reviewable.

## Workflow

1. Read the changed container files and repository guidance. Identify the build targets,
   runtime user, exposed services, mounted paths, environment variables, and expected
   startup behavior.
2. Run the repository's documented container checks. When no project-specific command
   exists, use `hadolint` for each changed Dockerfile and `docker compose config` for
   each changed Compose configuration.
3. Build the affected image or target with `docker build` or `docker compose build`.
   Pass only the build arguments and secrets required by the documented build contract;
   never place credentials in image layers, build logs, or committed configuration.
4. When startup, routing, health checks, or service wiring changes, start the smallest
   affected service set and exercise its documented health endpoint or smoke check.
   Stop the test services after verification.
5. Inspect image and runtime safety: use a non-root user where feasible, keep the final
   image free of build-only tooling and secrets, define a clear entrypoint, and avoid
   mutable base-image tags when an immutable digest is practical.
6. For newly introduced or updated external images, downloaded executables, or GitHub
   Actions, use `security-check` to assess provenance, version or digest pinning,
   release age, checksums, permissions, and runtime behavior. Pin GitHub Actions to
   full commit SHAs with accurate version comments.
7. Summarize commands run, build and smoke-test results, and every skipped check with a
   concrete reason.

## Default Checks

```shell
hadolint Dockerfile
docker build -t local-validation .
docker compose config
```

Replace these examples with the repository's documented file paths, build targets, tags,
and Compose files. Do not treat a successful syntax check as evidence that the image
builds or starts correctly.
