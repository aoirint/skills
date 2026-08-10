# BWS Operations

Use this reference after selecting a safe `BWS_ACCESS_TOKEN` source. Treat the
installed CLI's `--help` output as the command contract and the official
Bitwarden documentation as the maintained product source.

## Contents

- Preflight
- Projects and secrets
- State changes
- Secret injection with `bws run`
- Profiles and self-hosted servers
- Output handling
- Verification and evidence
- Troubleshooting
- Sources

## Preflight

Run these without printing the token:

```console
bws --version
bws --help
bws secret --help
bws project --help
bws run --help
```

Record the version and command shape. Confirm the intended Bitwarden server,
profile, machine account, project, and operation. Access tokens inherit the
machine account's permissions; choose or create the least-privileged account
before relying on command-side filtering.

## Projects and Secrets

Use the relevant help before composing a command:

```console
bws project list
bws project get PROJECT_ID
bws secret list
bws secret get SECRET_ID
```

Prefer IDs when names can collide. Treat list and get output as sensitive: a
response may contain secret values, descriptions, project details, or other
operational metadata. Parse only the required field in memory and do not paste
raw responses into logs, issues, chat, or test snapshots.

Use `--output` only with a format supported by the installed version. JSON is
usually the safest structured contract, but it is not safe to log merely
because it is structured.

## State Changes

Before create, edit, or delete:

1. Run `bws <resource> <operation> --help` for the installed version.
2. Resolve the exact project or secret ID with a read-only command.
3. Record the requested non-secret fields and a redacted indicator for every
   requested secret value.
4. Confirm the machine account has only the required write permission.
5. Execute once with tracing and verbose logging disabled.
6. Read back the exact ID and compare requested fields in memory.

For deletion, require explicit user authorization for the exact ID and verify
that the object is no longer returned. Do not interpret an unavailable read
after a permission change as proof of deletion.

## Secret Injection with `bws run`

Use `bws run` when a child process needs a project's secrets as environment
variables. Prefer:

```console
bws run --no-inherit-env --project-id PROJECT_ID -- executable arg
```

- Use `--no-inherit-env` to keep the access token and unrelated parent
  variables out of the child environment.
- Use a direct executable and argument vector. Add `--shell` only when shell
  syntax is required and the quoting and injection surface has been reviewed.
- Inspect secret key names before injection. Reject collisions, invalid
  environment-variable names, and unintended overwrites.
- Use `--uuids-as-keynames` when stable UUID-derived variable names are safer
  than mutable or colliding secret keys.
- Scope `--project-id` rather than injecting every project the machine account
  can access.

The child can expose injected values through its own logs, crash reports,
subprocesses, or diagnostics. Review that boundary separately from BWS.

## Profiles and Self-Hosted Servers

Use `bws config --help` and the installed command's profile options. Keep
server URL, profile, and config path separate from the access token:

- use `--profile` or `BWS_PROFILE` for a named non-secret context;
- use `--server-url` or `BWS_SERVER_URL` only for the intended Bitwarden
  deployment; and
- use `--config-file` or `BWS_CONFIG_FILE` when a non-default config location
  is required.

Inspect a config file before sharing it even when it is not intended to contain
the access token. Do not add a token field or a shell command that prints one.

## Output Handling

- Prefer no output for operations whose result does not need to be consumed.
- Capture structured output into a variable or pipe whose downstream commands
  are trusted and tracing is disabled.
- Quote extracted values and preserve bytes exactly; do not trim arbitrary
  whitespace from stored application secrets.
- Avoid command substitutions that place secret values into a long-lived shell
  variable when `bws run` can inject them directly.
- Never use example tokens that resemble live credentials. Use names such as
  `PROJECT_ID`, `SECRET_ID`, and `TOKEN_FROM_VAULT` in documentation.

## Verification and Evidence

Separate these states in the final report:

- **Observed:** command version, exit status, returned non-secret metadata, and
  read-back comparisons actually performed.
- **Changed:** exact IDs and requested fields sent to BWS, with values redacted.
- **Unavailable:** secret values intentionally suppressed, permissions not
  observable, or remote state not readable after the operation.
- **Planned:** cleanup, rotation, or revocation that was not authorized or not
  performed.

A successful exit status proves only that the command reported success. It
does not prove the returned value matched an external expectation unless that
comparison was performed.

## Troubleshooting

| Symptom | Check | Safe response |
| --- | --- | --- |
| Token missing or empty | Credential bridge exit status and selected identity | Stop; do not read a dotfile fallback. |
| Authentication failure | Token identity, revocation, expiration, server, and profile | Correct the context or rotate; do not print the token. |
| Authorization failure | Machine-account project access and operation permission | Reduce or correct permissions; do not switch to a broader token casually. |
| Repeated-session rate limit | Invocation count and wrapper design | Reuse a bounded session where supported or back off; do not loop rapidly. |
| Child lacks expected secret | Project scope, key validity, collision, and `--no-inherit-env` effects | Inspect names and command help without logging values. |
| Child received unrelated variables | Missing `--no-inherit-env` or shell wrapper inheritance | Narrow the child environment and rerun only when safe. |

## Sources

- [Bitwarden Secrets Manager CLI](https://bitwarden.com/help/secrets-manager-cli/)
- [Bitwarden access tokens](https://bitwarden.com/help/access-tokens/)
- [Bitwarden Secrets Manager SDK and BWS source](https://github.com/bitwarden/sdk-sm)
