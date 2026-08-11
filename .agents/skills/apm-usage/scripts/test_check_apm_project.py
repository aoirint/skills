"""Tests for the repository-owned APM metadata guard template."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import ModuleType


def load_guard() -> ModuleType:
    """Load the asset script without making the asset directory a package."""
    path = (
        Path(__file__).parents[1]
        / "assets"
        / "check-apm-project"
        / "check_apm_project.py"
    )
    spec = importlib.util.spec_from_file_location("check_apm_project", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUARD = load_guard()


class CheckApmProjectTests(unittest.TestCase):
    """Exercise successful and rejected metadata combinations."""

    def test_validate_versions_accepts_expected_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "apm.yml").write_text("version: 0.0.0\n", encoding="utf-8")
            (root / "apm.lock.yaml").write_text(
                "apm_version: 0.26.0\n", encoding="utf-8"
            )

            errors = GUARD.validate_versions(
                root=root,
                expected_project_version="0.0.0",
                expected_apm_version="0.26.0",
            )

        self.assertEqual(errors, ())

    def test_validate_versions_reports_mismatch_and_ambiguous_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "apm.yml").write_text("version: 1.0.0\n", encoding="utf-8")
            (root / "apm.lock.yaml").write_text(
                "apm_version: 0.26.0\napm_version: 0.26.0\n", encoding="utf-8"
            )

            errors = GUARD.validate_versions(
                root=root,
                expected_project_version="0.0.0",
                expected_apm_version="0.26.0",
            )

        self.assertEqual(len(errors), 2)
        self.assertIn("expected '0.0.0'", errors[0])
        self.assertIn("expected exactly one", errors[1])


if __name__ == "__main__":
    unittest.main()
