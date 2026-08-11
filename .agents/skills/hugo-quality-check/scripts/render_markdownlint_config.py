"""Render the Hugo markdownlint config from the shared prose baseline."""

import argparse
from pathlib import Path

GLOB_ANCHOR = '  - "**/*.md"\n'
IGNORE_ANCHOR = '  - ".agents/**"\n'
REPOSITORY_IGNORES = (
    "\n"
    "  # Hugo article source is checked separately with its renderer-aware rules.\n"
    '  - "content/**"\n'
    "\n"
    "  # Hugo's default public directory is generated output, not site-owned prose.\n"
    '  - "public/**"\n'
)
MD041_ANCHOR = "  # PR-template guidance needs to appear before the first visible heading, so\n"
CONTENT_MD033 = (
    "  # Article source may use renderer-owned inline HTML. This exception is\n"
    "  # isolated from repository documentation by the content-only glob above.\n"
    "  MD033: false\n\n"
)


def render_repository(source: Path) -> str:
    """Return repository rules with Hugo content and output excluded."""
    baseline = source.read_text(encoding="utf-8")
    if baseline.count(IGNORE_ANCHOR) != 1:
        raise ValueError("expected exactly one .agents ignore anchor")
    return baseline.replace(IGNORE_ANCHOR, IGNORE_ANCHOR + REPOSITORY_IGNORES)


def render_content(source: Path) -> str:
    """Return prose-baseline rules scoped to Hugo article source."""
    baseline = source.read_text(encoding="utf-8")
    if baseline.count(GLOB_ANCHOR) != 1 or baseline.count(MD041_ANCHOR) != 1:
        raise ValueError("expected prose glob and MD041 comment anchors")
    content = baseline.replace(GLOB_ANCHOR, '  - "content/**/*.md"\n')
    content = content.replace(
        "# Lint every committed Markdown document by default so docs, release notes, and\n"
        "# GitHub templates follow one repository-wide style.\n",
        "# Check Hugo article source separately from repository documentation so\n"
        "# renderer-specific exceptions cannot weaken README or operational prose.\n",
    )
    content = content.replace(MD041_ANCHOR, CONTENT_MD033 + MD041_ANCHOR)
    return content.replace(
        "# PR-template guidance needs to appear before the first visible heading, so\n"
        "# do not require the first line to be an H1.\n",
        "# Front matter and template guidance may appear before the first heading.\n",
    )


def main() -> int:
    """Render the asset, or report whether the committed asset is current."""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("repository_output", type=Path)
    parser.add_argument("content_output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    outputs = {
        args.repository_output: render_repository(args.source),
        args.content_output: render_content(args.source),
    }
    if args.check:
        return int(
            any(path.read_text(encoding="utf-8") != rendered for path, rendered in outputs.items())
        )

    for path, rendered in outputs.items():
        path.write_text(rendered, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
