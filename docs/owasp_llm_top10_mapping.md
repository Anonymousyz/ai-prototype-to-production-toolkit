# OWASP Top 10 for LLM and GenAI Applications 2025 mapping

This document maps the readiness checklist to the **2025** OWASP Top 10 risk names. It is a practical crosswalk, not a formal security audit or evidence that a control is effective.

Authoritative index: [OWASP GenAI Security Project — 2025 Top 10](https://genai.owasp.org/llm-top-10/). Checked 2026-07-15.

| OWASP 2025 risk | Toolkit checks that help surface it | Practical question |
|---|---|---|
| LLM01 Prompt Injection | Adversarial evaluation, must-refuse cases, instruction/data separation, tool-permission design | Can untrusted content override instructions or trigger an unauthorized action? |
| LLM02 Sensitive Information Disclosure | Data classification, minimization, external-model boundaries, output review | Can prompts, retrieval context, logs, or outputs expose personal, confidential, or regulated information? |
| LLM03 Supply Chain | Model, dataset, library, tool, and vendor inventory; version and provenance records | Which third-party artifacts are trusted, and how are changes or compromises detected? |
| LLM04 Data and Model Poisoning | Data provenance, ingestion approval, update/version controls, evaluation against manipulated content | Can poisoned training, fine-tuning, retrieval, or embedding data alter behavior? |
| LLM05 Improper Output Handling | Output validation, encoding/sanitization, downstream integration controls, human approval | Is model output treated as executable code, a command, or a final decision without validation? |
| LLM06 Excessive Agency | Least-privilege tool permissions, prohibited actions, approval gates, pause/manual takeover | Can the system perform more actions than the approved workflow requires? |
| LLM07 System Prompt Leakage | Secret separation, prompt-content review, access controls, red-team tests | Would disclosure of a system prompt expose secrets or weaken a control boundary? |
| LLM08 Vector and Embedding Weaknesses | Retrieval authorization, namespace isolation, provenance, poisoning tests, access-aware retrieval | Can embeddings or vector-store behavior leak, mix, or retrieve unauthorized content? |
| LLM09 Misinformation | Grounded evaluation, citations, uncertainty handling, human decision ownership | Can unsupported output be mistaken for reliable evidence or an authoritative decision? |
| LLM10 Unbounded Consumption | Rate limits, budget ownership, timeouts, recursion/tool-call limits, abuse monitoring | Can a user or agent create uncontrolled model, token, tool, or infrastructure consumption? |

## Veto examples

Do not move to production when any of these remains true:

- sensitive data can be sent to an unapproved model;
- irreversible tool calls can execute without accountable human approval;
- model outputs enter downstream systems without validation;
- model, prompt, retrieval, tool-call, user-action, and approval traces are absent;
- users are encouraged to treat AI output as final decision evidence;
- consumption limits and cost ownership are undefined;
- the system is marketed as production-ready while required controls remain demonstrably absent.

OWASP categories identify common risk areas; this mapping does not establish compliance with OWASP guidance or replace threat modeling and security testing for a specific system.
