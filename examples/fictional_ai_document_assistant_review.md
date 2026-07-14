# Fictional example: AI document assistant readiness review

> This is a fictional case for demonstration. It does not describe a real customer or organization.

## 1. Context

A mid-sized operations team built an AI assistant to summarize incoming supplier documents and extract key dates, obligations, and risk flags.

The demo works well on three clean PDF samples. The team wants to launch it to 80 users next month.

## 2. Initial readiness review

| Dimension | Score | Notes |
|---|---:|---|
| Business workflow and value | 6/10 | Workflow is clear, but baseline error rate is not measured. |
| Data boundaries | 4/12 | Supplier contracts may contain confidential terms; authorization unclear. |
| Model evaluation | 3/12 | No test set, no failure categories, no regression testing. |
| Human review | 5/10 | Users are expected to review, but responsibility is not logged. |
| Logs and auditability | 2/10 | Basic app logs exist; no model/prompt/output versioning. |
| Operations and cost | 4/10 | API cost estimated, but no fallback or rollback. |
| Adoption | 4/6 | First users identified; training plan missing. |
| **Total** | **28/70** | Controlled pilot only. |

## 3. Veto items

Potential blocker: confidential contract content may be sent to an unapproved external model.

## 4. Top risks

1. Data authorization is unclear.
2. No evaluation set exists.
3. Human review is not captured as an auditable action.
4. No rollback plan exists if summaries are wrong.
5. Users may treat extracted obligations as final decisions.

## 5. Recommended 30-day remediation plan

| Week | Action | Owner | Evidence |
|---|---|---|---|
| 1 | Confirm data authorization and model boundary | Legal / IT | Approved data-use note |
| 1 | Build 50-document test set | Ops lead | Test set and expected outputs |
| 2 | Define error categories and severity | Product / Risk | Evaluation rubric |
| 2 | Add human review status | Engineering | Review log field |
| 3 | Run pilot with 10 users | Ops | Usage and error report |
| 4 | Decide expand / revise / stop | Sponsor | Pilot decision memo |

## 6. Decision

Do not launch to 80 users yet. Run a controlled pilot with limited users, approved documents, human review, and explicit logs.
