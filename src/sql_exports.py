"""Static SQL-layer validation without requiring a database server."""

from __future__ import annotations

import re
from pathlib import Path

from src.config import BASE_DIR
from src.exceptions import OutputValidationError

SQL_ORDER = [
    "01_schema.sql",
    "02_data_quality.sql",
    "03_executive_kpis.sql",
    "04_time_performance.sql",
    "05_menu_performance.sql",
    "06_location_channel_performance.sql",
    "07_opportunity_analysis.sql",
]


def validate_sql_layer(sql_dir: Path = BASE_DIR / "sql") -> list[Path]:
    """Validate file order, independent terminators, and cleaned-schema references."""
    paths = [sql_dir / name for name in SQL_ORDER]
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        raise OutputValidationError(f"SQL files tidak ditemukan: {missing}")
    for path in paths:
        text = path.read_text(encoding="utf-8").strip()
        without_blocks = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        executable = "\n".join(
            line for line in without_blocks.splitlines() if not line.lstrip().startswith("--")
        ).strip()
        if not executable.endswith(";"):
            raise OutputValidationError(f"SQL file tidak berakhir dengan semicolon: {path.name}")
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
    if "fact_sales" not in combined or "record_id" not in combined:
        raise OutputValidationError("SQL layer tidak konsisten dengan fact_sales/record_id.")
    return paths
