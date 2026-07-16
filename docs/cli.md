# CLI usage

The toolkit includes the local, dependency-free `ai-ready` CLI. Core validation, migration, scoring, and reporting make no network calls and need no model API key.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

## Commands

```bash
ai-ready example --output sample_assessment.json
ai-ready validate examples/sample_assessment.json
ai-ready score examples/sample_assessment.json
ai-ready score examples/sample_assessment.json --format json
ai-ready report examples/sample_assessment.json --output examples/reports/sample_assessment_report.md
ai-ready report examples/sample_assessment.json --format html --output examples/reports/sample_assessment_report.html
ai-ready migrate legacy-v05.json --output assessment-v06.json
```

`example` copies the packaged fictional sample and refuses to overwrite an existing destination.

The backward-compatible script remains available:

```bash
python scripts/score_readiness.py examples/sample_assessment.json
```

## Canonical v0.6 input

Use [`examples/sample_assessment.json`](../examples/sample_assessment.json) and [`schemas/readiness_assessment.schema.json`](../schemas/readiness_assessment.schema.json) together. The CLI requires:

- `schema_version` fixed to `0.6`;
- a non-empty `system_name`; `stage` is optional, but must be non-empty when provided;
- all seven canonical numeric `scores` keys; strings, booleans, NaN, and infinity are rejected;
- matching fixed `max_scores` in this order: **10 / 12 / 12 / 10 / 10 / 10 / 6**;
- all eight canonical boolean `veto_items` keys;
- one or more evidence references for every dimension;
- nested human-review declarations: non-empty `review.owner`, `review.reviewer_type` fixed to `human`, and ISO `review.reviewed_at` (`YYYY-MM-DD`);
- `top_gaps` is required but may be empty; every listed item must be a non-empty string.

Unknown root fields, unknown or missing dimensions, altered maxima, incomplete veto declarations, malformed dates, missing evidence, and unsupported schema versions fail validation. A custom `anything: 1/1` score is invalid.

## Migrating v0.5 input

A v0.5 assessment is a document that matches the prior canonical contract but has no `schema_version`. Migration:

```bash
ai-ready migrate legacy-v05.json --output assessment-v06.json
```

The command creates a new file, adds `schema_version: "0.6"`, and validates the complete v0.6 document. It does not change scores, evidence, veto declarations, reviewer metadata, or the source file. It refuses to overwrite the source or an existing output. Unknown declared versions are not guessed.

## Static HTML report

```bash
ai-ready report examples/sample_assessment.json \
  --format html \
  --output examples/reports/sample_assessment_report.html
```

The HTML is self-contained, script-free, and contains an accessible score table and labelled bars. Assessment text is HTML-escaped before rendering. This is a safer distribution artifact, not a security assessment or deployment authorization.

## Example output

```text
System: Fictional Supplier Document Assistant
Stage: controlled pilot review
Review owner: Fictional cross-functional pilot review committee
Reviewed at: 2026-07-15
Decision: Controlled pilot only
Total: 42/70
Normalized: 42/70 (60.0%)
Veto: no
Top gaps:
- Evaluation set is too small
- Audit log design is incomplete
- Rollback owner is unclear
```

## Method boundary and exit codes

Validation establishes only that the declared structure is present. The CLI does not fetch or authenticate evidence, verify reviewer identity or independence, test a deployed system, perform a security/compliance audit, or authorize production. A high score cannot override any veto.

When `score --output` or `report --output` is used, the output path must differ from the source assessment path. Invalid input or unsafe output paths return exit code `2`; a veto returns `1` unless `--allow-veto` is set.
