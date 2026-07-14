#!/usr/bin/env python3
"""Backward-compatible wrapper for the ai-ready CLI.

Usage:
    python scripts/score_readiness.py examples/sample_assessment.json
    python scripts/score_readiness.py score examples/sample_assessment.json --format markdown
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ai_ready.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
