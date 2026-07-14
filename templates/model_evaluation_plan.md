# Model Evaluation Plan

## 1. Evaluation objective

What decision will the evaluation support?

> 

## 2. Use cases

| Use case | Expected behavior | Risk if wrong |
|---|---|---|
|  |  |  |

## 3. Test set

| Dataset / sample set | Size | Source | Data boundary | Owner |
|---|---:|---|---|---|
| Normal cases |  |  |  |  |
| Edge cases |  |  |  |  |
| Must-refuse cases |  |  |  |  |
| Historical failure cases |  |  |  |  |

## 4. Metrics

| Metric | Definition | Threshold | Evidence |
|---|---|---:|---|
| Task success |  |  |  |
| Factuality / faithfulness |  |  |  |
| Refusal accuracy |  |  |  |
| Human correction rate |  |  |  |
| Escalation accuracy |  |  |  |
| Latency |  |  |  |
| Cost per task |  |  |  |

## 5. Failure mode library

| Failure mode | Example | Severity | Detection method | Mitigation |
|---|---|---|---|---|
| Hallucination |  |  |  |  |
| Wrong extraction |  |  |  |  |
| Sensitive data exposure |  |  |  |  |
| Unsafe tool/action suggestion |  |  |  |  |
| Overconfident answer |  |  |  |  |

## 6. Regression rule

Regression tests should run after changes to:

- model;
- system prompt;
- user prompt template;
- retrieval corpus;
- tool permission;
- output schema;
- human review rule.

## 7. Go / no-go threshold

Production trial can proceed only if:

- no veto item exists;
- high-severity failure modes have controls;
- evaluation threshold is met;
- human review and rollback are defined;
- owner signs off.
