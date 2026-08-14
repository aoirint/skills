# Repository lifecycle

## Choose boundaries

One repository can protect several source roots when they share an operator,
credential boundary, destination, retention model, and disaster-recovery goal.
Split repositories when those properties differ materially. Avoid one
repository per project unless independent deletion, access, or portability is
worth the extra credentials and maintenance.

A practical media workflow often has three source states:

- active editing on fast local storage;
- inactive editable workspaces retained for possible return;
- adopted masters retained for publication and reuse.

They do not have to be separate repositories. Different source policies can
express different schedules and retention inside one repository. Split masters
when their long-term retention, cataloging, access, or restore path differs from
editable workspaces.

## Preserve history across classification changes

Kopia snapshots belong to a source identity. Moving files between source roots
does not rewrite earlier snapshots, and content deduplication does not by itself
move snapshot history to another repository. Preserve the old snapshot until a
new snapshot of the destination exists and its restore path is understood.

Use pinned snapshots for milestones such as initial migration, publication, or
pre-deletion state. Review pins periodically because they override ordinary
retention and can prevent space reclamation.

## Copies and offline media

A local repository on the source disk protects against ordinary file history
loss but not device loss. Maintain at least one independent repository copy.
An external disk can be a periodically synchronized replica: configure the job
to fail when the expected destination is absent and catch it up when attached.
Do not treat an intermittently connected replica as current without recording
its last successful synchronization.

For a removable destination, match both a stable device or volume identity and
the expected Kopia repository identity. A drive letter or mount path alone is
not sufficient. If either identity is absent or mismatched, exit without
initializing, replacing, synchronizing, or deleting. Persist a non-secret sync
record containing the source and destination repository identities, Kopia
version, completion time, covered snapshot or resulting repository state, and
errors. Describe the replica as current only through that recorded completion.

## Retirement

Before removing local source data, record a recoverable snapshot, its repository
and replica locations, the restoring Kopia version, and a bounded restore test.
Snapshot expiration is logical; maintenance is needed to reclaim unreferenced
content. Never delete the last understood copy merely because another storage
location is configured.
