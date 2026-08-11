from __future__ import annotations

import argparse
import hashlib
import re
from collections import defaultdict
from pathlib import Path
from typing import Sequence

ACTION_FILE_NAMES = ("action.yml", "action.yml.template")
ACTION_PATH_PATTERN = re.compile(
    r"^(?:check|test|build|deploy|setup|install|resolve)-[a-z0-9]+(?:-[a-z0-9]+)+$"
)
BARE_ACTION_NAMES = {"build", "check", "deploy", "setup", "test"}
RETIRED_PATH_PATTERN = re.compile(
    r"\.github/actions/(?:lint-node|check-hugo|lint-docker|check-source|test-source|"
    r"setup-python|setup-dotnet|generate-version|publish-thunderstore)(?:/|\s|$)"
)
LOCAL_SETUP_PATTERN = re.compile(r"uses:\s+\./\.github/actions/setup-[a-z0-9-]+")
OWNERSHIP_CLEANUP_PATTERN = re.compile(
    r"if:\s+always\(\)\s+&&\s+steps\.[a-z0-9-]+\.outputs\.[a-z0-9-]+\s*==\s*'true'"
)


def _action_directories(skills_root: Path) -> list[Path]:
    return sorted(
        {
            action_file.parent
            for file_name in ACTION_FILE_NAMES
            for action_file in skills_root.glob(f"*/assets/**/{file_name}")
        }
    )


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_composite_actions(skills_root: Path) -> list[str]:
    errors: list[str] = []
    action_directories = _action_directories(skills_root)
    paths_by_name: dict[str, list[Path]] = defaultdict(list)
    files_by_hash: dict[str, list[Path]] = defaultdict(list)

    for action_directory in action_directories:
        paths_by_name[action_directory.name].append(action_directory)
        if ACTION_PATH_PATTERN.fullmatch(action_directory.name) is None:
            errors.append(
                f"invalid action path: {action_directory.relative_to(skills_root)}"
            )

        action_file = next(
            action_directory / name
            for name in ACTION_FILE_NAMES
            if (action_directory / name).is_file()
        )
        action_text = action_file.read_text(encoding="utf-8")
        first_line = action_text.splitlines()[0] if action_text else ""
        action_name = first_line.removeprefix("name:").strip().lower()
        if not first_line.startswith("name:") or action_name in BARE_ACTION_NAMES:
            errors.append(
                f"ambiguous action name: {action_file.relative_to(skills_root)}"
            )
        if RETIRED_PATH_PATTERN.search(action_text) is not None:
            errors.append(
                f"retired local-action path: {action_file.relative_to(skills_root)}"
            )
        if (
            LOCAL_SETUP_PATTERN.search(action_text) is not None
            and OWNERSHIP_CLEANUP_PATTERN.search(action_text) is None
        ):
            errors.append(
                f"missing ownership-gated cleanup: {action_file.relative_to(skills_root)}"
            )

        for asset_file in sorted(
            path for path in action_directory.rglob("*") if path.is_file()
        ):
            files_by_hash[_file_hash(asset_file)].append(asset_file)

    for action_name, directories in sorted(paths_by_name.items()):
        if len(directories) > 1:
            locations = ", ".join(
                str(path.relative_to(skills_root)) for path in directories
            )
            errors.append(f"duplicate action path {action_name}: {locations}")

    for duplicate_files in sorted(
        files_by_hash.values(), key=lambda paths: str(paths[0])
    ):
        owning_skills = {
            path.relative_to(skills_root).parts[0] for path in duplicate_files
        }
        if len(owning_skills) > 1:
            locations = ", ".join(
                str(path.relative_to(skills_root)) for path in duplicate_files
            )
            errors.append(f"duplicate cross-Skill action asset: {locations}")

    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check canonical Composite Action contracts."
    )
    parser.add_argument(
        "skills_root", type=Path, help="Canonical .apm/skills directory."
    )
    args = parser.parse_args(argv)

    errors = validate_composite_actions(args.skills_root.resolve())
    if errors:
        for error in errors:
            print(error)
        return 1

    print("Composite Action contracts are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
