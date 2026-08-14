# Credential storage

## Separate the credential roles

Kopia's built-in credential persistence stores the repository password in the
operating-system credential store: Keychain on macOS, Credential Manager on
Windows, and a keyring on Linux. This is a Kopia-created local reconnect
credential. It is not a general interface for reading an arbitrary named secret
from the operating-system store.

Keep a separately recoverable copy of the repository password in an approved
secret or password manager. That copy is the disaster-recovery source of truth
when a device or its operating-system credential store is lost. The local
Kopia-created entry may remain for reconnect and unattended scheduling; do not
build a custom secret-manager-to-OS-store mirror merely to reproduce this
standard behavior.

Storage-provider credentials are separate. For example, an S3 access-key
identifier and secret may be persisted in Kopia's connection configuration.
Protect that configuration as credential-bearing data; the operating-system
store statement above applies specifically to the repository password.

## Choose persistent or process-scoped operation

Current Kopia CLI flags describe `--persist-credentials` as enabled by default.
Use Kopia's own persistence when the local operator accepts the protected OS
entry and needs reconnect or unattended scheduling.

Use `--no-persist-credentials` when policy forbids local repository-password
persistence. Supply the password to every fresh process or startup through a
narrowly scoped mechanism such as `KOPIA_PASSWORD`, and clear it when the
process ends. Do not promise reboot-surviving unattended operation unless that
startup injection path is deliberately designed and verified.

Before applying either mode, inspect the installed Kopia version's help and
current official documentation because flag and platform behavior can change:

- [Kopia command-line reference](https://kopia.io/docs/reference/command-line/)
- [Kopia global flags](https://kopia.io/docs/reference/command-line/flags/)

## Recovery and rotation checks

- Verify the separately recoverable password can connect through a bounded,
  non-logging procedure; the presence of a local OS entry is not recovery
  evidence.
- After changing the repository password, update the recovery source and each
  intended local connection without printing either value.
- After disabling persistence or disconnecting, verify the expected local
  reconnect behavior. Do not infer that a secret was removed from every store
  merely because a command succeeded.
