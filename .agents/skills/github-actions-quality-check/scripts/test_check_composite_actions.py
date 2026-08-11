from __future__ import annotations

import importlib.util
import io
import runpy
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import ModuleType


def _load_module() -> ModuleType:
    path = Path(__file__).with_name("check_composite_actions.py")
    spec = importlib.util.spec_from_file_location("check_composite_actions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Composite Action checker.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = _load_module()


class CompositeActionCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.skills_root = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_action(
        self,
        skill: str,
        action: str,
        content: str,
        *,
        script: str | None = None,
    ) -> Path:
        action_directory = (
            self.skills_root / skill / "assets" / "github" / "actions" / action
        )
        action_directory.mkdir(parents=True)
        (action_directory / "action.yml").write_text(content, encoding="utf-8")
        if script is not None:
            (action_directory / "run.sh").write_text(script, encoding="utf-8")
        return action_directory

    def test_valid_composed_actions(self) -> None:
        self.write_action(
            "node-quality-check",
            "setup-node-locked",
            "name: Set up locked Node environment\nruns:\n  using: composite\n  steps: []\n",
        )
        self.write_action(
            "hugo-quality-check",
            "check-hugo-site",
            """name: Check Hugo web site
runs:
  using: composite
  steps:
    - id: setup
      uses: ./.github/actions/setup-node-locked
    - if: always() && steps.setup.outputs.dependency-tree-owned == 'true'
      shell: bash
      run: rm -rf node_modules
""",
        )

        self.assertEqual(CHECKER.validate_composite_actions(self.skills_root), [])

    def test_reports_path_name_lifecycle_and_retired_reference(self) -> None:
        self.write_action(
            "first-skill",
            "check-source",
            """name: Check
runs:
  using: composite
  steps:
    - uses: ./.github/actions/setup-python-locked
    - uses: ./.github/actions/check-source
""",
        )

        errors = CHECKER.validate_composite_actions(self.skills_root)

        self.assertTrue(
            any(error.startswith("invalid action path:") for error in errors)
        )
        self.assertTrue(
            any(error.startswith("ambiguous action name:") for error in errors)
        )
        self.assertTrue(
            any(error.startswith("retired local-action path:") for error in errors)
        )
        self.assertTrue(
            any(
                error.startswith("missing ownership-gated cleanup:") for error in errors
            )
        )

    def test_reports_duplicate_action_path_and_cross_skill_asset(self) -> None:
        shared_script = "#!/usr/bin/env bash\necho shared\n"
        self.write_action(
            "first-skill",
            "check-node-source",
            "name: Check Node source\nruns:\n  using: composite\n  steps: []\n",
            script=shared_script,
        )
        self.write_action(
            "second-skill",
            "check-node-source",
            "name: Check Node package\nruns:\n  using: composite\n  steps: []\n",
            script=shared_script,
        )

        errors = CHECKER.validate_composite_actions(self.skills_root)

        self.assertTrue(
            any(
                error.startswith("duplicate action path check-node-source:")
                for error in errors
            )
        )
        self.assertTrue(
            any(
                error.startswith("duplicate cross-Skill action asset:")
                for error in errors
            )
        )

    def test_empty_action_is_ambiguous(self) -> None:
        self.write_action("empty-skill", "check-empty-source", "")

        self.assertEqual(
            CHECKER.validate_composite_actions(self.skills_root),
            [
                "ambiguous action name: "
                + str(
                    Path(
                        "empty-skill/assets/github/actions/check-empty-source/action.yml"
                    )
                )
            ],
        )

    def test_main_reports_success_and_failure(self) -> None:
        self.write_action(
            "valid-skill",
            "check-valid-source",
            "name: Check valid source\nruns:\n  using: composite\n  steps: []\n",
        )
        output = io.StringIO()
        with redirect_stdout(output):
            success = CHECKER.main([str(self.skills_root)])
        self.assertEqual(success, 0)
        self.assertEqual(output.getvalue(), "Composite Action contracts are valid.\n")

        self.write_action("invalid-skill", "invalid", "name: Check invalid source\n")
        output = io.StringIO()
        with redirect_stdout(output):
            failure = CHECKER.main([str(self.skills_root)])
        self.assertEqual(failure, 1)
        self.assertIn("invalid action path:", output.getvalue())

    def test_script_entry_point(self) -> None:
        self.write_action(
            "valid-skill",
            "check-valid-source",
            "name: Check valid source\nruns:\n  using: composite\n  steps: []\n",
        )
        script_path = Path(__file__).with_name("check_composite_actions.py")
        original_argv = sys.argv
        output = io.StringIO()
        try:
            sys.argv = [str(script_path), str(self.skills_root)]
            with redirect_stdout(output), self.assertRaisesRegex(SystemExit, "0"):
                runpy.run_path(str(script_path), run_name="__main__")
        finally:
            sys.argv = original_argv
        self.assertEqual(output.getvalue(), "Composite Action contracts are valid.\n")


if __name__ == "__main__":
    unittest.main()
