# Reporting and review

## Artifact layout

Use `evidence/`, `data/raw/`, `data/intermediate/`, `data/processed/`, `docs/`, `report/`, and `script/`. Keep a source manifest and data dictionary. Store stage certificates where large computations must be sealed.

## Statistical presentation

- Separate finite-population exact descriptions from sample estimates and cross-fit prediction.
- Full enumeration removes population-unit sampling uncertainty only. Keep `counterfactual_model` as the evidence class, record enumeration status separately, and preserve runtime/model uncertainty.
- For weighted discrete outcomes, freeze an exact integer nearest-rank rule such as `ceil(q*N)` and report prediction-range coverage. Do not call a fully known finite-population range a confidence interval.
- Show support alongside conditional probabilities.
- Keep zero probability distinct from unsupported cells.
- For integer state identification, show modal accuracy and empirical 80%/95% intervals; list every 100% mapping in a machine-readable appendix.
- Keep full-sample 100% descriptions separate from deployable cross-fit rules. Audit support in every training fold and disclose fallback behavior.
- Preserve the full numeric bin grid in heatmaps, including globally unsupported bins as blank cells; never compress observed categories into equal-width numeric-looking columns. Choose adaptive major ticks from numeric bin values with a bounded label count for A4 readability, and state both the cell resolution and tick spacing.
- Build plotted lines from consecutive supported integer segments. Never connect two supported points across an unsupported integer gap; preserve supported zero as different from unsupported.
- If dense integer panels make exact annotations unreadable at A4 size, split the numeric range into ordered strips or move the values to a table. Do not solve density by shrinking labels below legibility.
- When deterministic mapping witnesses are included, present or explicitly link the complete declared-universe mapping table; never show a headline subset as though it were complete. Apply the witness-selection and minimality rules from the exhaustive-seed reference routed by `SKILL.md`.
- Report a baseline, paired improvement, and an uncertainty or stability measure whose interpretation matches the design.

## Closure checks

Generate user-facing text, tables, claims, and captions from one structured source. Recompute headline claims separately from sealed canonical data as a report-closure check. Do not present this as independent endpoint/computation verification; apply the implementation-isolation rule in `SKILL.md` for that stronger claim. Verify HTML visible-text closure, PDF text inclusion, forbidden runtime assertions, figure set/hash closure, A4 portrait geometry, and evidence links.

For no-clobber pipelines, document full clean reruns separately from report-only and analysis-only rebuilds. Name every generated path that must be archived, keep prior runs by move rather than deletion, and link the reproduction guide and data dictionary from the report artifact table.

For resumable enumeration, embed a generation fingerprint in every part and atomic sidecar. Include the script, adjacent lock, endpoint contract, raw inputs, full schema, scenario/tier definitions, and parent hashes. On resume, recheck types, non-null values, exact key arrays, semantic invariants, part hashes, and the ordered part-root digest; range metadata alone is insufficient.

Render all PDF pages with a pinned renderer. Inspect every page for clipping, overflow, unreadable labels, misleading axes, broken glyphs, blank pages, orphaned captions, and table-header/row splits. Record page and contact-sheet hashes in visual QA evidence.

Treat non-Python report dependencies as semantic inputs too. Record and seal the exact font bytes used for PDF generation and the renderer executable hash plus version; a Python lock does not pin a system font or an arbitrary `PATH` binary. Bind rendered page/contact hashes to that renderer and the source PDF.

Give blank reviewers raw artifacts and the task, not intended conclusions. Require actionable findings. After each correction, rerun affected computations and request another pass until no useful issue remains.
