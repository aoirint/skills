# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#   "huggingface-hub>=1.27,<2",
# ]
# [tool.uv]
# exclude-newer = "P7D"
# ///
"""Download and verify a model bundle described by a reviewed profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from huggingface_hub import snapshot_download


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_profile(path: Path, expected_sha256: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"profile is missing or unsafe: {path}")
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError(
            f"profile SHA-256 mismatch: expected {expected_sha256}, got {actual}"
        )
    profile = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema",
        "profile_id",
        "model_id",
        "revision",
        "adapter_id",
        "model_class",
        "files",
    }
    if set(profile) != required or profile["schema"] != 1:
        raise ValueError("profile must match schema 1 exactly")
    if not all(
        isinstance(profile[key], str) and profile[key]
        for key in required - {"schema", "files"}
    ):
        raise ValueError("profile string fields must be non-empty")
    files = profile["files"]
    if not isinstance(files, dict) or not files:
        raise ValueError("profile files must be a non-empty object")
    for name, digest in files.items():
        if not isinstance(name, str):
            raise ValueError(f"invalid profile file entry: {name!r}")
        candidate = Path(name)
        if (
            candidate.is_absolute()
            or ".." in candidate.parts
            or candidate.as_posix() in {"", ".", "model-manifest.json"}
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise ValueError(f"invalid profile file entry: {name!r}")
    return profile


def manifest_bytes(profile: dict[str, Any], profile_sha256: str) -> bytes:
    manifest = {
        "schema": 1,
        "profile_id": profile["profile_id"],
        "profile_sha256": profile_sha256,
        "model_id": profile["model_id"],
        "revision": profile["revision"],
        "adapter_id": profile["adapter_id"],
        "model_class": profile["model_class"],
        "files": profile["files"],
    }
    return (
        json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode()


def verify_files(directory: Path, files: dict[str, str]) -> None:
    expected = set(files)
    actual = {
        item.relative_to(directory).as_posix()
        for item in directory.rglob("*")
        if item.is_file() or item.is_symlink()
    }
    if actual != expected:
        raise ValueError(
            f"bundle file set mismatch: expected {sorted(expected)}, got {sorted(actual)}"
        )
    for name, expected_digest in files.items():
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"missing or unsafe model file: {name}")
        actual_digest = sha256_file(path)
        if actual_digest != expected_digest:
            raise ValueError(f"SHA-256 mismatch for {name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--profile-sha256", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    profile_path = args.profile.expanduser().resolve(strict=True)
    profile = load_profile(profile_path, args.profile_sha256)
    destination = args.destination.expanduser().resolve(strict=False)
    if not destination.name:
        raise ValueError("destination must be a named directory")
    if destination.exists():
        raise ValueError(f"destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    snapshot = Path(
        snapshot_download(
            repo_id=profile["model_id"],
            revision=profile["revision"],
            allow_patterns=sorted(profile["files"]),
            token=False,
        )
    )
    staging = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.staging-", dir=destination.parent)
    )
    try:
        for name in profile["files"]:
            source = snapshot / name
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        verify_files(staging, profile["files"])
        manifest = manifest_bytes(profile, args.profile_sha256)
        manifest_sha256 = hashlib.sha256(manifest).hexdigest()
        (staging / "model-manifest.json").write_bytes(manifest)
        staging.replace(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)

    print(
        json.dumps(
            {
                "status": "ok",
                "profile_id": profile["profile_id"],
                "profile_sha256": args.profile_sha256,
                "model_id": profile["model_id"],
                "revision": profile["revision"],
                "manifest_sha256": manifest_sha256,
                "destination": str(destination),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
