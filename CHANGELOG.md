# Changelog

All notable changes to this project are documented here.

## v0.5.0 — 2026-07-15

- Made the seven 70-point dimensions and all eight veto keys canonical; one-field `1/1` inputs now fail validation.
- Required per-dimension evidence references plus a dated, human-owned review declaration.
- Expanded the JSON schema and regression suite to enforce dimensions, maxima, veto completeness, evidence, and review metadata.
- Updated the OWASP crosswalk to the official 2025 LLM/GenAI Top 10 names.
- Kept the score explicitly structural: the CLI still cannot verify evidence truth, reviewer identity, or production safety.

## v0.4.0 — 2026-07-15

- Strengthened input validation for empty identifiers, boolean/nonnumeric scores, malformed veto values, and non-string gaps.
- Expanded unit coverage from 3 to 11 tests, including CLI, malformed JSON, boundary, and reporting cases.
- Added two fictional assessment cases to demonstrate stronger readiness and veto override behavior.
- Added an explicit method-status document, calibration roadmap, and report disclaimer.
- Removed internal growth notes from the public product surface and clarified the evidence-bearing roadmap.

## v0.3.1

- Added `MANIFESTO.md` to make the core AI production-readiness philosophy explicit.
- Added `docs/production_ready_ai_thesis.md` with the workflow + evidence + governance + accountability model.
- Added article: `AI Deployment Is a Responsibility Problem, Not Just a Model Problem`.
- Updated README with core thesis and public thought model links.

## v0.3.0

- Added installable Python package `ai-ready`.
- Added `ai-ready score`, `ai-ready report`, `ai-ready validate`, and `ai-ready example` commands.
- Added Markdown report generation.
- Added unit tests and a CI package-installation template.
- Added CLI documentation and terminal demo.

## v0.2.0 — Draft

- Rewrote README with quickstart, framework, and benchmark positioning.
- Added benchmark gap analysis.
- Added NIST AI RMF crosswalk.
- Added OWASP LLM Top 10 mapping.
- Added Chinese quickstart.
- Added AI system card, risk register, model evaluation plan, and pilot review memo templates.
- Added article: From AI Demo to Production.
- Added machine-readable sample assessment JSON and a Python scoring script.
- Added GitHub Actions validation workflow template.
- Added CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, and issue templates.

## v0.1.0 — Initial draft

- Initial checklist, scorecard, prompts, source table, and fictional document-assistant example.
