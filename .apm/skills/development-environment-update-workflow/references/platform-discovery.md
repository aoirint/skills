# Platform Discovery and Verification

Use only the section for each in-scope environment. Discover existing managers;
examples below are not installation recommendations. The maintained baseline is
Windows 11 25H2 or later and Ubuntu 24.04 or later, as described in `SKILL.md`.
Keep an environment ledger so evidence from one host or distribution is never
substituted for another.

## Windows

- Record Windows release, architecture, user, terminal shell, and relevant IDE
  launch context. Inspect user and machine installation records and the actual
  manager sources. WinGet, vendor installers, portable tools, and language
  managers can coexist; one manager's inventory does not cover them all.
- Inspect command precedence, aliases, functions, application aliases, shims,
  and PATH entries before running the target. PowerShell's
  [Get-Command documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-command)
  explains `-All` and `-ListImported`. Exact-name lookup can import a module;
  use `-ListImported` or another constrained inspection where that would execute
  unreviewed code. Collect only the fields needed to identify resolution.
- Distinguish per-user and machine installations and check architecture and
  installer identity. If WinGet owns the target, consult its
  [upgrade documentation](https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade)
  for the installed version's ID, source, version, and scope selectors.
  Do not infer that selecting a package constrains every installer side effect
  or satisfies artifact review. Never default to upgrading all applications.
- Verify the effective command from the intended Windows shell and affected
  project directory, including the IDE's selected SDK/interpreter if relevant.
  Do not use a working Linux command as proof that the Windows tool works.

## Ubuntu on WSL2

- Identify the Windows host, exact registered distribution, WSL generation,
  Ubuntu release, architecture, and active Linux shell. Microsoft's
  [WSL command reference](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
  distinguishes WSL version/status and distribution-list inspection from
  update and lifecycle operations. Do not launch an unrequested distribution
  or update WSL merely to inventory it.
- Keep the Windows WSL platform/kernel, Ubuntu guest packages, and user/project
  tools as separate update targets. Updating WSL is not an Ubuntu package
  update; guest package evidence does not verify the host's WSL installation.
- Apply the Ubuntu checks below within the named guest. Inspect whether command
  resolution crosses into a Windows executable or inherited Windows PATH.
  Record project filesystem placement when native dependencies or host/guest
  interoperability can affect the result. Do not relocate projects as part of
  an update unless that move is separately in scope.
- Use `wsl-workflow` for interoperation settings, mounts, startup configuration,
  and restarts. A successful guest update is not verification after a WSL
  restart; report that check separately when required.

## Ubuntu package and shell layers

These checks apply independently to native Ubuntu and each Ubuntu WSL2 guest.
Native Ubuntu does not inherit WSL lifecycle or Windows PATH assumptions.

- Record `/etc/os-release`, architecture, and relevant package-manager metadata.
  Discover distribution packages, manually installed tools, user managers,
  virtual environments, and project selectors. Preserve the distribution's
  system runtimes; an application runtime update is not permission to replace
  the interpreter or libraries used by OS tooling.
- In Bash, use narrow `type -a` or `command -v` inspection for the target,
  then trace relevant links/shims and their owner. Check project directory,
  activation state, and shell initialization; do not dump the full environment
  or source unknown configuration to obtain a version.
- For APT-owned targets, inspect installed and candidate distro revisions,
  sources, holds/pins, architecture, and dependent packages. Use documentation
  for that Ubuntu release: the
  [Ubuntu apt-get manual](https://manpages.ubuntu.com/manpages/noble/man8/apt-get.8.html)
  includes a release selector, exact-version selection, and simulation behavior.
  Simulation does not lock the package state, and limited read access can make
  its result incomplete. Reconcile the final transaction before execution;
  inspect dependency changes and maintainer-script/service effects under the
  common security gates. An index refresh changes metadata and is not a tool
  upgrade or a guarantee of an eligible candidate.
- Treat distribution upgrades, kernel changes, service restarts, and cleanup as
  distinct operations, not implicit steps in updating a development CLI.
  Verify affected command resolution and representative projects in the native
  machine or named guest that actually owns the installation.
