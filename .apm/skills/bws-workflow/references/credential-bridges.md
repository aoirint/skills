# Credential Bridges for BWS

Use this reference when connecting `BWS_ACCESS_TOKEN` to an operating-system
credential vault or a language keyring.

## Contents

- Bridge contract
- Credential identity
- Platform selection
- Windows Credential Manager
- macOS Keychain
- Linux Secret Service
- Language keyrings
- Shell adapters
- WSL
- Migration and rotation
- CI and service runners
- Sources

## Bridge Contract

Build or select a bridge with three explicit operations: store, retrieve, and
delete. Require the retrieval operation to:

- select one credential by non-secret service and account attributes;
- write exactly the secret to stdout and diagnostics only to stderr;
- return nonzero for missing, locked, ambiguous, denied, or malformed data;
- avoid prompts in non-interactive mode unless the caller explicitly permits
  one;
- keep the token out of process arguments, shell history, logs, and files; and
- release or clear native buffers and short-lived variables as soon as the
  caller no longer needs them.

An environment variable is a transport, not a vault. Same-user processes,
debuggers, crash reporting, and child-process inheritance may expose it. Set
`BWS_ACCESS_TOKEN` immediately before BWS, minimize its lifetime, and prevent
unrelated child processes from inheriting it.

Do not add a plaintext fallback. A locked or unavailable vault is an
authentication failure, not permission to weaken storage.

## Credential Identity

Use stable, non-secret lookup attributes. A portable model is:

- service: `bitwarden-secrets-manager`;
- account: a context such as `work-production-windows` or
  `personal-development-wsl-ubuntu`; and
- secret: the machine-account access token.

On Windows, map these fields to a Generic Credential target such as
`Bitwarden Secrets Manager/<context>` and a non-secret username. Keep separate
entries when tokens, operating-system users, WSL distributions, organizations,
environments, or machine-account permissions differ. Never use the token or a
retrieved Bitwarden secret as a label or lookup attribute.

## Platform Selection

| Environment | Preferred store | Required preflight |
| --- | --- | --- |
| Windows desktop | Windows Credential Manager | Confirm a reviewed `CredRead`/`CredWrite` bridge is available for the current user. |
| macOS desktop | Keychain generic password | Confirm the selected keychain is unlocked and the service/account pair is unique. |
| Linux desktop | Secret Service implementation | Confirm a D-Bus session, default collection, and unlock path are available. |
| Headless Linux | Provisioned service keyring or workload secret store | Confirm non-interactive unlock and lifecycle ownership; otherwise stop. |
| Cross-platform application | Already pinned language keyring | Confirm the selected backend is an OS vault, not null or plaintext storage. |
| WSL | Windows bridge through interop, or a Linux keyring inside WSL | Choose one owner and keep Windows and distro identities distinct. |

Do not install a new keyring package or helper merely because it is convenient.
Review its provenance, immutable version, dependencies, storage backend,
runtime behavior, and release-age policy first.

## Windows Credential Manager

Use a Generic Credential owned by the current Windows user. Windows exposes
credentials for the current logon token through `CredReadW`; store or update
with `CredWriteW`, and release a returned credential buffer with `CredFree`.

Use a small reviewed helper or an already approved keyring backend. Require the
helper to:

1. accept only a non-secret target name as an argument;
2. write through `CredWriteW` from an interactive prompt, secure input, or a
   one-time migration source rather than a token argument;
3. retrieve `CRED_TYPE_GENERIC` with `CredReadW`;
4. validate a non-empty credential blob and emit only its decoded value;
5. zero temporary write buffers and call `CredFree` for read buffers; and
6. fail without changing `BWS_ACCESS_TOKEN` when lookup or decoding fails.

`cmdkey` can create and list credentials but does not provide a general secret
read interface. Do not parse Credential Manager files or place the token in a
`cmdkey /pass:` argument. Do not silently change machine-wide PowerShell
execution policy to run a bridge.

## macOS Keychain

Use a generic-password item keyed by service and account. Prefer Keychain
Access or a reviewed prompt/stdin helper for initial storage so the token does
not appear in a `security ... -w <token>` process argument.

For an existing item, a local adapter may retrieve only the secret with:

```bash
security find-generic-password \
  -s 'bitwarden-secrets-manager' \
  -a 'work-production-macos' \
  -w
```

Treat a keychain prompt, locked keychain, multiple matches, or access denial as
a failed lookup. Choose Keychain Services APIs directly when application-level
access-control requirements exceed the `security` CLI contract.

## Linux Secret Service

Use a Secret Service implementation such as GNOME Keyring through lookup
attributes rather than a stored D-Bus object path. With libsecret's
`secret-tool`, a typical lookup is:

```bash
secret-tool lookup \
  service bitwarden-secrets-manager \
  account work-production-linux
```

Store through an interactive prompt or stdin path that the current tool
documents as secret input; never append the token as an attribute. Confirm that
the selected collection is encrypted and unlocked. A headless environment
needs an owned D-Bus session and non-interactive unlock design; do not quietly
fall back to a plaintext keyring when those are absent.

## Language Keyrings

Use a language keyring only when it is already a reviewed, pinned dependency
or its adoption passes the project's supply-chain policy. The portable
interface is:

```text
set_password(service, account, token)
token = get_password(service, account)
delete_password(service, account)
```

Before use, inspect the active backend. Reject null, environment-only,
unencrypted file, and unexpected fallback backends. Treat `None`, an empty
value, backend initialization failure, or a locked store as a hard failure.

## Shell Adapters

Before writing an adapter, identify the exact shell runtime and executable,
including the PowerShell edition, Git Bash/MSYS2/Cygwin implementation, or WSL
distribution. Record its home and startup file, executable and helper path
syntax, path-conversion boundary, stdout newline convention, and whether it can
invoke the selected vault reader. Do not copy a command between runtimes merely
because both shells accept similar syntax.

Prefer a one-command wrapper. In POSIX shells, use a subshell so cleanup is
automatic:

```bash
with_bws_token() (
  set +x
  token="$(credential-get bitwarden-secrets-manager work-production)" || exit
  test -n "$token" || exit 1
  export BWS_ACCESS_TOKEN="$token"
  unset token
  command bws "$@"
)

with_bws_token secret list
```

Replace `credential-get` with the reviewed local reader. Do not implement it as
an alias containing a token.

In PowerShell, use a child scope and guaranteed cleanup:

```powershell
& {
    $token = & credential-get "Bitwarden Secrets Manager/work-production"
    if ([string]::IsNullOrWhiteSpace($token)) { throw "Credential lookup failed." }

    try {
        $env:BWS_ACCESS_TOKEN = $token
        bws secret list
    }
    finally {
        Remove-Item Env:\BWS_ACCESS_TOKEN -ErrorAction SilentlyContinue
        $token = $null
    }
}
```

Replace `credential-get` with the reviewed helper path. Keep errors free of
secret-bearing stdout and captured values.

For `bws run`, add `--no-inherit-env` unless the child intentionally needs
specific parent variables and their exposure has been reviewed:

```bash
with_bws_token run --no-inherit-env --project-id "$project_id" -- command arg
```

## WSL

Choose the vault owner explicitly:

- To use Windows Credential Manager, call a reviewed Windows reader through
  `pwsh.exe` or another fixed interop executable. Pass only the credential
  target, normalize the Windows newline, and reject missing interop or an empty
  result.
- To use a Linux keyring, keep its D-Bus session and unlock lifecycle entirely
  inside the distribution.

Do not assume Windows and WSL use the same token. Compare a migration source
and stored value in memory without printing either, and create separate target
names when they differ. Do not hard-code another user's Windows profile path.

## Migration and Rotation

1. Identify every current plaintext source and consumer without printing the
   value.
2. Store each distinct token under a distinct credential identity.
3. Read it back and compare in memory; emit only a boolean result.
4. Change consumers to the fail-closed bridge.
5. Start fresh shells or processes and verify BWS can authenticate.
6. Remove the exact plaintext sources only after successful read-back and
   consumer verification.
7. Revoke the old token when rotation, suspected exposure, or scope reduction
   requires it.

Deletion from a normal filesystem is not guaranteed secure erasure on SSDs,
snapshots, backups, or journaled filesystems. Treat a token that may have been
copied elsewhere according to the exposure and rotation policy.

## CI and Service Runners

Use the CI platform, orchestrator, or workload's native secret mechanism.
Scope the token to the job and machine account, mask logs, disable tracing, and
avoid exposing the token to untrusted pull requests. Do not require a desktop
vault, user session, GUI prompt, or personal keyring on an unattended runner.

## Sources

- [Bitwarden access tokens](https://bitwarden.com/help/access-tokens/)
- [Bitwarden Secrets Manager CLI](https://bitwarden.com/help/secrets-manager-cli/)
- [Microsoft `CredReadW`](https://learn.microsoft.com/windows/win32/api/wincred/nf-wincred-credreadw)
- [Microsoft password-handling guidance](https://learn.microsoft.com/windows/win32/secbp/handling-passwords)
- [Apple generic-password items](https://developer.apple.com/documentation/security/ksecclassgenericpassword)
- [Secret Service collections and items](https://specifications.freedesktop.org/secret-service/latest/ch03.html)
- [Python keyring interface](https://keyring.readthedocs.io/en/latest/)
