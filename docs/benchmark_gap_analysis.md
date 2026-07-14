# Benchmark gap analysis

This document records what was benchmarked and how the toolkit was improved.

## 1. Benchmark set

| Benchmark | What it does well | Borrowed idea |
|---|---|---|
| NIST AI RMF Playbook | Maps AI risk work into Govern / Map / Measure / Manage; emphasizes voluntary tailored actions | Added `nist_ai_rmf_crosswalk.md` and kept the toolkit as adaptable rather than mandatory |
| OWASP LLM Top 10 | Clear security risk taxonomy for LLM applications | Added `owasp_llm_top10_mapping.md` and veto/security wording |
| Google People + AI Guidebook | Human-centered design, user autonomy, feedback, error recovery | Strengthened adoption, human review, feedback, and user control sections |
| OpenAI Evals | Treats evals as core engineering practice; provides registry and custom eval guidance | Added model evaluation plan and evaluation evidence expectations |
| promptfoo | Strong README, quickstart, CI/CD, red-team positioning, developer-first language | Added quickstart, scoring script, CI workflow, and clearer public positioning |
| DeepEval | Pytest-like LLM testing, rich metrics, agent/RAG coverage | Added test/eval terminology and sample machine-readable assessment |
| Phoenix / Opik | Production observability: tracing, datasets, experiments, online evaluation | Added monitoring, audit, trace, and operations questions |
| NeMo Guardrails / Guardrails AI | Programmable guardrails and validators | Added guardrail/control vocabulary and veto items |
| Microsoft Responsible AI Toolbox / Fairlearn / AIF360 | Responsible AI, error analysis, fairness harms, interpretability | Added AI system card, harms/fairness questions, and risk register |
| TensorFlow Model Card Toolkit | Structured model documentation and transparency artifact | Added `ai_system_card.md` template |
| Microsoft Agent Governance Toolkit | Production-grade README, badges, SECURITY, CONTRIBUTING, compliance mapping, multilingual docs | Added badges, governance docs, issue templates, benchmark notes, and Chinese quickstart |
| OpenAI Cookbook | Practical examples over abstract essays | Added fictional cases and copyable templates |

---

## 2. Original gaps in this repository

| Gap | Why it mattered | Improvement made |
|---|---|---|
| README was useful but too plain | High-quality GitHub projects communicate value in 30 seconds | Rewrote README with value proposition, quickstart, map, framework, and benchmark positioning |
| No benchmark trail | Public readers need to know what this was compared against | Added `SOURCES.md` and this benchmark analysis |
| No machine-readable artifact | Toolkit looked like documents only | Added `examples/sample_assessment.json`, `schemas/readiness_assessment.schema.json`, and `scripts/score_readiness.py` |
| No CI / validation | Public repo lacked engineering signal | Added `.github/workflows/validate.yml` |
| No system documentation template | Production readiness needs transparency documentation | Added `templates/ai_system_card.md` |
| No risk register | Governance needs assignable risks and owners | Added `templates/risk_register.md` |
| No evaluation plan | AI readiness requires eval design, not only subjective review | Added `templates/model_evaluation_plan.md` |
| No pilot decision memo | FDE work needs go/no-go language | Added `templates/pilot_review_memo.md` |
| No NIST / OWASP mapping | Governance and security readers need familiar anchors | Added crosswalk documents |
| No article in repo | GitHub should include technical-report article linked to assets | Added `articles/001_from_ai_demo_to_production.md` |
| No contribution/security hygiene | Mature repos have contribution and security signals | Added `CONTRIBUTING.md`, `SECURITY.md`, issue templates |
| No Chinese quickstart | Portfolio should still serve Chinese readers | Added `docs/quickstart_zh.md` |

---

## 3. Remaining gaps after v0.2

| Gap | Priority | Suggested next step |
|---|---:|---|
| No packaged CLI | Medium | Turn `scripts/score_readiness.py` into an installable CLI only after repeated use |
| No live demo | Medium | Add a GitHub Pages static demo or Streamlit app later |
| No real anonymized case | High | Add one fully fictional but industry-realistic case for public sector / healthcare / industrial workflow |
| No automated markdown link check | Low | Add markdown link checker workflow after repo is public |
| No bilingual full README | Low | Keep English README + Chinese quickstart for now; full bilingual docs later |
| No MCP server | Low | Defer until users ask to call the toolkit from AI clients |

---

## 4. Portfolio implication

The public signal should be:

> This is not just a personal essay. It is a reusable deployment-readiness method, benchmarked against mature AI governance/evaluation/observability/security toolkits and translated into practical templates.

For FDE / AI governance / applied AI roles, this shows:

- structured problem framing;
- production-readiness thinking;
- governance and security awareness;
- eval/observability literacy;
- ability to produce reusable public assets;
- enough technical execution to create scripts, schema, CI and GitHub hygiene.
