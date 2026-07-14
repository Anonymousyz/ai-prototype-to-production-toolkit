# CLI usage

The toolkit includes a small installable CLI named `ai-ready`.

It is intentionally lightweight: no external dependencies, no network calls, no model API keys.

## Install locally

Use a virtual environment. Some systems block global installs via PEP 668.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
```

## Validate an assessment

```bash
ai-ready validate examples/sample_assessment.json
```

## Score an assessment

```bash
ai-ready score examples/sample_assessment.json
```

Expected output:

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

## Generate a Markdown report

```bash
ai-ready report examples/sample_assessment.json --output examples/reports/sample_assessment_report.md
```

## JSON output for automation

```bash
ai-ready score examples/sample_assessment.json --format json
```

## Backward-compatible script

The old script still works:

```bash
python scripts/score_readiness.py examples/sample_assessment.json
```

## Input format

Use [`examples/sample_assessment.json`](../examples/sample_assessment.json) as the minimum working example.

Required fields:

- `system_name`
- `scores`
- `max_scores`
- `veto_items`
- `top_gaps`

Optional field:

- `stage`
