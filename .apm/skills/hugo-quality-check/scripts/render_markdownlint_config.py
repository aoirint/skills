"""Render the Hugo markdownlint config from the shared prose baseline."""

import argparse
from pathlib import Path

IGNORE_ANCHOR = '  - ".agents/**"\n'
HUGO_IGNORE = (
    "\n"
    "  # Hugo's default public directory is generated output, not site-owned prose.\n"
    '  - "public/**"\n'
)


def render(source: Path) -> str:
    """Return the baseline with the documented Hugo output exclusion."""
    baseline = source.read_text(encoding="utf-8")
    if baseline.count(IGNORE_ANCHOR) != 1:
        raise ValueError("expected exactly one .agents ignore anchor")
    return baseline.replace(IGNORE_ANCHOR, IGNORE_ANCHOR + HUGO_IGNORE)


def main() -> int:
    """Render the asset, or report whether the committed asset is current."""
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    rendered = render(args.source)
    if args.check:
        return 0 if args.output.read_text(encoding="utf-8") == rendered else 1

    args.output.write_text(rendered, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
