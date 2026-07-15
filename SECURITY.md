# Security and information handling

The local CLI and compatibility script make no network calls. They read only the assessment file supplied by the user. The repository also contains prompts that may be copied into external AI services; those services have separate retention, training, access, residency, and contractual terms.

## Do not submit or publish

- API keys, tokens, passwords, connection strings, or credentials;
- personal or sensitive data;
- confidential client or employer documents;
- privileged, export-controlled, contract-restricted, or non-public incident material;
- real system names, architectures, or vulnerabilities not authorized for disclosure.

De-identification or summarization alone is not authorization. Consider contractual restrictions and re-identification risk before external-model processing or publication.

AI-generated reviews are drafting material, not source evidence or independent security/compliance review. The CLI validates declared structure but does not authenticate evidence, verify reviewer identity, inspect a deployed system, or grant production approval.

## Reporting a vulnerability

Use the repository's security-reporting channel. Include a minimal reproducer without live secrets, personal data, or confidential source material.
