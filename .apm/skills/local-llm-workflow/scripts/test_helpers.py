"""Standard-library tests for profile, bundle, and output validation helpers."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import sys
import tempfile
import types
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any
from unittest.mock import patch

SCRIPT_DIRECTORY = Path(__file__).parent


def load_module(name: str, filename: str, stubs: dict[str, types.ModuleType]) -> Any:
    original = {key: sys.modules.get(key) for key in stubs}
    sys.modules.update(stubs)
    try:
        spec = importlib.util.spec_from_file_location(name, SCRIPT_DIRECTORY / filename)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load {filename}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for key, value in original.items():
            if value is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = value


hub = types.ModuleType("huggingface_hub")
hub.snapshot_download = lambda **_kwargs: None
prepare = load_module(
    "prepare_model_bundle", "prepare_model_bundle.py", {"huggingface_hub": hub}
)

torch = types.ModuleType("torch")
pillow = types.ModuleType("PIL")
pillow.Image = object()
transformers = types.ModuleType("transformers")
transformers.__version__ = "test"
transformers.AutoModelForMultimodalLM = object()
transformers.AutoProcessor = object()
runner = load_module(
    "run_local_assistant",
    "run_local_assistant.py",
    {"torch": torch, "PIL": pillow, "transformers": transformers},
)


class HelperTests(unittest.TestCase):
    def profile(self, digest: str) -> dict[str, Any]:
        return {
            "schema": 1,
            "profile_id": "test-profile",
            "model_id": "example/model",
            "revision": "a" * 40,
            "adapter_id": "transformers-multimodal-chat-v1",
            "model_class": "AutoModelForMultimodalLM",
            "files": {"weights.bin": digest},
        }

    def write_profile(
        self, directory: Path, profile: dict[str, Any]
    ) -> tuple[Path, str]:
        path = directory / "profile.json"
        path.write_text(json.dumps(profile), encoding="utf-8")
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def test_profile_hash_and_path_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = self.profile("0" * 64)
            path, digest = self.write_profile(root, profile)
            self.assertEqual(prepare.load_profile(path, digest), profile)
            with self.assertRaisesRegex(ValueError, "profile SHA-256 mismatch"):
                prepare.load_profile(path, "f" * 64)
            profile["files"] = {"../escape": "0" * 64}
            path, digest = self.write_profile(root, profile)
            with self.assertRaisesRegex(ValueError, "invalid profile file entry"):
                prepare.load_profile(path, digest)

    def test_bundle_is_bound_to_profile_and_complete_file_set(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model = root / "model"
            model.mkdir()
            weights = model / "weights.bin"
            weights.write_bytes(b"weights")
            artifact_digest = hashlib.sha256(b"weights").hexdigest()
            profile = self.profile(artifact_digest)
            profile_path, profile_digest = self.write_profile(root, profile)
            loaded = runner.load_profile(profile_path, profile_digest)
            manifest = json.loads(prepare.manifest_bytes(profile, profile_digest))
            (model / "model-manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            verified, _digest = runner.verify_model_bundle(
                model, loaded, profile_digest
            )
            self.assertEqual(verified, manifest)
            (model / "unexpected").write_text("extra", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "file set"):
                runner.verify_model_bundle(model, loaded, profile_digest)

    def test_existing_verified_bundle_is_reusable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            model = root / "model"
            model.mkdir()
            weights = model / "weights.bin"
            weights.write_bytes(b"weights")
            profile = self.profile(hashlib.sha256(b"weights").hexdigest())
            _, profile_digest = self.write_profile(root, profile)
            manifest = prepare.manifest_bytes(profile, profile_digest)
            (model / "model-manifest.json").write_bytes(manifest)
            self.assertEqual(
                prepare.verify_existing_bundle(model, profile, profile_digest),
                hashlib.sha256(manifest).hexdigest(),
            )
            output = io.StringIO()
            with (
                patch.object(
                    sys,
                    "argv",
                    [
                        "prepare_model_bundle.py",
                        "--profile",
                        str(root / "profile.json"),
                        "--profile-sha256",
                        profile_digest,
                        "--destination",
                        str(model),
                    ],
                ),
                patch.object(
                    prepare,
                    "snapshot_download",
                    side_effect=AssertionError("reused bundle must not download"),
                ),
                redirect_stdout(output),
            ):
                self.assertEqual(prepare.main(), 0)
            self.assertEqual(json.loads(output.getvalue())["status"], "reused")
            (model / "unexpected").write_text("extra", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "file set"):
                prepare.verify_existing_bundle(model, profile, profile_digest)

    def test_classification_rejects_unknown_labels_and_false_evidence(self) -> None:
        args = Namespace(
            command="classify",
            allowed_labels=["keep", "drop"],
            source_text="A supported statement.",
        )
        with self.assertRaisesRegex(ValueError, "label is not"):
            runner.validate_result(
                args,
                {"label": "other", "evidence": [], "uncertain": False},
            )
        with self.assertRaisesRegex(ValueError, "at least one evidence"):
            runner.validate_result(
                args,
                {"label": "keep", "evidence": [], "uncertain": False},
            )
        with self.assertRaisesRegex(ValueError, "non-empty strings"):
            runner.validate_result(
                args,
                {"label": "keep", "evidence": ["  "], "uncertain": False},
            )
        with self.assertRaisesRegex(ValueError, "exact source span"):
            runner.validate_result(
                args,
                {"label": "keep", "evidence": ["invented"], "uncertain": False},
            )

    def test_localization_rejects_invalid_coordinates(self) -> None:
        args = Namespace(command="locate")
        with self.assertRaisesRegex(ValueError, "bbox"):
            runner.validate_result(args, {"bbox": [10, 10, 5, 20], "uncertain": False})

    def test_batch_discovery_is_sorted_bounded_and_confined(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "b.txt").write_text("b", encoding="utf-8")
            (root / "a.txt").write_text("a", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "duplicate.txt").write_text("a", encoding="utf-8")
            args = Namespace(input_directory=root, glob="*.txt", max_files=2)
            self.assertEqual(
                [path.name for path in runner.discover_batch_inputs(args)],
                ["a.txt", "b.txt"],
            )
            self.assertEqual(runner.batch_input_id(root / "a.txt", root), "a.txt")
            self.assertEqual(
                runner.batch_input_id(nested / "duplicate.txt", root),
                "nested/duplicate.txt",
            )
            args.max_files = 1
            with self.assertRaisesRegex(ValueError, "limit"):
                runner.discover_batch_inputs(args)
            args.max_files = 2
            args.glob = "../*.txt"
            with self.assertRaisesRegex(ValueError, "non-recursive"):
                runner.discover_batch_inputs(args)
            args.glob = "**/*.txt"
            with self.assertRaisesRegex(ValueError, "non-recursive"):
                runner.discover_batch_inputs(args)

    def test_text_input_rejects_empty_and_whitespace_only_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.txt"
            for content in ("", " \n\t"):
                path.write_text(content, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "must not be empty"):
                    runner.read_text(path, 100)

    def test_batch_continues_after_midstream_runtime_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ("a.txt", "b.txt", "c.txt"):
                (root / name).write_text(name, encoding="utf-8")
            args = Namespace(
                input_directory=root,
                glob="*.txt",
                max_files=3,
                max_new_tokens=32,
                labels=["keep", "drop", "review"],
                max_input_chars=100,
            )
            visited: list[str] = []

            def fake_run_task(
                task_args: Namespace,
                _processor: object,
                _model: object,
                _metadata: dict[str, Any],
            ) -> int:
                visited.append(task_args.input_id)
                if task_args.input_id == "b.txt":
                    raise RuntimeError("simulated device failure")
                return 0

            output = io.StringIO()
            with patch.object(runner, "run_task", side_effect=fake_run_task):
                with redirect_stdout(output):
                    status = runner.run_batch(args, object(), object(), {"run": "test"})
            self.assertEqual(status, 1)
            self.assertEqual(visited, ["a.txt", "b.txt", "c.txt"])
            record = json.loads(output.getvalue())
            self.assertEqual(record["status"], "error")
            self.assertEqual(record["input_id"], "b.txt")
            self.assertIsNone(record["prompt_sha256"])
            self.assertEqual(record["generation"]["max_new_tokens"], 32)

    def test_generation_failure_retains_prompt_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "input.txt"
            path.write_text("supported text", encoding="utf-8")
            args = Namespace(
                command="classify",
                input=path,
                input_id="input.txt",
                labels=["keep", "drop"],
                max_input_chars=100,
                max_new_tokens=32,
            )
            output = io.StringIO()
            with patch.object(
                runner, "generate", side_effect=RuntimeError("simulated failure")
            ):
                with redirect_stdout(output):
                    status = runner.run_task(args, object(), object(), {"run": "test"})
            self.assertEqual(status, 1)
            record = json.loads(output.getvalue())
            self.assertEqual(record["status"], "error")
            self.assertEqual(len(record["prompt_sha256"]), 64)
            self.assertEqual(record["generation"]["max_new_tokens"], 32)


if __name__ == "__main__":
    unittest.main()
