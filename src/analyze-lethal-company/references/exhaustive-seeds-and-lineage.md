# Exhaustive seeds and lineage

## Full-population contract

Freeze the inclusive seed domain, every declared population/comparison stratum, endpoint identities, scenario identities, canonical record encoding, and reduction order before production. For a claimed full enumeration:

- partition the domain into canonical disjoint half-open chunks;
- prove their union equals the declared domain with no gaps, overlaps, duplicates, or out-of-range seeds;
- store per-chunk and per declared population/comparison stratum (for example moon, level, profile, or build) contribution counts and ordered record digests, plus type-appropriate exact invariants: integer minima/maxima/sums/squared sums/XOR where meaningful, categorical contingencies, or canonical structured-record checks;
- compute a parent digest from the ordered chunk identities and digests;
- require reducer totals to equal worker totals and the expected population contribution count.

Use a second implementation that imports no production computational or canonical-encoding modules; share only frozen semantic/source inputs plus declarative contracts and schemas. Do not read production-derived intermediates, canonical records, contingencies, reducer outputs, or digests until the complete-domain independent phase is sealed. A chunk-interleaved loop that computes one expectation and immediately opens its production counterpart is not this two-phase protocol. Regenerate complete-domain results, type-appropriate invariants, and canonical digests independently; then use a second pass (recomputing chunks if necessary) for production comparison. Independently reproduce every declared reducer estimand and every reported metric/model row, not only raw-record equality or headline MAE. Make it reject targeted mutations such as seed offsets, serialized entry order, branch timing, draw counts, float precision, truncation, curve behavior, applicability rules, record encoding, or reduction order. A sample or prefix can validate performance but cannot certify coverage.

For weighted selection, freeze the entire edge path, not just the ordinary cumulative-probability loop: binary precision of the random target, division and accumulator precision, comparison inclusivity, treatment of nonpositive weights, and the decompiled fallback after cumulative rounding. If the game consumes another RNG draw when no cumulative bin reaches the target, the independent verifier must do the same. Include a fixture that actually reaches this fallback; otherwise a verifier can agree on common rows while shifting every later draw in the rare boundary row.

## Deterministic mappings and witnesses

Freeze the mapping universe in the endpoint contract, including every declared dimension that belongs to the estimand (for example moon, build, level, endpoint, type, interior, profile, or counterfactual scenario). Do not silently narrow “all mappings” to a headline scenario; if the report shows a headline subset, link the complete-universe table explicitly.

Derive a 100% mapping only from a complete-domain proof, such as an exhaustive finite-population contingency or an independently checked algebraic/formal derivation, never from cross-fit predictions. Check bidirectional closure over the declared mapping universe:

1. supported singleton cells minus emitted mappings is empty;
2. emitted mappings minus supported singleton cells is empty.

For every emitted mapping, use the complete-domain proof to verify contribution/cell support and distinct population-unit support; also verify distinct-seed support when seed is a separate clustering or witness unit. Report differing values or explicitly certify their equality. When seed witnesses are requested, attach the numerically smallest `min(requested count, distinct-seed support)` distinct seeds; use a requested count of three when the user asks for examples but gives no count. Disclose mappings whose distinct-seed support cannot supply the requested count instead of omitting them or duplicating seeds. Use an implementation-isolated scalar verifier to rescan from the domain minimum through the last witness when the requested count is fulfilled, recomputing mapping identity, output, applicability, and witness ordering to prove minimality. Audit the scalar entry point's transitive call closure from parsed source (or an equivalently enforceable dependency graph), reject production/chunk RNG and canonical-encoding helpers, seal the audit digest, and include a forbidden-call mutation fixture; a fixed `isolated: true` field is not an audit. For shortage cases, scan through the domain maximum and additionally confirm total distinct-seed support. Include actual-runtime mappings only when runtime correspondence, applicability, execution path, and every runtime-dependent input are established over the mapping's complete declared domain under the evidence policy's promotion boundary.

## Immutable stages

Separate semantic inputs, production certificates, processed analysis, report/media, and handoff into content-addressed stages. Bind every stage to its parent hash and artifact byte hashes. Revalidate parent artifacts before sealing a child. Keep failed or superseded attempts by rename; never overwrite a sealed run.

A handoff seal also needs a receiver-side, read-only verification mode. Recompute the seal self-hash, stage hashes and parent links, then rehash every directly and indirectly enumerated artifact from the bytes being received (including partition sidecars and resumable bundles). Internal JSON self-consistency alone does not prove that the referenced artifact bytes still exist or are unchanged, and is insufficient evidence for report-only ancestry.

Reserve canonical phase-seal and final-certificate paths for complete-domain production PASS runs. A prefix, mutation check, or independent-only diagnostic must require an explicit non-production output path and must be rejected before expensive scanning if it targets a canonical proof path.

Document three reproduction modes when applicable:

- a clean full run from a new semantic seal;
- an extension-only run against an unchanged sealed parent;
- a report-only rebuild against unchanged numeric parents.

## Additive work after a sealed run

Do not make changed live files appear to have belonged to the old run. Choose one of two paths:

- require a new semantic seal and full rerun when population definitions, core endpoint meaning, frozen game inputs, RNG mechanics, enumeration code, or core analysis logic changed;
- create a separately sealed additive extension when the old numeric artifacts remain byte-identical and the new endpoint can be enumerated independently.

For an additive extension, create a machine-readable overlay that binds the old semantic/certificate/analysis hashes and lists every superseded sealed path with its old hash, accepted new hash, role, and reason. Also hash every new contract, evidence file, script, lock, completion certificate, independent verifier, processed output, and review artifact. Fail if:

- a changed base path is undeclared;
- an overlay old hash differs from the base seal;
- a current or archived new hash differs from the overlay;
- an undeclared core computational input changed;
- a downstream stage omits the overlay or any required extension parent.

Avoid both extremes of recursive live-path verification: rejecting a legitimate declared extension because a report document changed, or blanket-skipping changed paths and allowing later drift. Compare unchanged base paths to the base seal, declared changed paths to exact overlay old/new pairs, and new paths to the extension allowlist. Seal the overlay into the final report and handoff chain.
