"""Small, typed filesystem helpers used by pipeline modules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.config import OUTPUT_DIR, REPORTS_DIR


def ensure_output_directories() -> None:
    """Create every directory written by the deterministic pipeline."""
    for path in [
        OUTPUT_DIR,
        OUTPUT_DIR / "figures",
        OUTPUT_DIR / "analysis",
        OUTPUT_DIR / "insights",
        OUTPUT_DIR / "kpis",
        OUTPUT_DIR / "bi",
        REPORTS_DIR / "data_quality",
        REPORTS_DIR / "product_taxonomy",
        REPORTS_DIR / "kpis",
        REPORTS_DIR / "analysis",
        REPORTS_DIR / "insights",
        REPORTS_DIR / "validation",
        REPORTS_DIR / "storytelling",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write portable UTF-8 JSON without local paths."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write normalized UTF-8 text ending in exactly one newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
