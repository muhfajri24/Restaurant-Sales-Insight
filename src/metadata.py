"""Portable project metadata generation."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config import GRAIN_LABEL


def build_project_metadata(
    raw: pd.DataFrame,
    clean: pd.DataFrame,
    removed: pd.DataFrame,
    flagged: pd.DataFrame,
    kpis: pd.DataFrame,
) -> dict[str, Any]:
    """Create metadata without machine-local paths or invented business fields."""
    return {
        "dataset_source": "Kaggle dataset rohitgrewal/restaurant-sales-data (per repository documentation)",
        "dataset_grain": GRAIN_LABEL,
        "primary_key": "record_id",
        "source_candidate_key": "order_id",
        "date_range": {"start": str(clean["date"].min().date()), "end": str(clean["date"].max().date())},
        "row_count_before_cleaning": len(raw),
        "row_count_after_cleaning": len(clean),
        "removed_record_count": len(removed),
        "flagged_record_count": len(flagged),
        "total_orders": None,
        "total_revenue": round(float(clean["revenue"].sum()), 2),
        "currency_status": "unknown",
        "product_mapping_coverage": float(
            clean.loc[clean["product_category"].ne("Other"), "revenue"].sum() / clean["revenue"].sum()
        ),
        "generated_kpi_list": kpis["metric"].tolist(),
        "generated_analytical_dimensions": [
            "time",
            "product",
            "product_category",
            "city",
            "purchase_type",
            "payment_method",
            "manager",
        ],
        "dashboard": "app.py",
        "phase_2_artifacts": [
            "reports/validation/project_validation.md",
            "reports/storytelling/executive_story.md",
            "docs/DASHBOARD_GUIDE.md",
        ],
        "limitations": [
            "Order-level KPIs unsupported",
            "Currency unknown",
            "Quantity unit unknown",
            "Revenue is not profit",
            "No customer identifiers",
            "No causal design",
        ],
    }
