#!/usr/bin/env bash

set -euo pipefail

SKILL_ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
readonly SKILL_ROOT
readonly SCRIPT_PATH="${SKILL_ROOT}/assets/github/actions/setup-node-locked/resolve-node-contract.sh"
TEST_ROOT=$(mktemp -d)
readonly TEST_ROOT

cleanup() {
  rm -rf -- "$TEST_ROOT"
}
trap cleanup EXIT

write_package() {
  local directory=$1
  local package_manager=$2

  mkdir -p -- "$directory"
  printf '{"packageManager":"%s"}\n' "$package_manager" >"${directory}/package.json"
  : >"${directory}/pnpm-lock.yaml"
}

test_valid_contract() {
  local package_directory="${TEST_ROOT}/valid"
  local output_path="${TEST_ROOT}/valid-output"
  write_package "$package_directory" 'pnpm@11.0.0'

  NODE_PACKAGE_DIRECTORY="$package_directory" \
    NODE_LOCKFILE_PATH='' \
    GITHUB_OUTPUT="$output_path" \
    bash "$SCRIPT_PATH"

  grep -Fx "lockfile-path=${package_directory}/pnpm-lock.yaml" "$output_path"
  grep -Fx 'pnpm-version=11.0.0' "$output_path"
}

test_invalid_package_manager() {
  local package_directory="${TEST_ROOT}/invalid-manager"
  write_package "$package_directory" 'npm@11.0.0'

  if NODE_PACKAGE_DIRECTORY="$package_directory" \
    NODE_LOCKFILE_PATH='' \
    GITHUB_OUTPUT="${TEST_ROOT}/invalid-manager-output" \
    bash "$SCRIPT_PATH"; then
    printf 'Expected an invalid package manager to fail.\n' >&2
    return 1
  fi
}

test_missing_lockfile() {
  local package_directory="${TEST_ROOT}/missing-lock"
  write_package "$package_directory" 'pnpm@11.0.0'
  rm -- "${package_directory}/pnpm-lock.yaml"

  if NODE_PACKAGE_DIRECTORY="$package_directory" \
    NODE_LOCKFILE_PATH='' \
    GITHUB_OUTPUT="${TEST_ROOT}/missing-lock-output" \
    bash "$SCRIPT_PATH"; then
    printf 'Expected a missing lockfile to fail.\n' >&2
    return 1
  fi
}

test_valid_contract
test_invalid_package_manager
test_missing_lockfile
