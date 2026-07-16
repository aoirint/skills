---
name: analyze-lethal-company
description: Analyze version-specific Lethal Company mechanics from decompiled assemblies, Unity assets, seeded RNG, and runtime observations, then produce reproducible evidence-backed reports. Use for mechanics investigations, seed enumeration, code/asset reconciliation, Terminal or HUD behavior, version comparisons, statistical prediction, or when code defaults may be overridden by serialized assets.
---

# Analyze Lethal Company

## Establish scope

1. Record the exact game version, Steam manifest/build identifier, platform, mod state, source paths, and evidence date.
2. Inventory and hash the assembly/decompilation and asset roots before drawing conclusions. Run `scripts/inventory_build.py` when a stable file manifest is useful.
3. Keep evidence from different builds in separate inventories. Analyze each build independently before comparing them.

## Build the evidence model

1. Start from the user-visible behavior and trace it through the entrypoint, call path, fields, and referenced assets.
2. Search both code and serialized assets. Treat a serialized scene/prefab/ScriptableObject value as authoritative when it overrides a C# initializer.
3. Record claim-level locators and hashes. Classify each claim as direct static evidence, deterministic derivation, counterfactual model, runtime observation, or unknown.
4. Read [evidence-policy.md](references/evidence-policy.md) before designing the evidence ledger or resolving conflicting sources.
5. Read [unity-and-rng.md](references/unity-and-rng.md) when the mechanic uses Unity serialization, `System.Random`, `UnityEngine.Random`, object enumeration, spawning, NavMesh, networking, or synchronization.

## Define endpoints before computation

1. Write a machine-readable endpoint contract before production.
2. Separate actual runtime endpoints from exact static/RNG endpoints and from analytic or counterfactual proxies. Never fill an unknown runtime endpoint with a proxy.
3. Define the population key, observation window, inclusion/exclusion predicates, units, rounding, thresholds, and applicability for every endpoint.
4. Name proxies by what they compute. Put `proxy`, `counterfactual`, or `static` in tables, captions, and artifact schemas.
5. Freeze analysis thresholds, binning, tie rules, sparse-cell fallbacks, folds, metrics, and uncertainty interpretation before inspecting production outcomes.

## Compute reproducibly

1. Prefer Python scripts with PEP 723 metadata. Set `[tool.uv] exclude-newer = "P7D"`, pin dependencies, and generate an adjacent uv lockfile.
2. Preserve source artifacts and prior runs. Use no-clobber outputs and archive by rename instead of overwriting.
3. For full seed enumeration, prove endpoints, gaps, overlaps, duplicates, integer moments, per-moon contribution counts, and parent hashes. Do not call a prefix or convenience sample “all seeds.”
4. When full item-level enumeration is infeasible, use a frozen domain-separated hash sample shared across moons and disclose the sampling assumption. Never downgrade a runtime-unknown endpoint into a sampled “actual” endpoint.
5. Reimplement fragile RNG logic independently. Test exclusive maxima, float32 accumulation, integer truncation, offsets, event branches, serialized multipliers, and RNG consumption order with mutation fixtures.
6. Keep training/test partitions at the seed level across all moons and variants. Fit bins, probabilities, modes, medians, intervals, sparse support, and fallbacks on training data only.

## Report and validate

1. Read [reporting-and-review.md](references/reporting-and-review.md) before building a formal HTML/PDF report.
2. State what can and cannot be inferred near every gameplay-facing result.
3. Prefer conditional heatmaps, support panels, and 80%/95%/100% certainty views over generic box plots when the question is state identification.
4. Generate HTML and A4 portrait PDF from one narrative/claim source. Verify claims and figure hashes independently, render every PDF page, and inspect all pages.
5. Ask a blank-context reviewer to challenge the plan before production and the report after production when the task warrants high assurance. Iterate until no useful correction remains.
6. Preserve scripts, locks, evidence, raw/intermediate/processed data, review records, and reproduction commands with the deliverable.
