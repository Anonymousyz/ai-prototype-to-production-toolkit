# AI Production Readiness Manifesto

> **AI demos prove possibility. Production requires responsibility.**

I designed this toolkit for an awkward handoff: the demo has won attention, but someone still has to decide whether the system belongs in a real workflow.

That decision cannot rest on a polished interface or a single model score. It needs a workflow, evidence, controls, and named owners.

> **Production-ready AI = workflow + evidence + governance + accountability.**

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

## The FDE role is translation

Forward-deployed work connects ambition with operating detail. The engineer has to translate a proposed capability into a workflow, a test plan, controls, ownership, and a handover that another team can run.

Code matters. So do the questions around it: who may use the system, what can go wrong, who notices, and who has the authority to stop it.

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

Only then is “production” a useful conversation.

## 中文摘要

这个工具箱针对一个很具体的交接点：AI demo 已经能跑，但团队还没有足够依据决定它能否进入真实业务流程。

模型效果只是其中一部分。真正需要核验的，是业务流程、数据授权、评估证据、人工责任、日志、运行成本和回滚机制。v0.5 把七个维度和八项一票否决条件固定下来，避免自定义分母把任意输入包装成满分。

CLI 只能检查材料是否按固定结构填写，不能证明证据真实，也不能证明评审人身份。最终判断仍由有权限、能承担后果的人作出。

> **生产级 AI = 业务流程 + 评估证据 + 治理机制 + 责任链。**
