# AI Production Readiness Manifesto

I designed this toolkit for the handoff after a demo has won attention and before a team decides whether the system belongs in a real workflow.

The decision needs more than a polished interface or a model score. The team must describe the workflow, examine evidence, define controls, and name the people responsible for operating the system.

## What a demo actually proves

A demo shows that a system worked under a chosen set of conditions. That matters, but it does not tell us how the system behaves with ordinary users, disputed inputs, unavailable dependencies, cost spikes, or an operator who needs to reverse a bad action.

The useful question is simple:

> What must be true before this output is allowed to influence a real workflow?

A team that cannot answer this question still has an experiment. It may be a good experiment. It is not yet a deployment case.

## The model sits inside a larger system

This toolkit reviews seven areas:

1. business workflow and value;
2. data authorization and boundaries;
3. output quality and evaluation;
4. human review and responsibility;
5. access control, logs, and auditability;
6. integration, operations, cost, and rollback;
7. adoption and improvement.

A stronger model does not repair unclear ownership. It does not create data permission, an incident owner, or a rollback path. Those are system design problems.

The v0.5 CLI therefore fixes all seven dimensions and all eight veto keys. Earlier drafts let an input file define its own dimensions and denominator. That was flexible, but it also made a nominal full score easy to manufacture. The current contract closes that loophole.

## Evidence has to survive questions

Before a pilot decision, the review packet should identify:

- the data the system may use;
- the evaluation cases and failure costs;
- observed failure modes;
- the person who may approve, override, or stop an action;
- the records retained for later review;
- the owners of incidents and cost;
- the rollback condition.

A reference in a JSON file is not proof. A reviewer name is not identity verification. The CLI checks whether these declarations exist and follow the fixed contract; accountable people still have to verify them.

## Human review needs a real job

“Human in the loop” is too vague to be useful. A review design should say what the person sees, which actions require approval, how disagreement is recorded, and when escalation is mandatory.

The reviewer also needs authority. If the system can act before the reviewer can intervene, the diagram may show a human while the workflow does not.

## Logs are part of the product

Useful logs let a team reconstruct an event: source input, retrieved context, model and prompt version, output, human edit, decision, downstream action, and rollback.

This is operational evidence, not paperwork added for an audit. Without it, teams cannot investigate failures or decide whether a control worked.

## Governance belongs in delivery

Governance work starts during discovery. It appears in the risk register, evaluation plan, access design, system card, pilot memo, and release decision. Waiting until launch turns governance into cleanup.

That is why this repository contains working artifacts and a CLI rather than a policy essay alone. The artifacts make gaps discussable. They do not make the final decision.

## Deployment work is translation

Applied AI work connects a proposed capability with operating detail. The person doing that work has to turn the proposal into a workflow, a test plan, controls, named ownership, and a handover another team can run.

Code matters alongside the operating questions: who may use the system, what can go wrong, who notices, and who has authority to stop it.

## A practical review sequence

When someone asks whether a working demo can go into production, ask:

1. Which workflow changes?
2. Which data is authorized?
3. What evidence defines acceptable performance?
4. Which actions require human judgment?
5. What is recorded?
6. Who owns incidents and operating cost?
7. What triggers rollback?
8. Who makes the decision, and on what evidence?

At that point, the team can discuss a production decision with shared terms and evidence.

## 中文摘要

这个工具箱处理一个具体交接点：AI 演示原型已经能运行，团队还需要判断它是否具备进入真实业务流程的条件。

模型效果只是材料的一部分。团队还要核对业务流程、数据授权、评估证据、人工责任、日志、运行成本和回滚机制。v0.5 固定七个维度和八项否决条件，防止自定义分母把任意输入包装成满分。

CLI 只检查材料是否按固定结构填写，不能核验证据真实性或评审人身份。最终判断仍由有权限、能够承担后果的人作出。
