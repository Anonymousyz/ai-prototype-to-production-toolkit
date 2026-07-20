from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

from .scoring import (
    load_assessment,
    migrate_assessment,
    render_html,
    render_json,
    render_markdown,
    render_text,
    score_assessment,
    validate_assessment,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-ready",
        description="Score AI prototype-to-production readiness assessments.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    score = sub.add_parser("score", help="Score an assessment JSON file")
    score.add_argument("assessment", help="Path to readiness assessment JSON")
    score.add_argument("--format", choices=["text", "markdown", "html", "json"], default="text", help="Output format")
    score.add_argument("--output", "-o", help="Write output to a file instead of stdout")
    score.add_argument("--allow-veto", action="store_true", help="Return exit code 0 even when veto items are present")

    report = sub.add_parser("report", help="Generate a Markdown or static HTML readiness report")
    report.add_argument("assessment", help="Path to readiness assessment JSON")
    report.add_argument("--format", choices=["markdown", "html"], default="markdown", help="Report format")
    report.add_argument("--output", "-o", required=True, help="Report path")
    report.add_argument("--allow-veto", action="store_true", help="Return exit code 0 even when veto items are present")

    validate = sub.add_parser("validate", help="Validate an assessment JSON file")
    validate.add_argument("assessment", help="Path to readiness assessment JSON")

    migrate = sub.add_parser("migrate", help="Migrate a legacy v0.5 assessment to the v0.6 schema")
    migrate.add_argument("assessment", help="Path to legacy or current assessment JSON")
    migrate.add_argument("--output", "-o", required=True, help="New v0.6 assessment path")

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
    # The wheel ships a package-local copy; source-tree fallbacks preserve
    # compatibility with direct script execution.
    here = Path(__file__).resolve()
    packaged = here.parent / "data" / "sample_assessment.json"
    if packaged.exists():
        return packaged
    for parent in [here, *here.parents]:
        candidate = parent / "examples" / "sample_assessment.json"
        if candidate.exists():
            return candidate
    candidate = Path.cwd() / "examples" / "sample_assessment.json"
    if candidate.exists():
        return candidate
    raise FileNotFoundError("Could not locate examples/sample_assessment.json")


def _reject_source_overwrite(source: str, output: str | None) -> None:
    if not output:
        return
    source_path = Path(source)
    output_path = Path(output)
    try:
        if source_path.exists() and output_path.exists() and source_path.samefile(output_path):
            raise ValueError("output path must differ from the source assessment path")
    except OSError:
        # Fall back to normalized path comparison when the filesystem cannot
        # answer same-file queries (for example, a transient network mount).
        pass
    if source_path.resolve() == output_path.resolve():
        raise ValueError("output path must differ from the source assessment path")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Backward compatibility: `python scripts/score_readiness.py sample.json`.
    if argv and argv[0] not in {"score", "report", "validate", "migrate", "example", "-h", "--help"}:
        argv = ["score", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "score":
            _reject_source_overwrite(args.assessment, args.output)
            result = score_assessment(load_assessment(args.assessment))
            rendered = {
                "text": render_text,
                "markdown": render_markdown,
                "html": render_html,
                "json": render_json,
            }[args.format](result)
            _write_or_print(rendered, args.output)
            return 1 if result.has_veto and not args.allow_veto else 0

        if args.command == "report":
            _reject_source_overwrite(args.assessment, args.output)
            result = score_assessment(load_assessment(args.assessment))
            rendered = {"markdown": render_markdown, "html": render_html}[args.format](result)
            _write_or_print(rendered, args.output)
            return 1 if result.has_veto and not args.allow_veto else 0

        if args.command == "validate":
            validate_assessment(load_assessment(args.assessment))
            print(f"Valid assessment: {args.assessment}")
            return 0

        if args.command == "migrate":
            _reject_source_overwrite(args.assessment, args.output)
            destination = Path(args.output)
            if destination.exists():
                raise FileExistsError(f"refusing to overwrite existing migration output: {destination}")
            source_data = json.loads(Path(args.assessment).read_text(encoding="utf-8-sig"))
            migrated = migrate_assessment(source_data)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(
                json.dumps(migrated, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                encoding="utf-8",
            )
            print(f"Migrated assessment to {destination}")
            return 0

        if args.command == "example":
            src = _sample_path()
            dst = Path(args.output)
            if dst.exists():
                raise FileExistsError(f"refusing to overwrite existing example output: {dst}")
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
