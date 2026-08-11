# Persistent bindfs Mounts on WSL

## Contents

- Purpose and selection
- Preflight
- Ordinary fstab persistence
- DrvFs startup-race pattern
- Explicit systemd mount unit
- Validation and restart proof
- Recovery
- References

## Purpose and selection

Use bindfs when the same directory must appear at another path with a different ownership or permission view. Prefer
a normal bind mount when no ownership or permission transformation is needed.

Choose persistence based on source readiness:

- Use `/etc/fstab` when the source is available when WSL invokes `mount -a`.
- Use an explicit systemd `.mount` unit when the source is under an automatically mounted Windows drive and logs
  prove that WSL's early `fstab` pass runs before that source exists.
- Do not add `nofail` as a guess. Test the actual failure: a missing bindfs source can still make `mount -a` return
  nonzero.

## Preflight

Establish the output boundary first. In a public or shared transcript, ask the user to run raw configuration and log
commands locally and return sanitized, minimal excerpts. Do not emit an entire `fstab`, mount table, or boot log
merely to find one bindfs failure.

1. Confirm systemd, bindfs, FUSE, and both directories:

    ```shell
    test "$(ps -p 1 -o comm=)" = systemd
    command -v bindfs
    bindfs --version
    test -d /mnt/c/path/to/source
    test -d /home/USER/path/to/target
    ```

2. Record the real IDs instead of assuming them:

    ```shell
    id -u USER
    id -g USER
    ```

3. Record the target's pre-change mount state with `findmnt --target`, including source, filesystem, and options. If
   it is already mounted, do not replace or unmount it unless that exact transition and restoration are authorized
   and recorded.

4. When current-boot mount changes are authorized, prove the intended mapping with a manual mount, inspect it with
   `findmnt`, exercise the required read/write behavior, and unmount it before installing persistence. Otherwise,
   use already-recorded successful manual-mount evidence or defer behavioral proof until restart. Understand every
   option. In particular, `allow_other` broadens FUSE access beyond the mounting user and must match the intended
   access policy.

5. Before quoting `/etc/fstab` or logs in a public artifact, redact inline credentials, credential-file locations,
   private usernames, hostnames, and paths. Preserve the option names and failure text needed for diagnosis.

   Apply the same redaction before transmitting collected output to another person or service. Do not read, copy,
   relocate, or publish a credential file merely because `fstab` references it.

## Ordinary fstab persistence

For a source that is ready during `mount -a`, use the filesystem type documented by bindfs:

```fstab
/source/path /target/path fuse.bindfs map=root/1000:@root/@1000,allow_other 0 0
```

Replace both IDs with verified values. Escape whitespace and other `fstab`-significant characters correctly. Then
validate before relying on the entry:

```shell
sudo findmnt --verify --verbose --tab-file /etc/fstab
sudo mount -av
findmnt --target /target/path
```

`mount -av` can activate every eligible entry, including remote filesystems. Run it only for an authorized apply or
test operation after reviewing the entire table; use `findmnt --verify` alone for read-only validation.

Do not duplicate the same mount in both `fstab` and a hand-written systemd unit.

## DrvFs startup-race pattern

This failure has a recognizable evidence chain:

1. The bindfs entry works when run manually after login.
2. The current source and target both exist.
3. Early boot logs contain `Failed to resolve source directory` for a path below `/mnt/<drive>` followed by
   `Processing /etc/fstab with mount -a failed`.
4. A later systemd-generated or manual mount succeeds.

This points to ordering, not malformed bindfs options. Remove only the affected bindfs entries from `/etc/fstab` and
represent them as explicit systemd mount units. Leave unrelated `fstab` entries and `/etc/wsl.conf` settings intact.

Before editing, create a collision-resistant backup while preserving metadata, for example:

```shell
backup=/etc/fstab.backup.$(date -u +%Y%m%dT%H%M%SZ)
sudo test ! -e "$backup" || { printf 'backup already exists: %s\n' "$backup" >&2; exit 1; }
sudo cp --preserve=mode,ownership,timestamps /etc/fstab "$backup"
```

Record the resolved backup path. Refuse to overwrite an existing backup.

## Explicit systemd mount unit

1. Derive the mandatory unit filename from the target path:

    ```shell
    systemd-escape --path --suffix=mount /home/USER/path/to/target
    ```

   Inspect the resolved path under `/etc/systemd/system` before writing. For every affected `.mount`, `.path`, or
   readiness unit, record file existence and hash plus `systemctl is-enabled` and `systemctl is-active` results. If
   a unit file already exists, preserve it in a collision-resistant, metadata-preserving backup and record that
   path. For a new file, record removal of that exact file as its rollback. Never overwrite an existing unit without
   a reviewed backup.

2. Create `/etc/systemd/system/<escaped-name>.mount`. The `Where=` value must exactly correspond to the escaped
   filename:

    ```ini
    [Unit]
    Description=bindfs mount for application data
    After=systemd-remount-fs.service

    [Mount]
    What=/mnt/c/path/to/source
    Where=/home/USER/path/to/target
    Type=fuse.bindfs
    Options=map=root/1000:@root/@1000,allow_other

    [Install]
    WantedBy=local-fs.target
    ```

3. Replace paths and IDs with inspected values. If `allow_other` is unnecessary, omit it. Never interpolate shell
   commands such as `$(id -u)` into a unit file; systemd does not evaluate them as a shell.

   `After=systemd-remount-fs.service` moves this work into the systemd phase; it is not a universal readiness
   guarantee for every Windows drive, network share, or custom automount. Use this unit when a later
   systemd-generated or manually started unit already succeeds in the current boot, then prove the ordering after
   restart. If a restarted unit still races, stop and design activation around the source's actual readiness signal.
   Do not hide the race with an arbitrary sleep or an unbounded retry loop.

4. Validate and enable the exact unit:

    ```shell
    sudo systemd-analyze verify /etc/systemd/system/<escaped-name>.mount
    sudo systemctl daemon-reload
    sudo systemctl enable <escaped-name>.mount
    # Add --now only when changing the current boot is explicitly authorized.
    systemctl show <escaped-name>.mount -p LoadState -p ActiveState -p SubState -p Result -p FragmentPath
    findmnt --target /home/USER/path/to/target
    ```

   For a startup-only change, stop after validation and `enable`; verify `systemctl is-enabled`, leave runtime mount
   behavior explicitly unverified, and prove it after restarting the distribution.

If multiple units are required, validate each source and target independently and avoid overlapping target mounts.

### Source-readiness fallback

When the source appears after the ordinary systemd mount attempt, first test whether systemd path activation
observes it. Create a narrowly named `.path` unit with `PathExists=/mnt/<drive>/path/to/source` and
`Unit=<escaped-name>.mount`, disable direct enablement of the mount unit, and enable the path unit instead. Record
the prior enabled and active state of both units before changing it. Validate both unit files and prove behavior
across restart; do not assume DrvFs notifications work on every WSL version.

If path activation is not observable, stop and disable the experimental `.path` unit, then remove it if new or
restore its prior file and state before introducing another activation owner. Verify that it can no longer trigger
the mount. Use a purpose-built oneshot readiness unit that the mount unit names with both `Requires=` and `After=`.
Keep the mount unit as the enabled startup owner. Bound the helper's polling interval and total timeout, return
failure when the source never appears, and log the final reason. Record both units' original file, enabled, and
active states; validate the dependency graph and test the helper independently. Do not use a fixed startup sleep, an
unbounded loop, or a success exit when the source is still absent.

## Validation and restart proof

Before restart, require all of the following:

- `findmnt --verify --tab-file /etc/fstab` succeeds.
- When an all-entry mount test was authorized, `mount -av` no longer attempts a removed entry or emits its old
  error; otherwise leave this check deferred.
- `systemd-analyze verify` accepts every new unit.
- For a startup-only change, the mount unit is loaded and enabled; leave active/mounted state and `findmnt` behavior
  deferred until restart.
- When current-boot activation was authorized, the mount unit reports `active`, `mounted`, and `Result=success`, and
  `findmnt --target` shows the intended source, target, filesystem, and options.

For a readiness fallback, also verify the helper according to its declared lifecycle: a `.path` unit is loaded,
enabled, and actively waiting or has successfully triggered; a oneshot unit has `Result=success` and its expected
`active/exited` or `inactive/dead` state. In every variant, the mount unit—not merely the helper—must be mounted
successfully. Inspect current-boot helper and mount journals for timeout or retry exhaustion.

Then fully stop the affected distribution from a Windows shell or another distribution. For a single-distribution
test, prefer `wsl.exe --terminate <Distribution>` and warn that its current sessions will end. Use
`wsl.exe --shutdown`
only after explicit confirmation because it stops every running distribution. On the next start, inspect only the
current boot and repeat the unit and `findmnt` checks. Absence of the old error plus a live mount establishes
persistence; either fact alone is insufficient.

## Recovery

If the persistence change fails:

1. Inspect `systemctl status <unit>` and `journalctl -b -u <unit>`.
2. Confirm that the Windows source exists now and that DrvFs automount is enabled as intended.
3. Compare current files and unit states with the recorded pre-change inventory; stop before overwriting unrelated
   later changes.
4. Stop task-activated `.path` and readiness helpers, then stop or unmount every task-activated bindfs mount,
   whether it came from a unit, a manual command, or `fstab`, in dependency-safe order. Verify with
   `findmnt --target` that the target is unmounted or has returned to its recorded pre-change mount state before restoring
   another startup owner.
5. Remove only newly created unit files, restore every replaced unit from its verified backup, and restore each
   unit's prior enabled/disabled state.
6. Restore the timestamped `fstab` backup only when it is the verified rollback target; do not overwrite later
   unrelated changes.
7. Run `systemctl daemon-reload`, repeat syntax validation, and verify the restored enablement and target mount
   state against the inventory. Restore prior active state only when doing so is safe and authorized; otherwise
   record the deferred runtime restoration.

Do not disable SSH verification, weaken FUSE access, or grant broad filesystem permissions as a mount-order
workaround.

## References

- [Microsoft: Advanced settings configuration in WSL](https://learn.microsoft.com/windows/wsl/wsl-config)
- [Microsoft: Use systemd to manage Linux services with WSL](https://learn.microsoft.com/windows/wsl/systemd)
- [bindfs manual page](https://bindfs.org/docs/bindfs.1.html)
- [systemd mount unit documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html)
- [systemd path unit documentation](https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html)
