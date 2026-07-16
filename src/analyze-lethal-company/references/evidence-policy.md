# Evidence policy

## Source order

Prefer sources in this order while preserving conflicts:

1. Runtime observation from a frozen, reproducible build and observation protocol.
2. Build-local decompiled code plus the serialized assets it references.
3. Build-local code or assets alone.
4. Official version notes.
5. Prior local analyses with source hashes.
6. Community material as a lead, not final proof.

Do not let a higher-ranked source erase a conflict. Explain why the sources describe different phases, clients, versions, or object sets.

## Claim classes

- `direct_static`: explicit in target-build code or serialized data.
- `exact_derived`: deterministic result whose complete finite population and implementation are verified.
- `counterfactual_model`: deterministic under stated assumptions that differ from runtime.
- `sample_estimate`: estimate from a frozen sample; record design and uncertainty meaning.
- `runtime_observed`: measured under a named profile/window.
- `unknown_runtime`: required runtime state is absent.

## Evidence ledger fields

Record claim ID, statement, build, class, source path, locator, source hash, derivation artifact, population key, endpoint status, and caveat. Use absolute paths only in source manifests; use workspace-relative frozen paths in portable reports.

## Conflict checks

- Compare C# field defaults with scene, prefab, and ScriptableObject serialization.
- Distinguish code presence from reachability and execution.
- Distinguish host state, client state, pre-sync state, and post-sync state.
- Distinguish planned objects from successfully spawned and active objects.
- Keep HUD, Terminal, server totals, quota values, and item `scrapValue` as separate endpoints unless code proves equality.
