# Promptfoo integration example

This optional example shows how model-evaluation evidence can be prepared for an `ai-ready` assessment. It does not convert Promptfoo results into readiness scores, veto decisions, compliance conclusions, or production approval.

## Information boundary

- Use only fictional, public, synthetic, or explicitly **authorized** test material.
- Do not send **confidential** client, employer, personal, security, or regulated data to an external provider.
- Anonymization alone is not authorization.
- Keep the default `echo` provider for a local wiring check. Before selecting a real model provider, confirm data authorization and place credentials in environment variables rather than files.
- An accountable **human** must review the test design, outputs, failures, and relevance before referencing them as evidence.

## Dry-run the fixture

From this directory:

```bash
npx promptfoo@0.121.19 eval -c promptfooconfig.yaml
```

The committed config uses Promptfoo's deterministic `echo` provider. It verifies template and assertion wiring; it does not evaluate a model.

## Use with an authorized provider

1. Copy `promptfooconfig.yaml` to an untracked working file.
2. Replace `echo` with an approved provider ID from the [official Promptfoo provider documentation](https://www.promptfoo.dev/docs/providers/).
3. Replace the synthetic cases with authorized evaluation fixtures.
4. Run the evaluation locally and retain the exact config, provider/model version, date, failures, and output path.
5. Have a human reviewer decide which result files may be cited under `evidence.model_output_quality_and_evaluation`.

Do not automatically translate pass rate into the 12-point evaluation score. The readiness score also depends on fixture coverage, failure severity, workflow consequence, reviewer judgment, and unresolved veto conditions.

## Source

Configuration structure follows the official Promptfoo documentation:

- https://www.promptfoo.dev/docs/configuration/parameters/
- https://www.promptfoo.dev/docs/configuration/test-cases/
- https://www.promptfoo.dev/docs/providers/echo/
