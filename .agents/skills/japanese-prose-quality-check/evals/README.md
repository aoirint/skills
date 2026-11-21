# Japanese Prose Quality Check: Evaluation

These cases compare how instructions shape a rewrite, not whether an editor
reproduces one preferred wording.

1. In [evals.json](evals.json), select a case. Give a fresh editor one skill
   version, the prompt, and the listed input file only. Keep the prompt
   and material the same across versions. Do not give the editor the
   manifest, expected output, review notes, or example prose.
2. Give an independent reader the packet and anonymized drafts. Reverse the order
   for a second reader when possible. Check the facts and constraints before
   comparing the writing. Record any consequential factual change separately.
3. Compare the complete drafts. Note where the opening, section order or headings
   help the reader, and where the phrasing or transitions make a passage read
   naturally as Japanese. Point to actual passages, including any advantage of
   the weaker draft. Record a tie if there is no clear preference.

Do not reward a version merely for being shorter, adding warnings or using a
particular heading. The suggested edit shows one possible result; it is not a
template or a scoring key.

- Investigation comment: [input](investigation-comment/input.md), [review](investigation-comment/review.md).
- Feature request: [input](feature-request/input.md), [review](feature-request/review.md).

Keep evals separate from normal use of the skill. If an editor can inspect
the skill directory, test from a copy without its evals directory and
supply the listed input files at the paths used in the prompt. Keep run
outputs and comparisons outside the skill, in a sibling workspace.

See the [Agent Skills evaluation guide](https://agentskills.io/skill-creation/evaluating-skills)
for the case manifest and workspace layout.

## Comparable writing

- [A short feature request](https://github.com/aoirint/ffmpeg-docker/issues/28)
  starts with the symptom and relevant context, then proposes a fix. It does
  not need the same headings as the request case above.
- [A field investigation](https://github.com/aoirint/impostor-compose-template/issues/5#issuecomment-1372822571)
  states the Docker setup before grouping evidence and giving a concrete
  check. The [README follow-up](https://github.com/aoirint/impostor-compose-template/pull/7)
  serves a different audience: it keeps the usable result, not the full log.

These show why the genre and audience matter more than reproducing a house
template. They are reference material for reviewers, not additional editor
inputs.
