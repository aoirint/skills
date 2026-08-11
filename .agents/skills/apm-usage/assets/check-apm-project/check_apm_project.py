"""Validate the project and lockfile versions expected by APM CI."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

TOP_LEVEL_SCALAR = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*?))?[ \t]*$")


def read_top_level_scalar(*, path: Path, key: str) -> str:
    """Read one non-empty top-level scalar from a small YAML metadata file."""
    matches: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line[0].isspace() or line.startswith("#"):
            continue
        match = TOP_LEVEL_SCALAR.match(line)
        if not match or match.group(1) != key:
            continue
        value = (match.group(2) or "").strip()
        if value.startswith(('"', "'")):
            quote = value[0]
            end = value.find(quote, 1)
            suffix = value[end + 1 :].strip() if end >= 0 else "invalid"
            value = (
                value[1:end]
                if end >= 0 and (not suffix or suffix.startswith("#"))
                else ""
            )
        else:
            value = re.split(r"[ \t]+#", value, maxsplit=1)[0].rstrip()
        matches.append(value)

    if len(matches) != 1 or not matches[0]:
        raise ValueError(f"{path}: expected exactly one non-empty top-level {key!r}")
    return matches[0]


def validate_versions(
    *, root: Path, expected_project_version: str, expected_apm_version: str
) -> tuple[str, ...]:
    """Return validation errors for the project and lockfile metadata."""
    checks = (
        (root / "apm.yml", "version", expected_project_version),
        (root / "apm.lock.yaml", "apm_version", expected_apm_version),
    )
    errors: list[str] = []
    for path, key, expected in checks:
        try:
            actual = read_top_level_scalar(path=path, key=key)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(str(error))
            continue
        if actual != expected:
            errors.append(f"{path}: {key} is {actual!r}; expected {expected!r}")
    return tuple(errors)


def main() -> int:
    """Run the metadata guard from its environment contract."""
    root = Path.cwd().resolve()
    expected_project_version = os.environ["APM_GUARD_EXPECTED_PROJECT_VERSION"]
    expected_apm_version = os.environ["APM_GUARD_EXPECTED_APM_VERSION"]
    errors = validate_versions(
        root=root,
        expected_project_version=expected_project_version,
        expected_apm_version=expected_apm_version,
    )
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        "APM project metadata is valid "
        f"(project {expected_project_version}, APM {expected_apm_version})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
