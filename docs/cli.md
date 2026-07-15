# CLI usage

The toolkit includes the local, dependency-free `ai-ready` CLI. It makes no network calls and needs no model API key.

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

## Commands

```bash
ai-ready validate examples/sample_assessment.json
ai-ready score examples/sample_assessment.json
ai-ready score examples/sample_assessment.json --format json
ai-ready report examples/sample_assessment.json --output examples/reports/sample_assessment_report.md
```

The backward-compatible script remains available:

```bash
python scripts/score_readiness.py examples/sample_assessment.json
```

## Canonical v0.5 input

Use [`examples/sample_assessment.json`](../examples/sample_assessment.json) and [`schemas/readiness_assessment.schema.json`](../schemas/readiness_assessment.schema.json) together. The CLI requires:

- `system_name` and `stage`;
- all seven canonical `scores` keys;
- matching fixed `max_scores`, each equal to 10;
- all eight canonical boolean `veto_items` keys;
- one or more evidence references for every dimension;
- a non-empty `reviewer` declaration;
- ISO `assessment_date` (`YYYY-MM-DD`);
- one or more non-empty `top_gaps`.

Unknown or missing dimensions, altered maxima, incomplete veto declarations, malformed dates, and missing evidence fail validation. A custom `anything: 1/1` score is invalid.

## Example output

```text
System: Fictional Supplier Document Assistant
Stage: controlled pilot review
Decision: Controlled pilot only
Total: 42/70
Normalized: 42/70 (60.0%)
Veto: no
Top gaps:
- Evaluation set is too small
- Audit log design is incomplete
- Rollback owner is unclear
```

## Method boundary

Validation establishes only that the declared structure is present. The CLI does not fetch or authenticate evidence, verify reviewer identity or independence, test a deployed system, perform a security/compliance audit, or authorize production. A high score cannot override any veto.
