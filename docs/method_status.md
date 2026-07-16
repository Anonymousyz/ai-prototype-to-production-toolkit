# Method status and evidence boundary

## Status

The fixed 70-point scale is an **author-designed, uncalibrated decision-support heuristic**. It has not been certified or validated as a substitute for legal, security, safety, compliance, or conformity assessment.

## What v0.6 enforces

- an explicit `schema_version: "0.6"` declaration, plus a non-destructive migration path for the known unversioned v0.5 contract;
- exactly seven named dimensions with fixed maxima **10 / 12 / 12 / 10 / 10 / 10 / 6**;
- complete declaration of eight named veto conditions;
- at least one evidence reference per dimension;
- nested `review.owner`, human `review.reviewer_type`, and ISO `review.reviewed_at` declarations;
- a declared `top_gaps` list, which may be empty;
- veto priority over the numeric total.

This closes the prior structural loophole in which arbitrary user-defined dimensions and maxima could produce a nominal full score.

## What the score can do

- force a team to address workflow, data, evaluation, ownership, auditability, operations, and adoption;
- make veto declarations and missing evidence visible;
- produce a repeatable review artifact;
- compare one system over time when rubric, evidence standard, and reviewers remain stable.

## What the score cannot prove

- that referenced evidence exists, is authentic, sufficient, current, or correctly interpreted;
- that the named reviewer is a human, independent, qualified, or actually completed the review;
- that a system is safe, compliant, secure, fair, or production-ready;
- that organizations or reviewers apply the scale consistently;
- that every sector-specific obligation or affected stakeholder has been assessed.

A reviewer field is a declaration for accountability, not identity verification. An evidence reference is a traceability pointer, not source authentication. The public JSON Schema checks structural shape; the Python runtime additionally rejects whitespace-only identifiers and invalid calendar dates. Static HTML output escapes declared text and contains no scripts, but it is still only a rendering of unverified declarations.

## Calibration roadmap

1. Collect at least 20 independently reviewed fictional or permission-cleared assessments.
2. Measure inter-rater agreement by category and identify ambiguous prompts.
3. Compare declared readiness decisions with later pilot incidents and reversals.
4. Publish rubric revisions, limitations, and migration notes.
5. Seek review from product, security, operations, legal/compliance, and affected-user representatives.

Until that work is complete, treat the output as structured evidence for an accountable human decision meeting—not the decision itself.
