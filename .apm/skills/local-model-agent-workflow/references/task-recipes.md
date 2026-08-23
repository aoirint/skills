# Task Recipes

Use these recipes only after the delegation gate establishes that direct agent
work and suitable deterministic or classical methods are not the better path,
or when exercising local inference is itself an application requirement.

The runner supplies reusable commands for common bounded tasks. Each emits one
JSON record with provenance and either a validated `result` or an error status.

Use the container invocation from [offline container operation](offline-container.md)
and append one of these command tails.

## Extract named fields

```shell
--model-directory /models extract --input /input/source.txt \
  --fields due_date,owner,status
```

Absent or uncertain values must be `null`. Field names define the exact output
keys.

## Classify into allowed labels

```shell
--model-directory /models classify --input /input/source.txt \
  --labels relevant irrelevant uncertain
```

The validator rejects labels outside the supplied set and requires quoted
evidence spans from the source. `label: null` is an abstention and requires
`uncertain: true`. A non-null label with `uncertain: true` is only a tentative
classification and must be routed to review. If an allowed label itself denotes
review, route it to review regardless of the uncertainty flag.

For multiple files, load the model once with the batch command:

```shell
--model-directory /models classify-batch --input-directory /input \
  --glob '*.txt' --labels keep drop review
```

The runner accepts a non-recursive filename pattern, stops discovery after the
configured limit is exceeded, then processes the accepted set in sorted order.
It emits one JSON record per file. Each record includes an `input_id` relative to
the mounted input directory as well as the content hash, so equal-content files
remain distinguishable.
Redirect JSON Lines output outside the container or to an explicitly writable
output mount.

## Summarize bounded text

```shell
--model-directory /models summarize --input /input/source.txt \
  --summary-chars 600
```

Split long documents at meaningful boundaries instead of raising input limits
without calibration.

## Ask a visual question

```shell
--model-directory /models inspect --image /input/image.png \
  --question 'Which status indicators are visibly active?'
```

Image evidence is not mechanically grounded by the runner. Independently inspect
high-impact answers.

## OCR visible text

```shell
--model-directory /models ocr --image /input/image.png
```

The prompt forbids reconstructing hidden or unreadable text. Calibrate against
the intended image sources and languages.

## Locate a visible target

```shell
--model-directory /models locate --image /input/image.png \
  --target 'the warning icon'
```

Coordinates are integer values normalized to 0 through 1000. Verify coordinates
against labeled examples before using them downstream.
