# OWASP LLM Top 10 mapping

This document maps the readiness checklist to common LLM application security concerns. It is a practical mapping, not a formal security audit.

| OWASP LLM risk | Toolkit checks that help surface it | Practical question |
|---|---|---|
| LLM01 Prompt Injection | Evaluation plan, guardrail/veto checks, must-refuse cases, tool permission design | Can untrusted input override instructions or trigger unsafe actions? |
| LLM02 Insecure Output Handling | Human review, output validation, downstream integration controls | Is model output treated as code, command, or final decision without validation? |
| LLM03 Training Data Poisoning | Data source boundary, knowledge-base update/versioning, supplier controls | Can poisoned or unreviewed data enter the system? |
| LLM04 Model Denial of Service | Cost budget, rate limits, failure handling, abuse cases | Can users or prompts create excessive token/tool usage? |
| LLM05 Supply Chain Vulnerabilities | Vendor/API dependency mapping, model/tool version records | Which third-party models, tools, plugins, or datasets are trusted? |
| LLM06 Sensitive Information Disclosure | Data sensitivity, masking, external model boundary, output review | Can the system expose personal, confidential, or regulated data? |
| LLM07 Insecure Plugin / Tool Design | Access control, tool permissions, human approval for high-risk actions | Can tools perform more than the workflow actually requires? |
| LLM08 Excessive Agency | Human-in-the-loop, prohibited actions, pause/manual takeover | Is the agent allowed to act beyond human-approved boundaries? |
| LLM09 Overreliance | Human review, user training, confidence limits, decision ownership | Will users trust outputs more than evidence supports? |
| LLM10 Model Theft | Access control, logging, vendor boundary, API security | Can model assets, prompts, data, or proprietary behavior be extracted? |

## Veto examples

Do not move to production if:

- sensitive data can be sent to an unapproved model;
- tool calls can execute irreversible actions without approval;
- model outputs enter downstream systems without validation;
- no trace exists for model version, prompt version, tool call, user action, and human approval;
- users are encouraged to rely on AI output as final decision evidence.
