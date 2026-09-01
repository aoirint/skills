# Task conventions

## Core task names

Use these names when the repository has the corresponding operation.

| Task | Contract |
| --- | --- |
| `sync` | Reproduce reviewed managed tools and project dependencies from committed locks. It may update local tool/package environments and caches, but not maintained source, configuration, or locks. |
| `format` | Rewrite maintained source using configured formatters. It must not lint, test, resolve, or update dependencies. |
| `format-check` | Verify formatting without rewriting files. It may be composed into `check`. |
| `lint` | Run static style and correctness diagnostics without rewriting source. |
| `typecheck` | Run the ecosystem type checker without rewriting source or locks. |
| `test` | Run deterministic behavioral tests and the repository coverage gate. |
| `build` | Produce the ordinary build output from reviewed source and locks. |
| `package` | Produce and inspect distributable artifacts when packaging is distinct from building. |
| `check` | Aggregate the repository's required non-mutating validation tasks. It must not invoke `format` or any update task. |

`format`, `format-check`, and `check` may depend on `sync` when environment
reproduction is an accepted prerequisite. After that prerequisite, use the
ecosystem's no-sync execution option when available so each task's own stage has
only its declared effect. In CI, keep installation and validation visibly
separate when their logs or failure ownership differ.

Use a domain verb such as `serve`, `deploy`, `download`, or `backup` for an
operator action. Do not force unrelated operations into `run`, and avoid a task
named `install` when readers could confuse tool installation, project dependency
sync, and product deployment.

## Mutation names

Use explicit names such as `update-tools`, `update-dependencies`, or
`update-locks`. Never make them dependencies of `sync`, `format`, `check`,
`test`, `build`, or an application task. Require a reviewed scope and show the
resulting configuration and lock diffs.

The presence of an update task is not authorization to execute it. Require the
requested tool or package set and expected versions before mutation. Do not use
a repository-wide `mise up`, `mise upgrade`, or unscoped package lock upgrade
when only narrower updates were approved.

`clean` is destructive. Give it explicit, repository-bounded targets and keep
it out of ordinary validation dependencies. Prefer a recoverable or
tool-provided cleanup operation over a broad recursive shell command.

## Composition

- Keep one public task name per stable maintainer or user operation.
- Use hidden tasks for reusable internal steps that are not a supported entry
  point.
- Use dependency edges for semantic prerequisites, not merely to shorten a
  command list.
- Forward caller arguments as an array or positional parameters; do not rebuild
  them through string evaluation.
- Keep short command sequences declarative. Put complex reusable behavior in a
  typed and tested repository script, then let the task invoke it.
- Keep cross-platform public tasks free of unguarded POSIX- or Windows-only
  syntax. Put necessary platform branches in a tested script or declare and
  verify the narrower supported platform set.
- Run repository tools through their ecosystem lock, such as `uv run --locked`
  or `pnpm install --frozen-lockfile`; mise's tool lock does not replace the
  package-manager lock.

## Secret-bearing tasks

Treat the outer task as a credential adapter and the application task as a
separate trust boundary.

1. Start the credential task with only its required inherited variables when
   mise sandboxing is available.
2. Retrieve only the selected secret objects. Avoid provider commands that
   inject an entire project or collection when the application needs a subset.
3. Validate object identity and non-empty values without printing them.
4. Remove access tokens, secret identifiers, and temporary variables.
5. Invoke a hidden application task with environment inheritance denied and
   only the declared application variables allowed.

Keep provider selectors and private-resource IDs in local or CI secret
configuration, never tracked files, logs, cache keys, or public diagnostics.
Let the provider Skill define which immutable ID, collection/project identity,
key/name, duplicate, and rename checks establish object identity. Do not pass
secret values through `env KEY=value command`, an evaluated shell string, or
another argv-visible form.

Test with synthetic values and fake provider/application executables. Assert
the selected object calls, forwarded arguments, fail-closed behavior, child
environment names, and the mapping from each synthetic provider object to its
expected application variable. Let the fake application compare values in
memory without printing them. Capture stdout and stderr and assert that they do
not contain synthetic values, bootstrap tokens, or selectors. Do not use real
secret values as test fixtures or print the resulting environment values. Seed
unrelated sentinel variables and inspect the final application process after
nested mise configuration has loaded. If the allowlist boundary cannot be
proved with the pinned mise release, stop rather than documenting isolation.
Keep live secret-bearing tasks out of `check`; CI executes only their
fake-provider boundary tests.
