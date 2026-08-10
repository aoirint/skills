---
name: bws-workflow
description: >-
  Operate the Bitwarden Secrets Manager CLI (`bws`) safely for secret and
  project reads or writes, process-scoped secret injection, profiles, and
  machine-account access-token handling. Use when configuring or
  troubleshooting BWS, retrieving or changing Secrets Manager data, running
  commands with `bws run`, or bridging `BWS_ACCESS_TOKEN` from Windows
  Credential Manager, macOS Keychain, Linux Secret Service, or a language
  keyring.
---

# BWS Workflow

Use the Bitwarden Secrets Manager CLI without turning its machine-account
access token or retrieved values into new plaintext secrets.

## When to Use

- Use this Skill for `bws`, the Secrets Manager CLI. Do not apply `bw`
  Password Manager CLI commands or authentication rules to it.
- Pair with `security-check` when creating a credential bridge, changing token
  storage, adding a dependency, or scripting secret injection.
- Treat CI and service runners as a separate environment: use their native
  secret store, then apply the same process-scoped injection and cleanup rules.
- Install or update BWS only when requested. Verify the current official
  release, provenance, integrity, compatibility, and project supply-chain
  policy before executing a downloaded artifact.

## Goals

- Keep the access token out of command arguments, shell history, tracked files,
  logs, and long-lived shell state.
- Use the least-privileged machine account and a distinct credential identity
  for each trust boundary.
- Make reads, writes, injection, and verification explicit and reproducible
  without disclosing secret values.
- Fail closed when a credential store is missing, locked, ambiguous, or empty.

## Workflow

1. **Establish the execution context.**
   - Run `bws --version` and the relevant `bws <command> --help` before relying
     on remembered syntax.
   - Identify the server or profile, machine account, project, requested
     operation, output consumer, and whether the operation changes state.
   - Check only whether `BWS_ACCESS_TOKEN` is set; never print its value.
   - Resolve missing IDs or permissions with read-only commands before a write
     or delete. Require explicit authorization for destructive operations.

2. **Select the token source.**
   - Prefer an OS credential vault or an already reviewed language keyring.
   - Read [credential bridges](references/credential-bridges.md) before adding
     or changing a bridge, shell startup hook, WSL adapter, or migration.
   - Use a CI platform's masked secret facility for CI. Do not make a desktop
     keyring or interactive unlock prompt a hidden runner dependency.
   - Keep an existing valid token source unless the user asked to migrate or
     rotate it.

3. **Load the token without exposing it.**
   - Retrieve it as late as possible through a reader that emits only the token
     on stdout, diagnostics on stderr, and a nonzero exit status on failure.
   - Reject missing, locked, ambiguous, or empty results. Unset any inherited
     `BWS_ACCESS_TOKEN` on failure instead of falling back to a plaintext file.
   - Pass the token through `BWS_ACCESS_TOKEN`; do not use `--access-token`
     because command arguments can be exposed through history, diagnostics,
     or process inspection.
   - Prefer a one-command wrapper or subshell over exporting the token from
     every interactive shell. If persistent shell loading is explicitly
     required, keep the hook fail-closed and avoid secondary caches.

4. **Plan the BWS operation.**
   - Read [BWS operations](references/operations.md) for projects, secrets,
     profiles, output handling, state changes, and `bws run`.
   - Prefer stable IDs over names when ambiguity matters. Record requested
     identifiers and non-secret values before a state change.
   - Treat JSON, YAML, environment, table, and TSV output as sensitive whenever
     it can contain secret values. Do not use secret-bearing output as a log.

5. **Execute with the narrowest exposure.**
   - Disable shell tracing and verbose request logging around credential reads
     and BWS commands.
   - Avoid temporary files. If an external contract requires one, create it
     with restrictive permissions, keep it out of the repository, and remove
     it in a guaranteed cleanup path.
   - Prefer direct argument arrays over an extra shell. For secret injection,
     prefer `bws run --no-inherit-env` so the launched process does not inherit
     the machine-account token or unrelated parent variables.
   - Give the machine account only the projects and operations needed by the
     command.

6. **Verify and clean up.**
   - For reads, distinguish observed output from unavailable or suppressed
     values. Do not claim a value was correct merely because the command
     exited successfully.
   - For writes, read back the exact object and compare the requested fields in
     memory without printing secrets. For deletes, verify the exact ID is no
     longer returned.
   - Remove `BWS_ACCESS_TOKEN` and transient variables from the current process
     unless the user explicitly requested a longer-lived session.
   - Report the BWS version, non-secret context, redacted command shape,
     observed result, verification, and any unavailable evidence.

## Failure Handling

- Stop on vault lookup failure; do not silently consult `~/.bws_token`, a
  dotfile, clipboard, or command-line fallback.
- Treat authentication failure, authorization failure, wrong server/profile,
  and rate limiting as different diagnoses. Inspect the error and current help
  before retrying.
- Do not loop rapidly with a machine token. Short-lived repeated sessions can
  encounter rate limits.
- Revoke and replace a suspected exposed token. Bitwarden does not retain a
  retrievable copy of a generated access token.

## Completion Checklist

- The BWS version and exact operation were identified.
- The token came from an approved store and never appeared in arguments or
  output.
- The machine account and requested object scope were least-privileged.
- A state change has a requested-value record and post-change read-back.
- Transient token state was removed and no plaintext fallback was introduced.
