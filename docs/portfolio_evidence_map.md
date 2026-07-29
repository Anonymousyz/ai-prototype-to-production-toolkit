# Portfolio evidence map

This page maps common AI-deployment questions to artifacts a reviewer can inspect in the public portfolio. It is not a competency score, a hiring rubric, or evidence of client deployment.

## What a reviewer can verify

| Deployment question | Public artifact | What to inspect | What it does **not** establish |
|---|---|---|---|
| Can the author turn a vague AI idea into a bounded workflow? | [FDE discovery guide](../templates/fde_discovery_interview_guide.md), readiness checklist, fictional cases | Workflow questions, decision owners, data boundary prompts, and pilot scope | A completed customer discovery engagement |
| Is there executable software rather than only a framework? | `src/ai_ready/`, `pyproject.toml`, CLI docs | Local install, `ai-ready score`, JSON and Markdown reports | A hosted production service |
| Can a score be manipulated through custom inputs? | [`scoring.py`](../src/ai_ready/scoring.py), [`test_scoring.py`](../tests/test_scoring.py) | Fixed seven dimensions, fixed maxima, eight veto keys, and tests that reject `anything: 1/1` | That the underlying evidence is true |
| Is evaluation treated as an operating question? | [model evaluation plan](../templates/model_evaluation_plan.md), risk register, fictional assessment cases | Failure modes, thresholds, escalation, rollback, and gap documentation | A real-world benchmark result |
| Are governance and security part of the implementation discussion? | [NIST crosswalk](nist_ai_rmf_crosswalk.md), [OWASP mapping](owasp_llm_top10_mapping.md), system card | Practical links between controls, risks, and workflow decisions | Legal advice, a security audit, or compliance certification |
| Can a team prepare for a human decision meeting? | [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit) | Alternatives, criteria, affected stakeholders, reversibility, trade-offs, and a pre-mortem | Approval, source authentication, or implementation authority |
| Can a reviewer inspect the tools and standards used to frame a design? | [Awesome AI Production Readiness](https://github.com/Anonymousyz/awesome-ai-production-readiness) | Curation policy, machine-readable catalog, archived-resource labeling, duplicate checks, and link report | Endorsement or security assessment of listed projects |

## Suggested review path

### For a technical interviewer

1. Run the local CLI against [`examples/sample_assessment.json`](../examples/sample_assessment.json).
2. Read the canonical validation logic in [`src/ai_ready/scoring.py`](../src/ai_ready/scoring.py).
3. Read the regression cases in [`tests/test_scoring.py`](../tests/test_scoring.py), especially the custom-denominator rejection.
4. Open the generated report under [`examples/reports/`](../examples/reports/).

### For a governance or risk interviewer

1. Read [`docs/method_status.md`](method_status.md) before looking at the score.
2. Compare the checklist with the [risk register](../templates/risk_register.md), [AI system card](../templates/ai_system_card.md), and [pilot review memo](../templates/pilot_review_memo.md).
3. Inspect the NIST and OWASP mappings for their stated scope and limits.
4. Follow the decision packet into the [Research-to-Decision Toolkit](https://github.com/Anonymousyz/research-to-decision-toolkit).

### For a product or FDE interviewer

1. Start with the fictional cases and the FDE discovery guide.
2. Ask whether the workflow, data boundary, evaluation plan, human decision point, operating owner, and rollback condition are explicit.
3. Use the [Awesome list](https://github.com/Anonymousyz/awesome-ai-production-readiness) to identify implementation tools for the gaps that remain.

## Honest boundary

The portfolio shows a method, working local software, tests, and fictional/public examples. It does not claim real client outcomes, production uptime, independent certification, or permission to deploy a system. Those claims would require separate evidence.
