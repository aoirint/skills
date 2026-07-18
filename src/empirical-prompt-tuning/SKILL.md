---
name: empirical-prompt-tuning
description: >-
  Empirically improve agent-facing instructions through fresh-executor scenario
  tests and measured iterations. Use only when explicitly asked to evaluate a
  prompt, skill, slash command, CLAUDE.md, or code-generation instruction;
  do not invoke automatically after ordinary edits.
---

# Empirical Prompt Tuning

Use this operator-triggered workflow to find instruction ambiguity with a fresh executor. Do not
replace executor evaluation with a self-review.

## Goals

- Measure whether an instruction produces the required outcome in realistic cases.
- Separate instruction defects from missing inputs and executor mistakes.
- Make the smallest traceable fix, then retest with a fresh executor.
- Stop at convergence, divergence, or an explicit resource cutoff.

## Workflow

1. Confirm that fresh subagent dispatch is available. If it is unavailable, do not apply this
   skill; report that empirical evaluation was skipped and suggest an independent session.
2. Perform Iteration 0 before dispatching:
   - Compare the frontmatter description's promises with the body’s actual scope.
   - Reconcile any mismatch in the target instruction.
3. Prepare two or three realistic scenarios before editing the target:
   - Include one median case and at least one edge or out-of-scope case.
   - Write three to seven fixed requirements per scenario, including at least one `[critical]`
     requirement. Do not change the checklist or critical tags after evaluation starts.
4. Dispatch one fresh, blank-slate executor per scenario. Give it the complete target instruction,
   scenario, fixed checklist, and the report contract below. Do not reveal suspected defects,
   intended fixes, or expected answers.
5. Evaluate both the deliverable and the executor report:
   - Mark success only when every `[critical]` requirement passes.
   - Calculate accuracy from the fixed checklist: pass = 1, partial = 0.5, fail = 0.
   - Record tool uses, duration, retries, unclear points, discretionary fill-ins, and the weak
     phase. Treat qualitative findings as primary; use metrics for comparison, not as the goal.
   - State which critical item failed when a scenario fails.
6. Maintain a per-target failure-pattern ledger. For each unclear point, record `Issue`, `Cause`,
   and a class-level `General Fix Rule`. Reuse and diagnose an existing pattern before adding one.
7. Before changing the instruction, name the exact checklist wording the change is intended to
   satisfy. Apply one related theme of minimal fixes, then rerun the same scenarios with new
   executors. Never reuse an executor.
8. Stop after two consecutive rounds with no new unclear points, accuracy improvement of at most
   three points, tool-use variation within 10%, and duration variation within 15%. Use three rounds
   for high-importance prompts. Add one hold-out scenario at convergence; if accuracy drops 15
   points or more from the recent average, redesign the scenarios and continue.
9. Treat three or more rounds without fewer unclear points as divergence. Stop patching and revise
   the target structure. Stop earlier only for a stated resource cutoff.

## Executor Contract

Ask each executor to return:

```text
- Deliverable: <artifact or execution summary>
- Requirement achievement: pass / fail / partial for each checklist item, with reasons
- Trace: all OK, or Understanding / Planning / Execution / Formatting with stuck or skipped reasons
- Unclear points: Issue / Cause / General Fix Rule for each finding
- Discretionary fill-ins: <bullets>
- Retries: <count and reason>
```

Use structural-review mode only for description/body consistency checks. It supports empirical
testing but does not count toward convergence.

## Report

For each iteration, report the changes, one row per scenario (success, accuracy, steps, duration,
retries, and weak phase), new structured findings, ledger updates, and the next minimal fix.

## Guardrails

- Do not tune scenarios to make a proposed fix look successful.
- Do not judge variants by preference. Compare fixed-checklist accuracy, unclear-point count, tool
  uses, and weak phases; use two independent orderings only if qualitative comparison is necessary.
- Use variant exploration only after a plateau. Keep the higher-accuracy variant; break ties with
  fewer unclear points, then fewer tool uses.
- Do not call a one-scenario pass or a self-reread empirical validation.
