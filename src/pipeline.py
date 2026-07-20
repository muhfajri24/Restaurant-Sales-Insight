"""Production orchestration for the restaurant performance pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.analysis import (
    build_concentration,
    build_product_outputs,
    build_time_outputs,
    dimension_table,
)
from src.cleaning import clean_sales_data
from src.config import DATA_PATH, OUTPUT_DIR, REPORTS_DIR
from src.exceptions import InputFileNotFoundError
from src.insights import build_business_insights, build_opportunities
from src.io_utils import ensure_output_directories, write_json
from src.kpis import build_kpi_summary
from src.metadata import build_project_metadata
from src.reporting import export_reports
from src.sql_exports import validate_sql_layer
from src.validation import validate_data_contract
from src.visualization import export_figures


def load_raw_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the preserved source extract with a specific missing-file error."""
    if not path.is_file():
        raise InputFileNotFoundError(
            f"Raw dataset tidak ditemukan: {path}. Letakkan source CSV pada data/restaurant_sales_raw.csv."
        )
    return pd.read_csv(path)


def _export_quality_and_taxonomy(
    clean: pd.DataFrame,
    audit: pd.DataFrame,
    removed: pd.DataFrame,
    flagged: pd.DataFrame,
    invalid: pd.DataFrame,
) -> None:
    clean.to_csv(OUTPUT_DIR / "restaurant_sales_cleaned.csv", index=False)
    audit.to_csv(OUTPUT_DIR / "cleaning_audit.csv", index=False)
    removed.to_csv(OUTPUT_DIR / "removed_records.csv", index=False)
    flagged.to_csv(OUTPUT_DIR / "flagged_records.csv", index=False)
    invalid.to_csv(REPORTS_DIR / "data_quality" / "invalid_records.csv", index=False)
    standardization = clean[["product_original", "product", "product_category"]].drop_duplicates()
    standardization.sort_values("product").to_csv(
        REPORTS_DIR / "data_quality" / "category_standardization.csv", index=False
    )
    coverage = (
        clean.groupby(["product_original", "product", "product_category"], dropna=False)
        .agg(records=("record_id", "count"), revenue=("revenue", "sum"))
        .reset_index()
    )
    coverage["mapping_status"] = np.where(coverage["product_category"].eq("Other"), "unmapped", "mapped")
    coverage.to_csv(REPORTS_DIR / "product_taxonomy" / "product_coverage.csv", index=False)
    coverage[coverage["mapping_status"].eq("unmapped")].to_csv(
        REPORTS_DIR / "product_taxonomy" / "unmapped_products.csv", index=False
    )


def _build_analysis_outputs(clean: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, Any]]]:
    outputs = {**build_time_outputs(clean), **build_product_outputs(clean)}
    dimensions = {
        "city": "city_performance",
        "purchase_type": "purchase_type_performance",
        "payment_method": "payment_method_performance",
        "manager": "manager_observed_performance",
    }
    for dimension, name in dimensions.items():
        outputs[name] = dimension_table(clean, dimension)
    outputs["city_driver_decomposition"] = outputs["city_performance"].copy()
    frames = []
    for dimension in [
        "month",
        "day_name",
        "is_weekend",
        "city",
        "purchase_type",
        "payment_method",
        "manager",
        "product",
        "product_category",
    ]:
        frame = dimension_table(clean, dimension)
        frame.insert(0, "dimension", dimension)
        frame.rename(columns={dimension: "member"}, inplace=True)
        frames.append(frame)
    outputs["dimension_performance"] = pd.concat(frames, ignore_index=True)
    outputs["revenue_driver_summary"] = pd.DataFrame(
        [
            {
                "component": "recorded_quantity",
                "value": clean["quantity"].sum(),
                "interpretation": "Recorded volume; unit unspecified.",
            },
            {
                "component": "weighted_selling_price",
                "value": clean["revenue"].sum() / clean["quantity"].sum(),
                "interpretation": "Revenue divided by recorded quantity.",
            },
            {
                "component": "sales_records",
                "value": len(clean),
                "interpretation": "Aggregated product records, not proven customer orders.",
            },
        ]
    )
    concentration, summary = build_concentration(clean)
    outputs["revenue_concentration"] = concentration
    return outputs, summary


def _export_analysis_and_bi(clean: pd.DataFrame, outputs: dict[str, pd.DataFrame]) -> None:
    for name, frame in outputs.items():
        frame.to_csv(OUTPUT_DIR / "analysis" / f"{name}.csv", index=False)
    fact_columns = [
        "record_id",
        "order_id",
        "date",
        "product",
        "city",
        "purchase_type",
        "payment_method",
        "manager",
        "price",
        "quantity",
        "revenue",
    ]
    clean[fact_columns].to_csv(OUTPUT_DIR / "bi" / "fact_sales.csv", index=False)
    dates = pd.DataFrame({"date": pd.date_range(clean["date"].min(), clean["date"].max())})
    dates = dates.assign(
        year=dates["date"].dt.year,
        month=dates["date"].dt.to_period("M").astype(str),
        day_name=dates["date"].dt.day_name(),
        is_weekend=dates["date"].dt.weekday.ge(5),
    )
    dates.to_csv(OUTPUT_DIR / "bi" / "dim_date.csv", index=False)
    clean[["product", "product_category"]].drop_duplicates().to_csv(OUTPUT_DIR / "bi" / "dim_product.csv", index=False)
    clean[["city"]].drop_duplicates().to_csv(OUTPUT_DIR / "bi" / "dim_location.csv", index=False)
    clean[["purchase_type", "payment_method"]].drop_duplicates().to_csv(
        OUTPUT_DIR / "bi" / "dim_channel.csv", index=False
    )


def run_pipeline(data_path: Path = DATA_PATH) -> dict[str, object]:
    """Run validation, cleaning, analytics, reports, figures, BI, and metadata."""
    ensure_output_directories()
    validate_sql_layer()
    raw = load_raw_data(data_path)
    invalid, duplicates, quality = validate_data_contract(raw)
    clean, audit, removed, flagged = clean_sales_data(raw)
    _export_quality_and_taxonomy(clean, audit, removed, flagged, invalid)
    kpis = build_kpi_summary(clean)
    kpis.to_csv(OUTPUT_DIR / "kpis" / "executive_kpis.csv", index=False)
    kpis.to_csv(OUTPUT_DIR / "kpi_summary.csv", index=False)
    outputs, concentration_summary = _build_analysis_outputs(clean)
    opportunities = build_opportunities(clean, outputs["product_performance"])
    opportunities.to_csv(OUTPUT_DIR / "insights" / "opportunity_matrix.csv", index=False)
    build_business_insights(opportunities).to_csv(OUTPUT_DIR / "insights" / "business_insights.csv", index=False)
    _export_analysis_and_bi(clean, outputs)
    export_reports(raw, clean, quality, duplicates, outputs, concentration_summary, opportunities)
    export_figures(clean, outputs, opportunities)
    write_json(
        OUTPUT_DIR / "project_metadata.json",
        build_project_metadata(raw, clean, removed, flagged, kpis),
    )
    return {
        "rows": len(clean),
        "total_orders": None,
        "total_revenue": round(float(clean["revenue"].sum()), 2),
        "cleaned_path": str(OUTPUT_DIR / "restaurant_sales_cleaned.csv"),
        "kpi_path": str(OUTPUT_DIR / "kpis" / "executive_kpis.csv"),
        "figures_dir": str(OUTPUT_DIR / "figures"),
    }
