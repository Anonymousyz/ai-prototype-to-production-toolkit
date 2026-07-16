# Readiness-to-decision handoff

An `ai-ready` result answers whether an AI-enabled workflow has enough declared structure, evidence, and operating control for a bounded deployment discussion. It does not resolve the broader business or policy decision. Use [`research-to-decision-toolkit`](https://github.com/Anonymousyz/research-to-decision-toolkit) when the readiness review must become a source-backed **human decision** packet.

## Handoff rule

The handoff **does not copy** the 70-point readiness score into the R2D 24-point score and does not treat a readiness label as the final decision. Each toolkit keeps its own uncalibrated structural contract.

| AI-ready artifact | R2D destination | Human check before transfer |
|---|---|---|
| `system_name`, `stage` | context and research question | Confirm the actual workflow and decision body |
| category scores | gap hypotheses only | Reassess; do not copy numeric values |
| evidence references | claims and evidence matrix | Open, authenticate, date, and interpret every source |
| veto items | constraints, stop conditions, and unresolved risks | Confirm whether the veto is still current |
| top gaps | research gaps and next actions | Assign owner, evidence need, and deadline |
| review owner/date | decision-review provenance | Verify identity, role, independence, and authorization |

## Fictional cross-repository path

The fictional supplier document assistant can be assessed in this repository and then reframed as the fictional procurement-copilot decision in R2D:

```bash
ai-ready validate examples/sample_assessment.json
ai-ready report examples/sample_assessment.json --format html --output readiness-report.html

# In a separate checkout of research-to-decision-toolkit:
r2d validate examples/fictional-ai-governance-research-to-decision/decision_brief.json
r2d report examples/fictional-ai-governance-research-to-decision/decision_brief.json --output decision-report.md
```

The examples are synthetic. Passing both CLIs establishes structural consistency only. It is not evidence of a real client outcome, deployment safety, legal compliance, or decision quality.
