# AI production review model

This page turns the repository’s method into a compact review model for a team considering a pilot or production deployment.

## Four parts of the review

| Part | What the team needs to establish | Risk when it is absent |
|---|---|---|
| Workflow | Which business process changes, who uses it, and who owns the decision | No named owner or measurable use |
| Evidence | Evaluation cases, logs, incidents, review records, and pilot findings | Decisions rest on untested assumptions |
| Controls | Data boundaries, risk register, control design, documentation, and review gates | Authorization and control gaps remain unclear |
| Operating responsibility | Named people and processes for review, incidents, cost, and rollback | Failures have no accountable response |

## What the toolkit provides

| Repository asset | How it is used |
|---|---|
| Readiness checklist | Review the workflow alongside model performance |
| Scorecard | Record fixed thresholds and veto conditions |
| Risk register | Name risks, owners, and planned responses |
| AI system card | Describe purpose, data, limitations, and controls |
| Model evaluation plan | Define evaluation before a wider rollout |
| Pilot review memo | Record the decision and its conditions |
| CLI report | Produce a repeatable review record |

## Use the model in a review

1. Name the workflow owner and the decision point.
2. State what evidence supports acceptable performance and which gaps remain.
3. Specify human review, authorization, logging, incident response, cost ownership, and rollback.
4. If a required condition is missing, keep the work in demonstration or controlled-pilot review until the team resolves it.
5. Let a responsible person make the deployment decision from the evidence, not from the score alone.

## Short public description

> I build tools for the handoff between AI prototypes and operating workflows: evaluation evidence, control design, human review, auditability, and clear responsibility.