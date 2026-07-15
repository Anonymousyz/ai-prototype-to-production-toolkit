# Benchmark gap analysis

This document records public references used for design comparison. It is not a claim of endorsement, equivalence, or compliance.

## Benchmark set

| Benchmark | Strength observed | Adaptation in this toolkit |
|---|---|---|
| NIST AI RMF and Playbook | Govern / Map / Measure / Manage framing and voluntary profiles | Crosswalk plus adaptable governance questions |
| OWASP Top 10 for LLM and GenAI Applications 2025 | Current LLM application security taxonomy | Practical, non-audit security/veto crosswalk |
| Google People + AI Guidebook | Human autonomy, feedback, error recovery | Human review, adoption, and user-control questions |
| OpenAI Evals, promptfoo, DeepEval, RAGAS | Test cases, metrics, regression, red teaming | Evaluation-plan and evidence expectations |
| Phoenix and Opik | Tracing, datasets, experiments, online evaluation | Monitoring, auditability, and operating questions |
| NeMo Guardrails and Guardrails AI | Programmable controls and validators | Guardrail/control vocabulary and veto conditions |
| Fairlearn and AIF360 | Harm and fairness analysis | Risk-register and system-card prompts |
| Hugging Face model cards | Maintained model documentation practice | Lightweight AI system-card template |
| Google Model Card Toolkit | Historical structured-documentation implementation; repository is archived | Retained as historical context, not a recommended maintained dependency |
| OpenAI Cookbook | Practical, reproducible examples | Fictional cases and copyable local commands |

See [`SOURCES.md`](../SOURCES.md) for direct URLs and access dates.

## Gaps closed through v0.5

| Earlier gap | Current response |
|---|---|
| Document-only appearance | Installable local CLI, JSON schema, examples, and tests |
| No fixed machine-readable contract | Canonical seven dimensions, fixed maxima, eight veto keys, and evidence/reviewer/date fields |
| Arbitrary-score loophole | Unknown dimensions and altered maxima now fail validation; regression test covers `anything: 1/1` |
| Limited governance artifacts | System card, risk register, evaluation plan, discovery guide, and pilot memo |
| Weak reference trail | NIST and OWASP crosswalks plus a source register |
| No engineering verification | Local unit suite and inactive GitHub Actions template under `docs/` |
| Ambiguous archived dependency | Archived Model Card Toolkit is labeled historical; maintained model-card practice points to Hugging Face |

## Deliberately unresolved gaps

| Gap | Why unresolved | Evidence-bearing next step |
|---|---|---|
| No calibration | Author-designed rubric has not been independently rated | Run permission-cleared multi-rater studies and publish agreement data |
| No evidence authentication | Local CLI does not fetch or verify sources | Define pluggable evidence attestations without presenting them as truth proof |
| No reviewer identity verification | Free-text declaration preserves portability | Add optional signed review records only after threat modeling and user demand |
| No production outcome validation | Public cases are fictional | Publish permission-cleared longitudinal case evidence when available |
| No active CI workflow | Current credential scope is not authorized to publish workflows | Activate the documented template only with explicit workflow-scope authorization |
| No live demo | Local CLI is the current reproducible surface | Add a static demo only if it preserves the same validation contract |

## Portfolio implication

The defensible public signal is not “this score proves production readiness.” It is:

> This repository turns deployment-readiness questions into a fixed, testable evidence structure, publishes its method boundary, and leaves the production decision with accountable humans.
