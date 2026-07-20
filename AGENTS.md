# Agent instructions

This repository is a local-first CLI (`ai-ready`) plus governance templates for scoring whether an AI prototype is structurally ready to enter a real business workflow. Documentation honesty is the product: every number the README states is locked by a test.

## Setup and verification

```bash
python -m pip install -e .
python -m pip install jsonschema   # optional; enables the schema cross-validation test
python -m unittest discover -s tests -v
ai-ready score examples/sample_assessment.json
```

All tests must pass before any commit. The suite runs in under a second.

## Hard rules

- Zero runtime dependencies. Do not add packages to `[project.dependencies]`.
- The canonical contract is frozen: seven dimensions summing to 70 points, eight veto keys, decision-tier thresholds at 25/45/60. Changing any of these requires the owner's explicit approval and a schema-version bump.
- `schemas/readiness_assessment.schema.json` and the runtime validator in `src/ai_ready/scoring.py` must stay in agreement; the cross-validation test enforces this.
- Every README claim (scores, counts, expected output) must stay backed by a test or a committed artifact. If you change behavior, update README, `README.zh-CN.md`, `docs/cli.md`, and the tests together.
- Examples are fictional. Never add real client, employer, or personal data. Never commit secrets.
- Record notable changes under `## Unreleased` in `CHANGELOG.md`. Do not create release tags or GitHub releases; releases are owner ceremonies with checksums and provenance.
- Keep `.github/workflows/validate.yml` aligned with `docs/github_actions_validate.template.yml`; a test checks the shared steps.
