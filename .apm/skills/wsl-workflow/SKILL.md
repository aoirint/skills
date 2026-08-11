---
name: wsl-workflow
description: >-
  Diagnose, configure, and verify Windows Subsystem for Linux environments. Use for WSL startup failures,
  Windows/Linux path and permission issues, wsl.conf or .wslconfig changes, systemd services, DrvFs mounts, and
  persistent bindfs mounts.
---

# WSL Workflow

## Goals

- Distinguish Windows-host configuration from per-distribution Linux configuration.
- Diagnose from current evidence before changing startup, mount, or interoperability settings.
- Make WSL changes reversible and verify them after a full distribution restart.
- Persist bindfs mounts without racing the Windows-drive mount during WSL startup.

## Workflow

1. Establish the disclosure boundary before running any evidence command. If raw output would leave the authorized
   private environment or enter a public/shared transcript, have the user capture it locally, sanitize it, and
   provide only the minimum excerpt. Treat hostnames and system fingerprints as potentially private alongside paths
   and credentials. If a secret is already disclosed, stop further output, never repeat the value, and tell the user
   to revoke or rotate it through the owning service; editing or deleting the transcript is not sufficient
   remediation.

2. Identify the distribution, WSL version, init system, and failing boundary. Run read-only checks first:

    ```shell
    uname -a
    cat /etc/os-release
    ps -p 1 -o comm=
    command -v wsl.exe >/dev/null && wsl.exe --version
    test -e /etc/wsl.conf && printf '/etc/wsl.conf exists\n'
    findmnt --target / -o FSTYPE,OPTIONS
    ```

3. Separate the configuration layers:
   - Use `/etc/wsl.conf` for one distribution, including systemd, DrvFs automount, the default user, networking, and
     Windows interoperability.
   - Use `%UserProfile%\.wslconfig` for global WSL 2 VM resources and behavior.
   - Use Windows `wsl.exe` commands for distribution lifecycle operations. Invoke `wsl.exe` from WSL when useful,
     but state when the user must run an elevated Windows command.

4. Collect evidence at the failing layer. Do not run broad `findmnt`, configuration dumps, verifier commands,
   `dmesg`, or `journalctl` through an exposed channel. Prefer a known target with selected output columns, a named
   unit, the current boot, and a narrow error pattern.
   - Startup and kernel: `dmesg`, `journalctl -b`, and `systemctl --failed`.
   - Mounts: use `findmnt` and `findmnt --verify --tab-file /etc/fstab` for read-only inspection. Treat `mount -av`
     as a state-changing test; run it only after reviewing the entire table and only when the user authorized
     applying or testing all eligible entries.
   - Windows paths: confirm the relevant DrvFs source such as `/mnt/c/...` exists before blaming FUSE or
     permissions.
   - Permissions: record `id`, source ownership, target ownership, mount options, and the effective process user. Do
     not assume UID/GID 1000.
   - Performance: measure the same representative operation on the current filesystem and on the WSL Linux
     filesystem. Keep tool versions, dependency state, and workload constant; do not diagnose from subjective speed
     alone. Record the effective `.wslconfig` CPU, memory, and swap limits plus runtime evidence such as `nproc`,
     `free`, `swapon --show`, and CPU/memory pressure during identical trials. Similar slowness or saturation in
     both locations is not proof that a VM limit caused it. To attribute the problem to a configured limit, verify
     the applied runtime ceiling, preserve the exact original `.wslconfig` content and relevant Windows metadata,
     change only that limit with authorization, and use an authorized Windows-side controller. With confirmation,
     run `wsl.exe --shutdown`. Wait until `wsl.exe --list --running` reports no distributions before restarting the
     distribution, then verify the new ceiling and repeat the full DrvFs-versus-Linux-filesystem paired trial as a
     counterfactual. Restore the original setting and repeat the full shutdown and ceiling verification after the
     trial unless the user explicitly requests retaining the new limit.

   Redact credentials, tokens, usernames, private hostnames, and private paths before transmitting collected output
   or placing it in an artifact. Inspect `fstab` entries for inline credentials or credential-file locations before
   quoting them. Never read or copy a credential file merely to diagnose its mount entry.

5. Before editing a privileged Linux configuration file or Windows host configuration such as `.wslconfig`, show the
   exact file, intended change, expected effect, restart requirement, and rollback path. Preserve the original
   content and applicable Linux mode/ownership or Windows metadata in a collision-resistant backup. If the file was
   absent, record that fact and the hash of the exact task-created bytes. Restore absence only after confirming the
   path is still a regular file with that hash; any mismatch or replacement blocks deletion as a possible later user
   change. Do not overwrite or remove unrelated later user changes.

6. Apply the smallest change that addresses the observed failure. Validate syntax before restarting. For systemd
   units, run `systemd-analyze verify`, `systemctl daemon-reload`, and the narrow unit start or enable operation.

7. Verify both immediate and restarted state. Changes to `/etc/wsl.conf` generally require fully stopping the
   distribution. Resolve the exact distribution name and obtain explicit confirmation immediately before running
   `wsl.exe --terminate <Distribution>` from a Windows shell or another distribution; warn that its current sessions
   will end. Obtain explicit confirmation before `wsl.exe --shutdown` because it stops every running WSL
   distribution. After restart, recheck the current boot logs, unit result, and actual mount or process state. If
   restart is not confirmed or cannot be observed, defer and mark restart verification unverified.

For diagnosis-only or evidence-incomplete work, keep observed facts, sanitized evidence gaps, hypotheses, planned
changes, applied changes, and post-change verification separate. Leave unavailable configuration, logs, and restart
results explicitly unverified. Do not present a hypothesis or proposed write as a proven cause or completed fix.

## WSL Operating Guidance

- Prefer the Linux filesystem for Linux build trees, package caches, databases, Unix sockets, and
  permission-sensitive workloads. Use `/mnt/<drive>` when Windows applications need direct access and accept DrvFs
  semantics and possible I/O overhead.
- Use Windows paths through `wslpath` rather than manually translating complex paths.
- Treat path case, executable bits, ownership, symlinks, and file-watcher behavior as filesystem-boundary concerns.
  Inspect the active filesystem and mount options before changing application settings.
- When investigating slow builds or unreliable file watching below `/mnt/<drive>`, compare a disposable
  Linux-filesystem copy of the same revision. Use identical lockfiles, tool versions, workloads, and watcher
  settings; give each location separate dependencies, cache, and output directories; warm them identically; and run
  repeated trials. Declare the acceptable timing variance and watcher correctness threshold before testing. If only
  the Linux copy improves beyond that threshold, keep the project, dependencies, caches, and build output in the
  Linux filesystem and let Windows tools access it through WSL integration. Use polling watchers only as a measured
  fallback because they can increase load.
- Keep generated files, credentials, and private keys on the side whose permission and backup model owns them. Never
  weaken permissions broadly merely to make Windows and Linux tools interoperate.
- Confirm whether systemd is PID 1 before relying on units. To enable it on supported WSL versions, set
  `[boot] systemd=true` in `/etc/wsl.conf`, restart WSL completely, then verify with `systemctl status`.
- Do not infer persistence from a successful manual command. Verify the configured startup mechanism after a new WSL
  boot.

## Persistent bindfs Mounts

Read [references/bindfs-persistence.md](references/bindfs-persistence.md) whenever configuring, repairing, or
reviewing a persistent bindfs mount. Use an ordinary `/etc/fstab` entry for sources that are reliably available when
`mount -a` runs. For a source below `/mnt/<drive>`, prefer an explicit systemd mount unit when startup logs show WSL
processing `fstab` before the DrvFs source exists.

## Completion Criteria

- Record the original symptom and baseline. Record an evidence-backed cause when established; otherwise record the
  remaining hypotheses and evidence gap without inventing a pass.
- Preserve a rollback artifact for every privileged file changed.
- Pass configuration-specific validation without suppressing real errors.
- Verify the requested behavior after the required WSL restart, or clearly leave that restart verification to the
  user.
