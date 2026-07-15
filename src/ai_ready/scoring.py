from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Mapping

REQUIRED_FIELDS = ["system_name", "scores", "max_scores", "veto_items", "top_gaps"]


@dataclass(frozen=True)
class AssessmentResult:
    system_name: str
    stage: str | None
    decision: str
    total: float
    max_total: float
    normalized_70: float
    percentage: float
    has_veto: bool
    veto_items: list[str]
    top_gaps: list[str]
    category_scores: dict[str, dict[str, float]]


def decision(total: float, max_total: float, has_veto: bool) -> str:
    """Return a deployment decision using the default 70-point heuristic scale."""
    if has_veto:
        return "Do not proceed: veto item present"
    normalized = total / max_total * 70 if max_total else 0
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


def _numeric(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be numeric, not boolean")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc


def validate_assessment(data: Mapping[str, Any]) -> None:
    missing = [k for k in REQUIRED_FIELDS if k not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    if not isinstance(data["system_name"], str) or not data["system_name"].strip():
        raise ValueError("system_name must be a non-empty string")
    if data.get("stage") is not None and (not isinstance(data["stage"], str) or not data["stage"].strip()):
        raise ValueError("stage must be a non-empty string when provided")
    if not isinstance(data["scores"], Mapping) or not data["scores"]:
        raise ValueError("scores must be a non-empty object")
    if not isinstance(data["max_scores"], Mapping):
        raise ValueError("max_scores must be an object")
    if not isinstance(data["veto_items"], Mapping):
        raise ValueError("veto_items must be an object")
    if not all(isinstance(value, bool) for value in data["veto_items"].values()):
        raise ValueError("every veto_items value must be boolean")
    if not isinstance(data["top_gaps"], list) or not all(isinstance(x, str) for x in data["top_gaps"]):
        raise ValueError("top_gaps must be a list of strings")
    for category, value in data["scores"].items():
        if category not in data["max_scores"]:
            raise ValueError(f"Missing max score for category: {category}")
        score = _numeric(value, f"score for category {category}")
        maximum = _numeric(data["max_scores"][category], f"max score for category {category}")
        if maximum <= 0:
            raise ValueError(f"max score must be positive for category: {category}")
        if score < 0 or score > maximum:
            raise ValueError(f"score out of range for category: {category}")


def score_assessment(data: Mapping[str, Any]) -> AssessmentResult:
    validate_assessment(data)
    scores = {k: float(v) for k, v in data["scores"].items()}
    max_scores = {k: float(v) for k, v in data["max_scores"].items()}
    total = sum(scores.values())
    max_total = sum(max_scores[k] for k in scores)
    normalized_70 = total / max_total * 70 if max_total else 0.0
    percentage = total / max_total * 100 if max_total else 0.0
    veto_items = [k for k, v in data["veto_items"].items() if v]
    category_scores = {
        k: {"score": scores[k], "max": max_scores[k], "percentage": scores[k] / max_scores[k] * 100}
        for k in scores
    }
    return AssessmentResult(
        system_name=data["system_name"].strip(),
        stage=data.get("stage", "").strip() or None,
        decision=decision(total, max_total, bool(veto_items)),
        total=total,
        max_total=max_total,
        normalized_70=normalized_70,
        percentage=percentage,
        has_veto=bool(veto_items),
        veto_items=veto_items,
        top_gaps=list(data["top_gaps"]),
        category_scores=category_scores,
    )


def _fmt_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}".rstrip("0").rstrip(".")


def render_text(result: AssessmentResult) -> str:
    lines = [f"System: {result.system_name}"]
    if result.stage:
        lines.append(f"Stage: {result.stage}")
    lines.extend([
        f"Decision: {result.decision}",
        f"Total: {_fmt_number(result.total)}/{_fmt_number(result.max_total)}",
        f"Normalized: {_fmt_number(result.normalized_70)}/70 ({result.percentage:.1f}%)",
        f"Veto: {'yes' if result.has_veto else 'no'}",
    ])
    if result.veto_items:
        lines.append("Veto items:")
        lines.extend(f"- {item}" for item in result.veto_items)
    if result.top_gaps:
        lines.append("Top gaps:")
        lines.extend(f"- {gap}" for gap in result.top_gaps)
    return "\n".join(lines)


def render_markdown(result: AssessmentResult) -> str:
    lines = [
        f"# AI readiness report: {result.system_name}", "", "## Summary", "",
        f"- **Stage:** {result.stage or 'not specified'}",
        f"- **Decision:** {result.decision}",
        f"- **Total:** {_fmt_number(result.total)}/{_fmt_number(result.max_total)}",
        f"- **Normalized:** {_fmt_number(result.normalized_70)}/70 ({result.percentage:.1f}%)",
        f"- **Veto:** {'yes' if result.has_veto else 'no'}", "", "## Category scores", "",
        "| Category | Score | Max | % |", "|---|---:|---:|---:|",
    ]
    for category, values in result.category_scores.items():
        label = category.replace("_", " ")
        lines.append(f"| {label} | {_fmt_number(values['score'])} | {_fmt_number(values['max'])} | {values['percentage']:.1f}% |")
    lines.extend(["", "## Veto items", ""])
    lines.extend((f"- {item}" for item in result.veto_items) if result.veto_items else ["No veto item was marked true."])
    lines.extend(["", "## Top gaps", ""])
    lines.extend((f"- {gap}" for gap in result.top_gaps) if result.top_gaps else ["No top gaps were listed."])
    lines.extend(["", "## Suggested next action", "", _suggest_next_action(result), "", "## Method note", "", "This output is a decision-support heuristic, not certification, legal advice, or proof that deployment is safe."])
    return "\n".join(lines)


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
    return json.dumps(asdict(result), ensure_ascii=False, indent=2)
