# AI Prototype-to-Production Toolkit

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)
![GitHub release](https://img.shields.io/github/v/release/Anonymousyz/ai-prototype-to-production-toolkit)

A practical toolkit for the moment after an AI demo works and before anyone should call it production-ready.

It gives teams checklists, scorecards, prompts, templates, a local CLI, and three fictional assessment cases for enterprise, public-sector, and regulated AI deployment work.

> Many AI demos look impressive. Production deployment is different: business workflow, data boundaries, model evaluation, human review, access control, audit logging, cost ownership, rollback, and organizational adoption all matter.

> [!IMPORTANT]
> The score is an author-designed decision-support heuristic. It is not certification or proof of safety, compliance, security, or production readiness. v0.5 fixes the seven dimensions and eight veto keys, requires evidence references and a dated human review declaration, but does not verify their truth or the reviewer's identity. Read the [method status and evidence boundary](docs/method_status.md) before using it in a real decision.

---

## Core thesis

> **AI demos prove possibility. Production requires responsibility.**

This toolkit is built around a simple operating model:

```text
Production-ready AI = workflow + evidence + governance + accountability
```

Core beliefs:

- A demo is not a deployment decision.
- Readiness depends on workflow, governance, evaluation, and accountability as much as model output.
- Enterprise AI should be reviewed through evidence, not excitement.
- Human review, auditability, rollback, and ownership are product requirements, not compliance afterthoughts.
- The FDE job is to translate AI capability into an accountable operating workflow.

Read the full [`MANIFESTO.md`](MANIFESTO.md) and [`docs/production_ready_ai_thesis.md`](docs/production_ready_ai_thesis.md).

---

## 30-second value proposition

Use this toolkit when a team says:

> “The AI demo works. Can we put it into the real workflow next month?”

It helps the team answer:

1. What is clear enough for pilot?
2. What is still a blocker?
3. What evidence must be collected before production?
4. What should be automated, human-reviewed, or prohibited?
5. Which risks map to NIST AI RMF and OWASP LLM Top 10 concerns?

---

## Quick start

### Option A: human workshop

1. Copy [`templates/ai_prototype_readiness_checklist.md`](templates/ai_prototype_readiness_checklist.md).
2. Score the prototype with [`scorecards/ai_prototype_readiness_scorecard.md`](scorecards/ai_prototype_readiness_scorecard.md).
3. Fill [`templates/risk_register.md`](templates/risk_register.md).
4. Write a decision memo using [`templates/pilot_review_memo.md`](templates/pilot_review_memo.md).

### Option B: installable CLI

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e .
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

Generate a Markdown report:

```bash
ai-ready report examples/sample_assessment.json --output examples/reports/sample_assessment_report.md
```

See [`docs/cli.md`](docs/cli.md), [`docs/demo.md`](docs/demo.md), and [`examples/terminal_demo.txt`](examples/terminal_demo.txt).

---

## Repository map

| Area | Files | Purpose |
|---|---|---|
| Orientation | [`README.md`](README.md), [`docs/quickstart_zh.md`](docs/quickstart_zh.md) | Explain the toolkit to public readers |
| Thought model | [`MANIFESTO.md`](MANIFESTO.md), [`docs/production_ready_ai_thesis.md`](docs/production_ready_ai_thesis.md) | Make the deployment philosophy explicit |
| Checklist | [`templates/ai_prototype_readiness_checklist.md`](templates/ai_prototype_readiness_checklist.md) | Assess deployment readiness across 7 dimensions |
| Score / CLI | [`scorecards/ai_prototype_readiness_scorecard.md`](scorecards/ai_prototype_readiness_scorecard.md), [`scripts/score_readiness.py`](scripts/score_readiness.py), [`src/ai_ready`](src/ai_ready), [`docs/cli.md`](docs/cli.md) | Convert qualitative review into a decision and Markdown report |
| Governance artifacts | [`templates/ai_system_card.md`](templates/ai_system_card.md), [`templates/risk_register.md`](templates/risk_register.md), [`templates/model_evaluation_plan.md`](templates/model_evaluation_plan.md) | Document system purpose, risk, evaluation and controls |
| FDE workflow | [`templates/fde_discovery_interview_guide.md`](templates/fde_discovery_interview_guide.md) | Guide discovery conversations with business teams |
| Prompts | [`prompts/ai_readiness_review_prompt.md`](prompts/ai_readiness_review_prompt.md), [`prompts/fde_case_study_prompt.md`](prompts/fde_case_study_prompt.md) | Use AI assistants to structure review and case writing |
| Crosswalks | [`docs/nist_ai_rmf_crosswalk.md`](docs/nist_ai_rmf_crosswalk.md), [`docs/owasp_llm_top10_mapping.md`](docs/owasp_llm_top10_mapping.md) | Map checklist to NIST and OWASP language |
| Method boundary | [`docs/method_status.md`](docs/method_status.md) | State the heuristic's limits and validation roadmap |
| Examples | [`docs/demo.md`](docs/demo.md), [`examples/sample_assessment.json`](examples/sample_assessment.json), [`examples/internal_policy_search_assistant.json`](examples/internal_policy_search_assistant.json), [`examples/customer_support_action_agent.json`](examples/customer_support_action_agent.json) | Demonstrate score, veto, and decision behavior |
| Packaging | [`pyproject.toml`](pyproject.toml), [`docs/github_actions_validate.template.yml`](docs/github_actions_validate.template.yml) | Install locally; CI remains a documented template until the repository credential can publish workflows |
| Public writing | [`articles/001_from_ai_demo_to_production.md`](articles/001_from_ai_demo_to_production.md), [`articles/002_ai_deployment_is_a_responsibility_problem.md`](articles/002_ai_deployment_is_a_responsibility_problem.md) | Technical-report style articles for GitHub |
| Benchmarking | [`docs/benchmark_gap_analysis.md`](docs/benchmark_gap_analysis.md), [`SOURCES.md`](SOURCES.md) | Explain what high-quality projects were benchmarked |

---

## Core framework

A prototype becomes production-ready only when the team can answer questions across seven dimensions:

1. **Business workflow and value:** Which workflow changes, and how is value measured?
2. **Data source, authorization, and boundaries:** What data is used, and under what authorization?
3. **Model output quality and evaluation:** How are quality, hallucination, failure, and regression measured?
4. **Human review and responsibility chain:** Which actions need human review, and who owns mistakes?
5. **Access control, logs, and auditability:** Can the team prove who did what, when, with which model/prompt/version?
6. **System integration, operations, and cost:** Can the system survive failure, rollback, cost spikes, and ownership changes?
7. **Organizational adoption and continuous improvement:** Will real users adopt it, and how will feedback improve the workflow?

```mermaid
flowchart LR
  A[AI demo] --> B[Workflow mapping]
  B --> C[Data boundary review]
  C --> D[Evaluation plan]
  D --> E[Human review design]
  E --> F[Access logs auditability]
  F --> G[Ops cost rollback]
  G --> H[Pilot decision]
  H --> I[Production trial or revise]
```

---

## Where it fits

This is **not** an LLM evaluation framework like OpenAI Evals, promptfoo, DeepEval, Phoenix, Opik, or RAGAS.

It sits before or beside those tools as a deployment-readiness layer:

| Tool category | Examples | What they are strong at | This toolkit adds |
|---|---|---|---|
| Evals/testing | OpenAI Evals, promptfoo, DeepEval, RAGAS | Metrics, test cases, regression, CI | Business workflow, governance, role ownership, go/no-go decisions |
| Observability | Phoenix, Opik | Tracing, monitoring, experiments | Pre-production readiness and governance evidence |
| Guardrails/security | NeMo Guardrails, Guardrails AI, OWASP LLM Top 10 | Input/output controls, security risk taxonomy | Cross-functional deployment checklist and pilot memo |
| Responsible AI | Microsoft Responsible AI Toolbox, Fairlearn, AIF360, Model Card Toolkit | Fairness, explainability, model documentation | Lightweight enterprise AI system card + risk register |
| Human-centered AI | Google PAIR Guidebook | User autonomy, feedback, error recovery | Production readiness framing for enterprise workflows |

---

## Limits

This toolkit is **not**:

- legal advice;
- security audit;
- medical, financial, or certification advice;
- a substitute for professional compliance review;
- a guarantee that an AI system is safe or production-ready.

Use it as a structured starting point for product, governance, risk, compliance, and deployment discussions.

The current release uses a fixed but uncalibrated 70-point scale. Every dimension requires referenced evidence, a named reviewer and assessment date are mandatory, and all eight veto keys must be declared. These checks are structural: unresolved vetoes cannot be offset by a high total, and the CLI does not authenticate evidence or reviewer identity.

---

## Chinese summary / 中文简介

这是一套面向 **FDE / AI 落地 / AI 治理 / 受监管行业部署** 的公开工具箱，用来判断一个 AI 原型是否具备进入真实业务流程的准备度。

它不是单篇文章，也不是单条 prompt，而是：

- readiness checklist；
- scorecard；
- risk register；
- AI system card；
- FDE discovery interview guide；
- prompt templates；
- fictional case；
- NIST AI RMF / OWASP LLM Top 10 对照；
- 一个可安装运行、可生成 Markdown/JSON 报告的 CLI；
- 三个分别展示“受控试点、较强准备度、一票否决”的虚构案例。

---

## Roadmap

The next evidence-bearing milestones are documented in [`docs/roadmap.md`](docs/roadmap.md): broader tests, independent rubric review, more cases, a stable package release, and real-world feedback that can be published without disclosing confidential data.

---

## License

MIT License. See [`LICENSE`](LICENSE).

---

## Sources and benchmark projects

See [`SOURCES.md`](SOURCES.md) and [`docs/benchmark_gap_analysis.md`](docs/benchmark_gap_analysis.md).
