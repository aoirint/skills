#!/usr/bin/env python3
"""Check unpublished APM project and lock generator versions."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TOP_LEVEL_SCALAR = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*?))?[ \t]*$")
EXPECTED_APM_VERSION = "0.25.0"


def read_top_level_scalar(path: Path, key: str) -> str:
    matches: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line[0].isspace() or line.startswith("#"):
            continue
        match = TOP_LEVEL_SCALAR.match(line)
        if match and match.group(1) == key:
            value = (match.group(2) or "").strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            matches.append(value)

    if len(matches) != 1 or not matches[0]:
        raise ValueError(f"{path}: expected exactly one non-empty top-level {key!r}")
    return matches[0]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--expected-apm-version", default=EXPECTED_APM_VERSION)
    parser.add_argument("--expected-project-version", default="0.0.0")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    checks = (
        (root / "apm.yml", "version", args.expected_project_version),
        (root / "apm.lock.yaml", "apm_version", args.expected_apm_version),
    )
    errors: list[str] = []
    for path, key, expected in checks:
        try:
            actual = read_top_level_scalar(path, key)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(str(error))
            continue
        if actual != expected:
            errors.append(f"{path}: {key} is {actual!r}; expected {expected!r}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        "APM project metadata is valid "
        f"(project {args.expected_project_version}, APM {args.expected_apm_version})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
