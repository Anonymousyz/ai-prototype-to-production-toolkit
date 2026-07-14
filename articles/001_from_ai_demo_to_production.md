# From AI Demo to Production: A Readiness Framework for Enterprise AI Deployment

## Summary

Many AI projects do not fail because the model is weak. They fail because the organization cannot answer a more operational question:

> What must be true before this AI prototype can enter a real business workflow?

A demo proves possibility. Production requires responsibility.

This article introduces a practical readiness framework for moving AI prototypes into enterprise, public-sector, or regulated workflows.

---

## 1. The demo-production gap

A working AI demo usually proves three things:

1. the model can generate plausible output;
2. users can imagine a better workflow;
3. a sponsor can see potential value.

But a production workflow requires more:

- the business process must be explicit;
- data use must be authorized;
- outputs must be evaluated;
- human review must be designed;
- access and logs must support auditability;
- failures must have owners;
- cost and operations must be sustainable;
- real users must adopt the new workflow.

This is why “the demo works” is not the same as “the system is ready.”

---

## 2. Seven readiness dimensions

The toolkit uses seven dimensions.

### 2.1 Business workflow and value

The first question is not “Which model should we use?”

The first question is:

> Which workflow changes, for whom, and how will we know it improved?

If there is no baseline, no user, and no value metric, the AI prototype is still a concept.

### 2.2 Data source, authorization, and boundaries

AI deployment often fails at the data boundary:

- Who owns the data?
- Can it be used for this purpose?
- Can it be sent to an external model?
- Does it contain personal, confidential, or regulated information?
- How is it retained, masked, isolated, or deleted?

A prototype that ignores data authorization should not become production.

### 2.3 Model output quality and evaluation

Evaluation cannot rely on “the answer looks good.”

Teams need:

- test cases;
- edge cases;
- must-refuse cases;
- historical failure cases;
- regression tests;
- thresholds for acceptable quality.

Evaluation frameworks such as OpenAI Evals, promptfoo, DeepEval, RAGAS, Phoenix, and Opik are valuable here. This toolkit does not replace them; it helps decide what needs to be evaluated before production.

### 2.4 Human review and responsibility

For many enterprise workflows, the correct design is not full automation.

A practical deployment should separate:

- tasks AI can automate;
- tasks AI can draft but humans must approve;
- tasks AI should refuse or escalate;
- tasks AI must never perform.

The responsibility chain matters: when the AI output is wrong, who notices, who corrects, who explains, and who owns the consequence?

### 2.5 Access control, logs, and auditability

If the team cannot reconstruct what happened, the system is not ready.

Production AI systems should record:

- user action;
- input category;
- model version;
- prompt version;
- retrieval or tool version;
- output;
- human approval/rejection;
- incident or correction.

Auditability is not paperwork after launch. It is a design requirement before launch.

### 2.6 System integration, operations, and cost

A production AI workflow depends on systems, APIs, vendors, retrieval sources, model endpoints, identity systems, and human operations.

The team should know:

- what fails when the model endpoint fails;
- how to pause or roll back;
- who pays for tokens and infrastructure;
- what rate limits and budget limits exist;
- who maintains the system after the first pilot.

### 2.7 Organizational adoption and improvement

Even if the model works, users may not adopt it.

The team needs:

- first user group;
- training plan;
- feedback channel;
- review cadence;
- improvement backlog;
- decision rule for expansion or shutdown.

---

## 3. A practical go/no-go rule

A prototype should not move into production if any of these are true:

- unauthorized data is used;
- sensitive or regulated data enters an unapproved external model;
- high-risk decisions are affected without human review;
- there are no logs, versions, or traceability;
- no one owns errors, pause, rollback, or maintenance;
- model output quality cannot be evaluated;
- costs are not controlled or owned;
- users are encouraged to over-rely on the AI output.

These are not abstract governance concerns. They are deployment blockers.

---

## 4. How to use the toolkit

Start with four files:

1. [`templates/fde_discovery_interview_guide.md`](../templates/fde_discovery_interview_guide.md)
2. [`templates/ai_prototype_readiness_checklist.md`](../templates/ai_prototype_readiness_checklist.md)
3. [`templates/risk_register.md`](../templates/risk_register.md)
4. [`templates/pilot_review_memo.md`](../templates/pilot_review_memo.md)

For a quick scoring demo:

```bash
python scripts/score_readiness.py examples/sample_assessment.json
```

---

## 5. Why this matters for FDE work

Forward deployed engineering is not only about writing code at the customer site. In AI deployment, the FDE-like role often has to connect:

- customer workflow;
- AI capability;
- engineering constraints;
- governance requirements;
- measurable business value;
- product feedback.

The best FDE work turns a vague AI opportunity into a controlled deployment path.

That requires both technical literacy and organizational judgment.

---

## 6. Final thought

The question is not:

> “Can the model answer this?”

The better question is:

> “Can the organization safely, measurably, and responsibly use this answer in a real workflow?”

That is the difference between an AI demo and an AI deployment.
