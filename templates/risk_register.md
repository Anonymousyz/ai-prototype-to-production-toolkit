# AI Deployment Risk Register

| ID | Risk | Category | Severity | Likelihood | Control / mitigation | Owner | Evidence | Status |
|---|---|---|---|---|---|---|---|---|
| R1 | Unauthorized or unclear data use | Data / compliance | High |  | Confirm data authorization and allowed model boundary |  |  | Open |
| R2 | Hallucinated or incomplete output | Model quality | High |  | Evaluation set, failure cases, human review |  |  | Open |
| R3 | Overreliance by users | Human factors | Medium |  | UI warning, training, review requirement |  |  | Open |
| R4 | Missing audit trail | Governance / audit | High |  | Log user action, model version, prompt version, output, human approval |  |  | Open |
| R5 | Excessive tool or workflow autonomy | Agent safety | High |  | Limit actions, require approval, define prohibited actions |  |  | Open |
| R6 | Cost spike or denial-of-wallet | Operations | Medium |  | Budget limit, rate limit, usage monitoring |  |  | Open |
| R7 | Vendor / API dependency failure | Operations | Medium |  | fallback, pause, rollback plan |  |  | Open |

## Categories

- Data / compliance
- Model quality
- Security
- Human factors
- Governance / audit
- Operations
- Vendor / supply chain
- Adoption

## Status values

- Open
- In progress
- Mitigated
- Accepted
- Closed
