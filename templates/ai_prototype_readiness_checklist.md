# AI Prototype-to-Production Readiness Checklist

Use this checklist before moving an AI prototype into a real business workflow.

Score each item:

- `0` = not defined;
- `1` = partially defined;
- `2` = clearly defined and supported by evidence.

---

## 1. Business workflow and value

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 1 | The exact business workflow is defined, not just a general “AI productivity” goal. |  |  |
| 2 | The baseline is known: time, cost, error rate, waiting time, or manual effort. |  |  |
| 3 | Success metrics are defined. |  |  |
| 4 | The first real users and usage frequency are identified. |  |  |
| 5 | The cost of not deploying is understood. |  |  |

---

## 2. Data source, authorization, and boundaries

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 6 | All input data sources are listed. |  |  |
| 7 | Data authorization and allowed use are confirmed. |  |  |
| 8 | Personal, sensitive, confidential, or regulated data is identified. |  |  |
| 9 | Data masking, classification, isolation, or minimization rules exist. |  |  |
| 10 | The team knows whether data can be sent to external models or third-party APIs. |  |  |
| 11 | Data update, expiry, deletion, and versioning rules are defined. |  |  |

---

## 3. Model output quality and evaluation

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 12 | Must-answer question types are defined. |  |  |
| 13 | Must-refuse or escalate question types are defined. |  |  |
| 14 | Test cases cover normal, edge, and adversarial inputs. |  |  |
| 15 | A failure case library exists. |  |  |
| 16 | Regression tests run after model, prompt, tool, or knowledge-base changes. |  |  |
| 17 | Minimum acceptable output quality is defined. |  |  |

---

## 4. Human review and responsibility chain

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 18 | Automated, human-reviewed, and prohibited use cases are separated. |  |  |
| 19 | Review roles, permissions, and timelines are defined. |  |  |
| 20 | Human edits, approvals, and rejections are logged. |  |  |
| 21 | Error explanation, correction, and escalation responsibilities are defined. |  |  |
| 22 | Pause, downgrade, or manual takeover mechanisms exist. |  |  |

---

## 5. Access control, logs, and auditability

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 23 | User roles and access permissions are defined. |  |  |
| 24 | Data, features, and outputs are restricted by role. |  |  |
| 25 | User actions, model calls, and outputs are logged. |  |  |
| 26 | Prompt, model, knowledge-base, and tool versions are recorded. |  |  |
| 27 | Logs support audit, review, incident investigation, and accountability. |  |  |

---

## 6. System integration, operations, and cost

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 28 | Integration with existing business tools, identity systems, or data systems is defined. |  |  |
| 29 | API, model, knowledge-base, and file-processing failures are handled. |  |  |
| 30 | Backup, rollback, release, and change-management rules exist. |  |  |
| 31 | Model, token, storage, review, and operations costs are estimated. |  |  |
| 32 | Maintenance ownership and response timelines are defined. |  |  |

---

## 7. Organizational adoption and continuous improvement

| # | Check | Score | Evidence / notes |
|---:|---|---:|---|
| 33 | First users, training, and use scenarios are defined. |  |  |
| 34 | A feedback channel and iteration cadence exist. |  |  |
| 35 | A 3-month operations, review, and expansion plan exists. |  |  |

---

## Veto items

Do not move into production if any of the following is true:

- unauthorized data is used;
- sensitive or regulated data enters an unapproved external model;
- high-risk decisions are affected without human review;
- there are no logs, versions, or traceability;
- no one owns errors, pause, rollback, or maintenance;
- model output quality cannot be evaluated;
- costs are not controlled or owned;
- the system is marketed as production-ready but remains a demo.
