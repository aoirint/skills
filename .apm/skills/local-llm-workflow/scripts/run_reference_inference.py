# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#   "accelerate>=1.14,<2",
#   "pillow>=12.3,<13",
#   "torch>=2.10,<3",
#   "torchvision>=0.25,<1",
#   "transformers>=5.14,<6",
# ]
# [tool.uv]
# exclude-newer = "P7D"
# ///
"""Run bounded text and vision tasks against a verified local model bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import torch
import transformers
from PIL import Image
from transformers import AutoModelForMultimodalLM, AutoProcessor

MAX_IMAGE_PIXELS = 50_000_000
DEFAULT_MAX_INPUT_CHARS = 12_000
DEFAULT_MAX_NEW_TOKENS = 512
SUPPORTED_ADAPTERS = {
    "transformers-multimodal-chat-v1": (
        "AutoModelForMultimodalLM",
        AutoModelForMultimodalLM,
    )
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve(strict=True)
    if path.is_symlink() or not path.is_file():
        raise argparse.ArgumentTypeError(f"not a safe file: {path}")
    return path


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
    adapter = SUPPORTED_ADAPTERS.get(profile["adapter_id"])
    if adapter is None or adapter[0] != profile["model_class"]:
        raise ValueError(
            f"unsupported adapter and model class: {profile['adapter_id']}, "
            f"{profile['model_class']}"
        )
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


def verify_model_bundle(
    directory: Path, profile: dict[str, Any], profile_sha256: str
) -> tuple[dict[str, Any], str]:
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f"model bundle is not a safe directory: {directory}")
    manifest_path = directory / "model-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError("model-manifest.json is missing or unsafe")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_manifest = {
        "schema": 1,
        "profile_id": profile["profile_id"],
        "profile_sha256": profile_sha256,
        "model_id": profile["model_id"],
        "revision": profile["revision"],
        "adapter_id": profile["adapter_id"],
        "model_class": profile["model_class"],
        "files": profile["files"],
    }
    if manifest != expected_manifest:
        raise ValueError("model manifest does not match the reviewed profile")
    expected_names = set(profile["files"]) | {"model-manifest.json"}
    actual_names = {
        item.relative_to(directory).as_posix()
        for item in directory.rglob("*")
        if item.is_file() or item.is_symlink()
    }
    if actual_names != expected_names:
        raise ValueError("model bundle file set does not match the reviewed profile")
    for name, expected_digest in profile["files"].items():
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"missing or unsafe model file: {name}")
        if sha256_file(path) != expected_digest:
            raise ValueError(f"model file SHA-256 mismatch: {name}")
    return manifest, sha256_file(manifest_path)


def read_text(path: Path, max_chars: int) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("input text must not be empty or whitespace-only")
    if len(text) > max_chars:
        raise ValueError(
            f"input has {len(text)} characters; limit is {max_chars}. "
            "Split the task or raise --max-input-chars deliberately."
        )
    return text


def verify_image(path: Path) -> None:
    Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValueError("image must be JPEG, PNG, or WebP")
    with Image.open(path) as image:
        if image.width * image.height > MAX_IMAGE_PIXELS:
            raise ValueError(f"image exceeds the {MAX_IMAGE_PIXELS} pixel limit")
        image.verify()


def configure_torch_native_overrides() -> str:
    try:
        from torch._native.registry import deregister_op_overrides
    except ImportError:
        return "unavailable"
    deregister_op_overrides(disable_dsl_names="triton")
    return "triton-disabled"


def load_runtime(
    model_directory: Path,
    profile: dict[str, Any],
) -> tuple[Any, Any, dict[str, Any]]:
    native_override_status = configure_torch_native_overrides()
    processor = AutoProcessor.from_pretrained(
        str(model_directory), local_files_only=True, trust_remote_code=False
    )
    model_class = SUPPORTED_ADAPTERS[profile["adapter_id"]][1]
    model = model_class.from_pretrained(
        str(model_directory),
        device_map="auto",
        local_files_only=True,
        trust_remote_code=False,
    ).eval()
    raw_device_map = getattr(model, "hf_device_map", None)
    device_map = (
        {str(key): str(value) for key, value in raw_device_map.items()}
        if isinstance(raw_device_map, dict)
        else {"primary": str(model.device)}
    )
    runtime = {
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "device_map": device_map,
        "torch_native_overrides": native_override_status,
    }
    return processor, model, runtime


def generate(
    processor: Any,
    model: Any,
    prompt: str,
    image_path: Path | None,
    max_new_tokens: int,
) -> str:
    content: list[dict[str, Any]] = []
    if image_path is not None:
        with Image.open(image_path) as source_image:
            normalized_image = source_image.convert("RGB").copy()
        content.append({"type": "image", "image": normalized_image})
    content.append({"type": "text", "text": prompt})
    inputs = processor.apply_chat_template(
        [{"role": "user", "content": content}],
        add_generation_prompt=True,
        enable_thinking=False,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)
    input_length = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        output_ids = model.generate(
            **inputs, do_sample=False, max_new_tokens=max_new_tokens
        )
    return processor.decode(
        output_ids[0][input_length:], skip_special_tokens=True
    ).strip()


def parse_json_object(raw: str) -> dict[str, Any]:
    candidate = raw.strip()
    if candidate.startswith("```"):
        lines = candidate.splitlines()
        if lines and lines[-1].strip() == "```":
            candidate = "\n".join(lines[1:-1]).strip()
    parsed = json.loads(candidate)
    if not isinstance(parsed, dict):
        raise ValueError("model output must be a JSON object")
    return parsed


def require_exact_keys(value: dict[str, Any], keys: set[str]) -> None:
    if set(value) != keys:
        raise ValueError(
            f"unexpected JSON keys: expected {sorted(keys)}, got {sorted(value)}"
        )


def load_label_definitions(
    path: Path, allowed_labels: list[str], max_chars: int
) -> dict[str, str]:
    raw = read_text(path, max_chars)
    parsed = json.loads(raw)
    if not isinstance(parsed, dict) or set(parsed) != set(allowed_labels):
        raise ValueError("label definition keys must exactly match --labels")
    if any(
        not isinstance(value, str) or not value.strip() for value in parsed.values()
    ):
        raise ValueError("every label definition must be a non-empty string")
    return {label: parsed[label].strip() for label in allowed_labels}


def build_prompt(args: argparse.Namespace) -> tuple[str, Path | None]:
    if args.command in {"extract", "classify", "summarize"}:
        source = read_text(args.input, args.max_input_chars)
        args.source_text = source
        source_block = f"<SOURCE>\n{source}\n</SOURCE>"
        if args.command == "extract":
            fields = [
                field.strip() for field in args.fields.split(",") if field.strip()
            ]
            if not fields:
                raise ValueError("--fields must contain at least one field")
            args.expected_fields = fields
            schema = {field: "string|null" for field in fields}
            return (
                "Extract only explicitly stated values from SOURCE. Return one JSON "
                f"object with exactly these fields: {json.dumps(schema)}. "
                "Use null when "
                f"absent or uncertain. Do not infer.\n{source_block}",
                None,
            )
        if args.command == "classify":
            args.allowed_labels = list(dict.fromkeys(args.labels))
            definitions = None
            if getattr(args, "label_definitions", None) is not None:
                definitions = load_label_definitions(
                    args.label_definitions,
                    args.allowed_labels,
                    args.max_input_chars,
                )
            policy = (
                f" Label definitions: {json.dumps(definitions)}."
                if definitions is not None
                else ""
            )
            return (
                "Classify SOURCE into exactly one allowed label. Return JSON only as "
                '{"label": string|null, "evidence": [string], "uncertain": boolean}. '
                f"Allowed labels: {json.dumps(args.allowed_labels)}.{policy} "
                "Evidence must quote "
                f"short exact spans. Abstain when insufficient.\n{source_block}",
                None,
            )
        return (
            "Summarize SOURCE without adding facts. Return JSON only as "
            '{"summary": string, "evidence": [string], "uncertain": boolean}. '
            f"Keep summary within {args.summary_chars} characters and quote exact "
            "evidence.\n"
            f"{source_block}",
            None,
        )

    verify_image(args.image)
    if args.command == "inspect":
        return (
            f"Question: {args.question}\nAnswer only from visible image evidence. "
            "Return "
            'JSON only as {"answer": string|null, "evidence": [string], '
            '"uncertain": boolean}. Abstain when insufficient.',
            args.image,
        )
    if args.command == "ocr":
        return (
            "Transcribe only visible text in reading order. Return JSON only as "
            '{"text": string, "uncertain": boolean}. Do not reconstruct '
            "unreadable text.",
            args.image,
        )
    if args.command == "locate":
        return (
            f"Locate this target: {args.target}. Return JSON only as "
            '{"bbox": [x1,y1,x2,y2]|null, "uncertain": boolean}. Coordinates are '
            "integers from 0 to 1000 with a top-left origin. Abstain when uncertain.",
            args.image,
        )
    raise AssertionError(f"unhandled command: {args.command}")


def validate_result(args: argparse.Namespace, result: dict[str, Any]) -> None:
    if args.command == "extract":
        require_exact_keys(result, set(args.expected_fields))
        if any(
            value is not None and not isinstance(value, str)
            for value in result.values()
        ):
            raise ValueError("extract values must be strings or null")
        return
    expected = {
        "classify": {"label", "evidence", "uncertain"},
        "summarize": {"summary", "evidence", "uncertain"},
        "inspect": {"answer", "evidence", "uncertain"},
        "ocr": {"text", "uncertain"},
        "locate": {"bbox", "uncertain"},
    }[args.command]
    require_exact_keys(result, expected)
    if not isinstance(result["uncertain"], bool):
        raise ValueError("uncertain must be a boolean")
    if "evidence" in result and not (
        isinstance(result["evidence"], list)
        and all(
            isinstance(item, str) and bool(item.strip()) for item in result["evidence"]
        )
    ):
        raise ValueError("evidence must be a list of non-empty strings")
    if args.command == "classify":
        if result["label"] is not None and result["label"] not in args.allowed_labels:
            raise ValueError("label is not in --labels")
        if result["label"] is None and result["uncertain"] is not True:
            raise ValueError("null label requires uncertain true")
        if result["label"] is not None and not result["evidence"]:
            raise ValueError("non-null label requires at least one evidence span")
    elif args.command == "summarize":
        if (
            not isinstance(result["summary"], str)
            or len(result["summary"]) > args.summary_chars
        ):
            raise ValueError("summary is invalid or exceeds --summary-chars")
        if result["summary"] and not result["evidence"]:
            raise ValueError("non-empty summary requires at least one evidence span")
    elif args.command == "inspect":
        if result["answer"] is not None and not isinstance(result["answer"], str):
            raise ValueError("answer must be a string or null")
        if result["answer"] is None and result["uncertain"] is not True:
            raise ValueError("null answer requires uncertain true")
    elif args.command == "ocr" and not isinstance(result["text"], str):
        raise ValueError("text must be a string")
    elif args.command == "locate":
        bbox = result["bbox"]
        valid = bbox is None or (
            isinstance(bbox, list)
            and len(bbox) == 4
            and all(
                isinstance(item, int) and not isinstance(item, bool) for item in bbox
            )
            and all(0 <= item <= 1000 for item in bbox)
            and bbox[0] < bbox[2]
            and bbox[1] < bbox[3]
        )
        if not valid or (bbox is None and result["uncertain"] is not True):
            raise ValueError("bbox must be valid coordinates or an uncertain null")
    if args.command in {"classify", "summarize"} and any(
        evidence not in args.source_text for evidence in result["evidence"]
    ):
        raise ValueError("every evidence item must be an exact source span")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--profile-sha256", required=True)
    parser.add_argument("--model-directory", type=Path, required=True)
    parser.add_argument("--max-new-tokens", type=int, default=DEFAULT_MAX_NEW_TOKENS)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("extract", "classify", "summarize"):
        command = subparsers.add_parser(name)
        command.add_argument("--input", type=existing_file, required=True)
        command.add_argument(
            "--max-input-chars", type=int, default=DEFAULT_MAX_INPUT_CHARS
        )
    subparsers.choices["extract"].add_argument("--fields", required=True)
    subparsers.choices["classify"].add_argument("--labels", nargs="+", required=True)
    subparsers.choices["classify"].add_argument(
        "--label-definitions", type=existing_file
    )
    subparsers.choices["summarize"].add_argument(
        "--summary-chars", type=int, default=800
    )
    batch = subparsers.add_parser("classify-batch")
    batch.add_argument("--input-directory", type=Path, required=True)
    batch.add_argument("--glob", default="*.txt")
    batch.add_argument("--max-files", type=int, default=10_000)
    batch.add_argument("--labels", nargs="+", required=True)
    batch.add_argument("--label-definitions", type=existing_file)
    batch.add_argument("--max-input-chars", type=int, default=DEFAULT_MAX_INPUT_CHARS)
    for name in ("inspect", "ocr", "locate"):
        subparsers.add_parser(name).add_argument(
            "--image", type=existing_file, required=True
        )
    subparsers.choices["inspect"].add_argument("--question", required=True)
    subparsers.choices["locate"].add_argument("--target", required=True)
    return parser


def discover_batch_inputs(args: argparse.Namespace) -> list[Path]:
    directory = args.input_directory.expanduser().resolve(strict=True)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"input directory is missing or unsafe: {directory}")
    pattern = Path(args.glob)
    if (
        pattern.is_absolute()
        or ".." in pattern.parts
        or len(pattern.parts) != 1
        or "**" in args.glob
    ):
        raise ValueError("--glob must be a non-recursive filename pattern")
    if args.max_files <= 0:
        raise ValueError("--max-files must be positive")
    files = []
    for path in directory.glob(args.glob):
        if path.is_file() and not path.is_symlink():
            files.append(path)
            if len(files) > args.max_files:
                raise ValueError(f"batch has more than the {args.max_files} file limit")
    files.sort()
    if not files:
        raise ValueError("batch input set is empty")
    return files


def batch_input_id(path: Path, directory: Path) -> str:
    resolved_directory = directory.expanduser().resolve(strict=True)
    resolved_path = path.expanduser().resolve(strict=True)
    try:
        return resolved_path.relative_to(resolved_directory).as_posix()
    except ValueError as error:
        raise ValueError("batch input escaped --input-directory") from error


def run_task(
    args: argparse.Namespace,
    processor: Any,
    model: Any,
    metadata_base: dict[str, Any],
) -> int:
    prompt, image_path = build_prompt(args)
    input_path = image_path if image_path is not None else args.input
    metadata = {
        **metadata_base,
        "input_id": getattr(args, "input_id", input_path.name),
        "input_sha256": sha256_file(input_path),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "generation": {"do_sample": False, "max_new_tokens": args.max_new_tokens},
    }
    if getattr(args, "label_definitions", None) is not None:
        metadata["label_definitions_sha256"] = sha256_file(args.label_definitions)
    try:
        raw = generate(processor, model, prompt, image_path, args.max_new_tokens)
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "error", **metadata, "error": str(error)}))
        return 1
    try:
        result = parse_json_object(raw)
        validate_result(args, result)
    except (json.JSONDecodeError, ValueError) as error:
        print(
            json.dumps(
                {"status": "invalid", **metadata, "error": str(error), "raw": raw}
            )
        )
        return 2
    print(
        json.dumps({"status": "ok", **metadata, "result": result}, ensure_ascii=False)
    )
    return 0


def run_batch(
    args: argparse.Namespace,
    processor: Any,
    model: Any,
    metadata_base: dict[str, Any],
) -> int:
    statuses = []
    batch_directory = args.input_directory.expanduser().resolve(strict=True)
    for input_path in discover_batch_inputs(args):
        task_args = argparse.Namespace(**vars(args))
        task_args.command = "classify"
        task_args.input = input_path
        task_args.input_id = batch_input_id(input_path, batch_directory)
        try:
            statuses.append(run_task(task_args, processor, model, metadata_base))
        except (OSError, RuntimeError, ValueError) as error:
            try:
                input_sha256 = sha256_file(input_path)
            except OSError:
                input_sha256 = None
            print(
                json.dumps(
                    {
                        "status": "error",
                        **metadata_base,
                        "input_id": task_args.input_id,
                        "input_sha256": input_sha256,
                        "prompt_sha256": None,
                        "generation": {
                            "do_sample": False,
                            "max_new_tokens": args.max_new_tokens,
                        },
                        "error": str(error),
                    }
                )
            )
            statuses.append(1)
    return max(statuses)


def main() -> int:
    args = build_parser().parse_args()
    if args.max_new_tokens <= 0:
        raise ValueError("--max-new-tokens must be positive")
    profile = load_profile(
        args.profile.expanduser().resolve(strict=True), args.profile_sha256
    )
    model_directory = args.model_directory.expanduser().resolve(strict=True)
    manifest, manifest_sha256 = verify_model_bundle(
        model_directory, profile, args.profile_sha256
    )
    processor, model, runtime = load_runtime(model_directory, profile)
    metadata_base = {
        "profile_id": profile["profile_id"],
        "profile_sha256": args.profile_sha256,
        "model_id": manifest["model_id"],
        "revision": manifest["revision"],
        "adapter_id": manifest["adapter_id"],
        "model_manifest_sha256": manifest_sha256,
        "runtime": runtime,
    }
    if args.command != "classify-batch":
        return run_task(args, processor, model, metadata_base)
    return run_batch(args, processor, model, metadata_base)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        raise SystemExit(1) from error
