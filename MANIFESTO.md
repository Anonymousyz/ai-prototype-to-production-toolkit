# AI Production Readiness Manifesto

> **AI demos prove possibility. Production requires responsibility.**

This repository is built around one thesis:

> **Production-ready AI = workflow + evidence + governance + accountability.**

A model can be impressive in a demo and still be unready for a real business workflow. The gap is not only technical. It is operational, organizational, legal, ethical, and human.

This manifesto explains the thinking behind the toolkit.

---

## 1. A demo is not a deployment decision

A demo proves that something can work once, in a controlled setting, with motivated users and limited consequences.

Production deployment means the system will affect real users, real workflows, real data, real budgets, and real responsibilities.

The question is not:

> Does the AI output look good?

The question is:

> What must be true before this output can safely influence a real workflow?

---

## 2. The model is only one part of the system

Many AI projects over-focus on model capability and under-specify the surrounding system.

Production readiness requires at least seven dimensions:

1. business workflow and value;
2. data source authorization and boundaries;
3. model output quality and evaluation;
4. human review and responsibility chain;
5. access control, logs and auditability;
6. system integration, operations and cost;
7. organizational adoption and improvement loops.

A better model cannot compensate for unclear ownership, weak data boundaries, missing logs, or no rollback plan.

---

## 3. Evidence should come before excitement

Excitement is useful for exploration. Evidence is required for deployment.

A team should be able to show:

- what data the system can and cannot use;
- what evaluation cases were tested;
- what failure modes were observed;
- who reviews or overrides outputs;
- what logs are kept;
- who owns cost and incidents;
- what happens when the system is wrong.

If these answers are missing, the system is still a demo, no matter how impressive the interface looks.

---

## 4. Human review is a product requirement

Human review is often treated as a compliance patch. It should be designed as part of the product.

Good human review answers:

- which decisions require a human;
- what the reviewer can see;
- what evidence is shown;
- how disagreement is handled;
- when escalation is required;
- how corrections improve the system.

A human-in-the-loop label means little without a real responsibility chain.

---

## 5. Auditability is not paperwork

Audit logs are not only for auditors. They are how teams learn from failures, resolve disputes, and improve systems.

A production AI system should make important events traceable:

- input sources;
- retrieval context;
- model outputs;
- human edits;
- approval or rejection;
- downstream actions;
- incidents and rollback.

Without traceability, accountability becomes theatre.

---

## 6. Governance should be embedded in delivery

AI governance should not arrive after the product is already shipped.

For enterprise and regulated AI, governance is part of delivery:

- discovery questions;
- readiness scoring;
- risk register;
- model/system documentation;
- evaluation plan;
- pilot review memo;
- release decision.

This is why this toolkit includes templates, prompts, scorecards, examples, and a CLI. The goal is to make governance operational, not ornamental.

---

## 7. The FDE job is translation

Forward-deployed engineering is not just writing a demo inside a customer environment.

The harder work is translation:

- from executive ambition to workflow design;
- from model output to business evidence;
- from user excitement to adoption plan;
- from risk concern to control design;
- from prototype to accountable system.

This is the operating model behind the toolkit.

---

## 8. Practical rule

When someone says:

> The AI demo works. Can we put it into production?

Answer with this review sequence:

1. What workflow will change?
2. What data is authorized?
3. How do we evaluate quality?
4. Who reviews outputs?
5. What is logged?
6. Who owns incidents and cost?
7. What is the rollback plan?
8. What evidence supports the decision?

Only then should a team discuss production deployment.

---

## Chinese summary / 中文摘要

这个项目背后的核心判断是：

> **AI demo 证明可能性，生产化要求责任。**

生产级 AI 不是“模型效果不错”就可以上线，而是要同时具备：

- 真实业务流程；
- 明确数据边界；
- 可复核评估证据；
- 人工责任链；
- 审计日志；
- 成本和故障责任；
- 回滚机制；
- 组织采纳路径。

一句话：

> **生产级 AI = 业务流程 + 评估证据 + 治理机制 + 责任链。**
