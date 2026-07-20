"""Backward-compatible public API for the modular production pipeline.

New code should import focused modules such as ``src.cleaning`` or
``src.analysis``. This façade preserves existing notebook and test imports.
"""

from src.analysis import (
    build_concentration,
    build_product_outputs,
    build_time_outputs,
)
from src.analysis import (
    dimension_table as _dimension_table,
)
from src.cleaning import clean_sales_data
from src.config import (
    BASE_DIR,
    DATA_PATH,
    DAY_ORDER,
    EXPECTED_COLUMNS,
    FIGURES_DIR,
    GRAIN_LABEL,
    MAPPING_PATH,
    ORDER_KPIS_SUPPORTED,
    OUTPUT_DIR,
    REPORTS_DIR,
    TEXT_COLUMNS,
)
from src.insights import build_opportunities
from src.kpis import build_kpi_summary
from src.pipeline import load_raw_data, run_pipeline
from src.validation import classify_duplicates, normalize_column_names, validate_data_contract
from src.visualization import export_figures

__all__ = [
    "BASE_DIR",
    "DATA_PATH",
    "DAY_ORDER",
    "EXPECTED_COLUMNS",
    "FIGURES_DIR",
    "GRAIN_LABEL",
    "MAPPING_PATH",
    "ORDER_KPIS_SUPPORTED",
    "OUTPUT_DIR",
    "REPORTS_DIR",
    "TEXT_COLUMNS",
    "_dimension_table",
    "build_concentration",
    "build_kpi_summary",
    "build_opportunities",
    "build_product_outputs",
    "build_time_outputs",
    "classify_duplicates",
    "clean_sales_data",
    "export_figures",
    "load_raw_data",
    "normalize_column_names",
    "run_pipeline",
    "validate_data_contract",
]
