#!/usr/bin/env bash

# Resolve the Node contract used by the Hugo validation action.

set -euo pipefail

main() {
  : "${NODE_PACKAGE_DIRECTORY:?NODE_PACKAGE_DIRECTORY is required}"
  : "${NODE_LOCKFILE_PATH:=}"
  : "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

  local lockfile_path=$NODE_LOCKFILE_PATH
  if [[ -z "$lockfile_path" ]]; then
    lockfile_path="${NODE_PACKAGE_DIRECTORY}/pnpm-lock.yaml"
  fi
  if [[ ! -f "$lockfile_path" ]]; then
    printf 'Lockfile does not exist: %s\n' "$lockfile_path" >&2
    return 1
  fi

  local package_json="${NODE_PACKAGE_DIRECTORY}/package.json"
  local package_manager
  package_manager=$(
    grep -oE '"packageManager"[[:space:]]*:[[:space:]]*"[^"]+"' \
      "$package_json" | head -n 1 | sed -E 's/.*"([^"]+)"$/\1/'
  ) || package_manager=''
  if [[ "$package_manager" != pnpm@* || -z "${package_manager#pnpm@}" ]]; then
    printf 'packageManager must specify pnpm@<version>: %s\n' "$package_json" >&2
    return 1
  fi

  {
    printf 'lockfile-path=%s\n' "$lockfile_path"
    printf 'pnpm-version=%s\n' "${package_manager#pnpm@}"
  } >>"$GITHUB_OUTPUT"
}

main "$@"
