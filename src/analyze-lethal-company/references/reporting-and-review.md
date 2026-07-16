# Reporting and review

## Artifact layout

Use `evidence/`, `data/raw/`, `data/intermediate/`, `data/processed/`, `docs/`, `report/`, and `script/`. Keep a source manifest and data dictionary. Store stage certificates where large computations must be sealed.

## Statistical presentation

- Separate finite-population exact descriptions from sample estimates and cross-fit prediction.
- Show support alongside conditional probabilities.
- Keep zero probability distinct from unsupported cells.
- For integer state identification, show modal accuracy and empirical 80%/95% intervals; list every 100% mapping in a machine-readable appendix.
- Keep full-sample 100% descriptions separate from deployable cross-fit rules. Audit support in every training fold and disclose fallback behavior.
- Preserve the full numeric bin grid in heatmaps, including globally unsupported bins as blank cells; never compress observed categories into equal-width numeric-looking columns. Choose adaptive major ticks from numeric bin values with a bounded label count for A4 readability, and state both the cell resolution and tick spacing.
- If seed examples are useful, deterministically select the smallest matching seeds and independently verify minimality.
- Report a baseline, paired improvement, and an uncertainty or stability measure whose interpretation matches the design.

## Closure checks

Generate user-facing text, tables, claims, and captions from one structured source. Independently recompute headline claims from canonical data. Verify HTML visible-text closure, PDF text inclusion, forbidden runtime assertions, figure set/hash closure, A4 portrait geometry, and evidence links.

For no-clobber pipelines, document full clean reruns separately from report-only and analysis-only rebuilds. Name every generated path that must be archived, keep prior runs by move rather than deletion, and link the reproduction guide and data dictionary from the report artifact table.

Render all PDF pages with a pinned renderer. Inspect every page for clipping, overflow, unreadable labels, misleading axes, broken glyphs, and blank pages. Record page and contact-sheet hashes in visual QA evidence.

Give blank reviewers raw artifacts and the task, not intended conclusions. Require actionable findings. After each correction, rerun affected computations and request another pass until no useful issue remains.
