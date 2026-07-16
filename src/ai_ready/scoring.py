from __future__ import annotations

from dataclasses import asdict, dataclass
from copy import deepcopy
from datetime import date
from html import escape
import json
import math
from pathlib import Path
import re
from typing import Any, Mapping

CURRENT_SCHEMA_VERSION = "0.6"
CANONICAL_MAX_SCORES: dict[str, int] = {
    "business_workflow_and_value": 10,
    "data_source_authorization_boundaries": 12,
    "model_output_quality_and_evaluation": 12,
    "human_review_and_responsibility_chain": 10,
    "access_control_logs_auditability": 10,
    "system_integration_operations_cost": 10,
    "organizational_adoption_improvement": 6,
}
CANONICAL_VETO_ITEMS = (
    "unauthorized_data_use",
    "sensitive_data_to_unapproved_model",
    "high_risk_decision_without_human_review",
    "no_logs_or_traceability",
    "no_error_or_rollback_owner",
    "cannot_evaluate_output_quality",
    "uncontrolled_cost",
    "marketed_as_production_ready_but_remains_demo",
)
REQUIRED_FIELDS = [
    "schema_version",
    "system_name",
    "scores",
    "max_scores",
    "veto_items",
    "top_gaps",
    "evidence",
    "review",
]


@dataclass(frozen=True)
class AssessmentResult:
    system_name: str
    stage: str | None
    review_owner: str
    reviewed_at: str
    decision: str
    total: float
    max_total: float
    normalized_70: float
    percentage: float
    has_veto: bool
    veto_items: list[str]
    top_gaps: list[str]
    category_scores: dict[str, dict[str, float]]
    evidence_refs: dict[str, list[str]]


def decision(total: float, max_total: float, has_veto: bool) -> str:
    """Return a deployment discussion label using the fixed 70-point heuristic."""
    total_value = _numeric(total, "decision total")
    max_value = _numeric(max_total, "decision maximum")
    if max_value <= 0:
        raise ValueError("decision maximum must be greater than zero")
    if total_value < 0 or total_value > max_value:
        raise ValueError("decision total must be between zero and the decision maximum")
    if not isinstance(has_veto, bool):
        raise ValueError("decision has_veto must be boolean")
    if has_veto:
        return "Do not proceed: veto item present"
    normalized = total_value / max_value * 70
    if normalized <= 25:
        return "Demo only"
    if normalized <= 45:
        return "Controlled pilot only"
    if normalized <= 60:
        return "Small production trial with monitoring"
    return "Stronger production readiness, still check controls"


def load_assessment(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, Mapping):
        raise ValueError("assessment must be a JSON object")
    validate_assessment(data)
    return dict(data)


def migrate_assessment(data: Mapping[str, Any]) -> dict[str, Any]:
    """Return a validated v0.6 copy of a legacy v0.5 or current assessment."""
    if not isinstance(data, Mapping):
        raise ValueError("assessment must be a JSON object")
    migrated = deepcopy(dict(data))
    version = migrated.get("schema_version")
    if "schema_version" not in migrated:
        migrated["schema_version"] = CURRENT_SCHEMA_VERSION
    elif version != CURRENT_SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {version!r}")
    validate_assessment(migrated)
    return migrated


def _numeric(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be numeric, not boolean")
    if not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a JSON number, not {type(value).__name__}")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _iso_date(value: Any, label: str) -> str:
    if not _nonempty_string(value) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
        raise ValueError(f"{label} must be an ISO date (YYYY-MM-DD)")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO date (YYYY-MM-DD)") from exc


def _require_exact_keys(actual: Mapping[str, Any], expected: set[str], label: str) -> None:
    actual_keys = set(actual)
    if actual_keys != expected:
        missing = sorted(expected - actual_keys)
        extra = sorted(actual_keys - expected)
        details = []
        if missing:
            details.append(f"missing={missing}")
        if extra:
            details.append(f"extra={extra}")
        raise ValueError(f"{label} must match the canonical set ({'; '.join(details)})")


def validate_assessment(data: Mapping[str, Any]) -> None:
    allowed_root_fields = set(REQUIRED_FIELDS) | {"stage"}
    extra_root_fields = sorted(set(data) - allowed_root_fields)
    if extra_root_fields:
        raise ValueError(f"Unknown root fields: {', '.join(extra_root_fields)}")
    missing = [key for key in REQUIRED_FIELDS if key not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    if data["schema_version"] != CURRENT_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be '{CURRENT_SCHEMA_VERSION}', got {data['schema_version']!r}"
        )
    if not _nonempty_string(data["system_name"]):
        raise ValueError("system_name must be a non-empty string")
    if data.get("stage") is not None and not _nonempty_string(data["stage"]):
        raise ValueError("stage must be a non-empty string when provided")

    scores = data["scores"]
    max_scores = data["max_scores"]
    if not isinstance(scores, Mapping):
        raise ValueError("scores must be an object")
    if not isinstance(max_scores, Mapping):
        raise ValueError("max_scores must be an object")
    canonical_dimensions = set(CANONICAL_MAX_SCORES)
    _require_exact_keys(scores, canonical_dimensions, "scores canonical score dimensions")
    _require_exact_keys(max_scores, canonical_dimensions, "max_scores canonical score dimensions")
    for category, canonical_maximum in CANONICAL_MAX_SCORES.items():
        score = _numeric(scores[category], f"score for category {category}")
        maximum = _numeric(max_scores[category], f"max score for category {category}")
        if maximum != canonical_maximum:
            raise ValueError(
                f"canonical maximum for {category} is {canonical_maximum}, got {maximum:g}"
            )
        if score < 0 or score > maximum:
            raise ValueError(f"score out of range for category: {category}")

    veto_items = data["veto_items"]
    if not isinstance(veto_items, Mapping):
        raise ValueError("veto_items must be an object")
    _require_exact_keys(veto_items, set(CANONICAL_VETO_ITEMS), "veto_items canonical veto items")
    if not all(isinstance(value, bool) for value in veto_items.values()):
        raise ValueError("every veto_items value must be boolean")

    top_gaps = data["top_gaps"]
    if not isinstance(top_gaps, list) or not all(_nonempty_string(item) for item in top_gaps):
        raise ValueError("top_gaps must be a list of strings and every item must be non-empty")

    evidence = data["evidence"]
    if not isinstance(evidence, Mapping):
        raise ValueError("evidence must be an object keyed by canonical score dimension")
    _require_exact_keys(evidence, canonical_dimensions, "evidence dimensions")
    for category, references in evidence.items():
        if (
            not isinstance(references, list)
            or not references
            or not all(_nonempty_string(item) for item in references)
        ):
            raise ValueError(f"evidence.{category} must be a non-empty list of reference strings")

    review = data["review"]
    if not isinstance(review, Mapping):
        raise ValueError("review must be an object")
    _require_exact_keys(review, {"owner", "reviewer_type", "reviewed_at"}, "review fields")
    if not _nonempty_string(review.get("owner")):
        raise ValueError("review.owner must name the accountable human review owner")
    if review.get("reviewer_type") != "human":
        raise ValueError("review.reviewer_type must be 'human'; AI assistance cannot own the review")
    _iso_date(review.get("reviewed_at"), "review.reviewed_at")


def score_assessment(data: Mapping[str, Any]) -> AssessmentResult:
    validate_assessment(data)
    scores = {
        key: _numeric(data["scores"][key], f"score for category {key}")
        for key in CANONICAL_MAX_SCORES
    }
    max_scores = {key: float(CANONICAL_MAX_SCORES[key]) for key in CANONICAL_MAX_SCORES}
    total = sum(scores.values())
    max_total = float(sum(CANONICAL_MAX_SCORES.values()))
    normalized_70 = total / max_total * 70
    percentage = total / max_total * 100
    veto_items = [key for key in CANONICAL_VETO_ITEMS if data["veto_items"][key]]
    category_scores = {
        key: {
            "score": scores[key],
            "max": max_scores[key],
            "percentage": scores[key] / max_scores[key] * 100,
        }
        for key in CANONICAL_MAX_SCORES
    }
    review = data["review"]
    return AssessmentResult(
        system_name=data["system_name"].strip(),
        stage=data.get("stage", "").strip() or None,
        review_owner=review["owner"].strip(),
        reviewed_at=_iso_date(review["reviewed_at"], "review.reviewed_at"),
        decision=decision(total, max_total, bool(veto_items)),
        total=total,
        max_total=max_total,
        normalized_70=normalized_70,
        percentage=percentage,
        has_veto=bool(veto_items),
        veto_items=veto_items,
        top_gaps=list(data["top_gaps"]),
        category_scores=category_scores,
        evidence_refs={key: list(data["evidence"][key]) for key in CANONICAL_MAX_SCORES},
    )


def _fmt_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}".rstrip("0").rstrip(".")


def render_text(result: AssessmentResult) -> str:
    lines = [f"System: {result.system_name}"]
    if result.stage:
        lines.append(f"Stage: {result.stage}")
    lines.extend(
        [
            f"Review owner: {result.review_owner}",
            f"Reviewed at: {result.reviewed_at}",
            f"Decision: {result.decision}",
            f"Total: {_fmt_number(result.total)}/{_fmt_number(result.max_total)}",
            f"Normalized: {_fmt_number(result.normalized_70)}/70 ({result.percentage:.1f}%)",
            f"Veto: {'yes' if result.has_veto else 'no'}",
        ]
    )
    if result.veto_items:
        lines.append("Veto items:")
        lines.extend(f"- {item}" for item in result.veto_items)
    if result.top_gaps:
        lines.append("Top gaps:")
        lines.extend(f"- {gap}" for gap in result.top_gaps)
    return "\n".join(lines)


def render_markdown(result: AssessmentResult) -> str:
    lines = [
        f"# AI readiness report: {result.system_name}",
        "",
        "## Summary",
        "",
        f"- **Stage:** {result.stage or 'not specified'}",
        f"- **Human review owner:** {result.review_owner}",
        f"- **Reviewed at:** {result.reviewed_at}",
        f"- **Decision:** {result.decision}",
        f"- **Total:** {_fmt_number(result.total)}/{_fmt_number(result.max_total)}",
        f"- **Normalized:** {_fmt_number(result.normalized_70)}/70 ({result.percentage:.1f}%)",
        f"- **Veto:** {'yes' if result.has_veto else 'no'}",
        "",
        "## Category scores",
        "",
        "| Category | Score | Max | % |",
        "|---|---:|---:|---:|",
    ]
    for category, values in result.category_scores.items():
        label = category.replace("_", " ")
        lines.append(
            f"| {label} | {_fmt_number(values['score'])} | {_fmt_number(values['max'])} | {values['percentage']:.1f}% |"
        )
    lines.extend(["", "## Evidence references", ""])
    for category, references in result.evidence_refs.items():
        lines.append(f"### {category.replace('_', ' ')}")
        lines.extend(f"- {reference}" for reference in references)
        lines.append("")
    lines.extend(["## Veto items", ""])
    lines.extend(
        (f"- {item}" for item in result.veto_items)
        if result.veto_items
        else ["No veto item was marked true."]
    )
    lines.extend(["", "## Top gaps", ""])
    lines.extend(
        (f"- {gap}" for gap in result.top_gaps)
        if result.top_gaps
        else ["No top gaps were listed."]
    )
    lines.extend(
        [
            "",
            "## Suggested next action",
            "",
            _suggest_next_action(result),
            "",
            "## Method note",
            "",
            "This output is a fixed-schema decision-support heuristic, not certification, legal advice, source verification, or proof that deployment is safe.",
        ]
    )
    return "\n".join(lines)


def render_html(result: AssessmentResult) -> str:
    """Render a self-contained, script-free HTML report with escaped content."""
    title = escape(result.system_name)
    rows: list[str] = []
    for category, values in result.category_scores.items():
        label = category.replace("_", " ")
        label_html = escape(label)
        percentage = values["percentage"]
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{label_html}</th>"
            f"<td>{_fmt_number(values['score'])}</td>"
            f"<td>{_fmt_number(values['max'])}</td>"
            f"<td>{percentage:.1f}%</td>"
            "<td><div class=\"bar\" role=\"img\" "
            f"aria-label=\"{escape(label, quote=True)}: {percentage:.1f}%\">"
            f"<span style=\"width:{percentage:.1f}%\"></span></div></td>"
            "</tr>"
        )

    evidence_sections: list[str] = []
    for category, references in result.evidence_refs.items():
        label = escape(category.replace("_", " "))
        items = "".join(f"<li>{escape(reference)}</li>" for reference in references)
        evidence_sections.append(f"<section><h3>{label}</h3><ul>{items}</ul></section>")

    veto_items = (
        "".join(f"<li>{escape(item)}</li>" for item in result.veto_items)
        if result.veto_items
        else "<li>No veto item was marked true.</li>"
    )
    gap_items = (
        "".join(f"<li>{escape(gap)}</li>" for gap in result.top_gaps)
        if result.top_gaps
        else "<li>No top gaps were listed.</li>"
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI readiness report: {title}</title>
<style>
:root{{--ink:#172033;--muted:#526076;--line:#cbd5e1;--accent:#1459a6;--bg:#f7f9fc}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,sans-serif}}
main{{max-width:1040px;margin:auto;padding:2rem}} section{{background:white;border:1px solid var(--line);border-radius:10px;margin:1rem 0;padding:1rem 1.25rem}}
h1,h2,h3{{line-height:1.25}} table{{width:100%;border-collapse:collapse}} caption{{font-weight:700;text-align:left;margin-bottom:.5rem}}
th,td{{border:1px solid var(--line);padding:.6rem;text-align:left;vertical-align:top}} .bar{{min-width:150px;height:1rem;background:#e2e8f0;border-radius:999px;overflow:hidden}} .bar span{{display:block;height:100%;background:var(--accent)}} .boundary{{border-left:5px solid #b45309}}
</style>
</head>
<body><main>
<h1>AI readiness report: {title}</h1>
<section aria-labelledby="summary"><h2 id="summary">Summary</h2><ul>
<li><strong>Stage:</strong> {escape(result.stage or 'not specified')}</li>
<li><strong>Human review owner:</strong> {escape(result.review_owner)}</li>
<li><strong>Reviewed at:</strong> {escape(result.reviewed_at)}</li>
<li><strong>Decision:</strong> {escape(result.decision)}</li>
<li><strong>Total:</strong> {_fmt_number(result.total)}/{_fmt_number(result.max_total)} ({result.percentage:.1f}%)</li>
<li><strong>Veto:</strong> {'yes' if result.has_veto else 'no'}</li>
</ul></section>
<section aria-labelledby="scores"><h2 id="scores">Category scores</h2>
<table><caption>Declared readiness score by category</caption><thead><tr><th scope="col">Category</th><th scope="col">Score</th><th scope="col">Max</th><th scope="col">Percent</th><th scope="col">Visual</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</section>
<section aria-labelledby="evidence"><h2 id="evidence">Evidence references</h2>{''.join(evidence_sections)}</section>
<section aria-labelledby="veto"><h2 id="veto">Veto items</h2><ul>{veto_items}</ul></section>
<section aria-labelledby="gaps"><h2 id="gaps">Top gaps</h2><ul>{gap_items}</ul></section>
<section aria-labelledby="next"><h2 id="next">Suggested next action</h2><p>{escape(_suggest_next_action(result))}</p></section>
<section class="boundary" aria-labelledby="method"><h2 id="method">Method note</h2><p>This output is a fixed-schema decision-support heuristic, not certification, legal advice, source verification, or proof that deployment is safe.</p></section>
</main></body></html>"""
    return html


def _suggest_next_action(result: AssessmentResult) -> str:
    if result.has_veto:
        return "Stop the deployment path until veto items are resolved and independently reviewed."
    if result.normalized_70 <= 25:
        return "Keep the system as a demo. Clarify workflow value, data boundaries, evaluation and ownership before pilot."
    if result.normalized_70 <= 45:
        return "Run only a controlled pilot with human review, logging, rollback ownership and a small evaluation set."
    if result.normalized_70 <= 60:
        return "Proceed to a small production trial only if monitoring, incident response and business ownership are explicit."
    return "Proceed carefully with production readiness review; continue monitoring, red-team tests and periodic risk review."


def render_json(result: AssessmentResult) -> str:
    return json.dumps(asdict(result), ensure_ascii=False, indent=2, allow_nan=False)
