from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

from .scoring import load_assessment, render_json, render_markdown, render_text, score_assessment, validate_assessment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-ready",
        description="Score AI prototype-to-production readiness assessments.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    score = sub.add_parser("score", help="Score an assessment JSON file")
    score.add_argument("assessment", help="Path to readiness assessment JSON")
    score.add_argument("--format", choices=["text", "markdown", "json"], default="text", help="Output format")
    score.add_argument("--output", "-o", help="Write output to a file instead of stdout")
    score.add_argument("--allow-veto", action="store_true", help="Return exit code 0 even when veto items are present")

    report = sub.add_parser("report", help="Generate a Markdown readiness report")
    report.add_argument("assessment", help="Path to readiness assessment JSON")
    report.add_argument("--output", "-o", required=True, help="Markdown report path")
    report.add_argument("--allow-veto", action="store_true", help="Return exit code 0 even when veto items are present")

    validate = sub.add_parser("validate", help="Validate an assessment JSON file")
    validate.add_argument("assessment", help="Path to readiness assessment JSON")

    example = sub.add_parser("example", help="Copy the sample assessment JSON")
    example.add_argument("--output", "-o", default="sample_assessment.json", help="Destination path")

    return parser


def _write_or_print(text: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n", encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print(text)


def _sample_path() -> Path:
    # Works from installed editable package and from source tree.
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        candidate = parent / "examples" / "sample_assessment.json"
        if candidate.exists():
            return candidate
    candidate = Path.cwd() / "examples" / "sample_assessment.json"
    if candidate.exists():
        return candidate
    raise FileNotFoundError("Could not locate examples/sample_assessment.json")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Backward compatibility: `python scripts/score_readiness.py sample.json`.
    if argv and argv[0] not in {"score", "report", "validate", "example", "-h", "--help"}:
        argv = ["score", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "score":
            result = score_assessment(load_assessment(args.assessment))
            rendered = {
                "text": render_text,
                "markdown": render_markdown,
                "json": render_json,
            }[args.format](result)
            _write_or_print(rendered, args.output)
            return 1 if result.has_veto and not args.allow_veto else 0

        if args.command == "report":
            result = score_assessment(load_assessment(args.assessment))
            _write_or_print(render_markdown(result), args.output)
            return 1 if result.has_veto and not args.allow_veto else 0

        if args.command == "validate":
            validate_assessment(load_assessment(args.assessment))
            print(f"Valid assessment: {args.assessment}")
            return 0

        if args.command == "example":
            src = _sample_path()
            dst = Path(args.output)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            print(f"Copied sample assessment to {dst}")
            return 0

    except Exception as exc:  # pragma: no cover - CLI boundary
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
