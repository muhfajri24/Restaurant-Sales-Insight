"""Markdown and data-quality report exports."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config import GRAIN_LABEL, REPORTS_DIR
from src.io_utils import write_json, write_text


def export_reports(
    raw: pd.DataFrame,
    clean: pd.DataFrame,
    quality: dict[str, Any],
    duplicates: pd.DataFrame,
    outputs: dict[str, pd.DataFrame],
    concentration_summary: dict[str, dict[str, Any]],
    opportunities: pd.DataFrame,
) -> None:
    """Write reproducible reports from generated tables only."""
    grain = {
        "verified_grain": GRAIN_LABEL,
        "primary_key": "record_id (generated stable key)",
        "source_candidate_key": "order_id (unique in the supplied extract)",
        "order_level_kpis_supported": False,
        "row_count": len(raw),
        "unique_order_ids": int(raw.iloc[:, 0].nunique()),
        "exact_duplicate_extra_copies": int(raw.duplicated().sum()),
        "uncertainty": "The source label order_id does not prove a complete customer order; fractional high quantities indicate aggregated product sales records.",
    }
    write_json(REPORTS_DIR / "data_quality" / "data_grain_summary.json", grain)
    duplicates.to_csv(REPORTS_DIR / "data_quality" / "duplicate_record_analysis.csv", index=False)
    write_json(REPORTS_DIR / "data_quality" / "data_quality_summary.json", quality)
    write_text(
        REPORTS_DIR / "data_quality" / "data_grain_analysis.md",
        f"""# Data Grain Analysis

## Verified conclusion

The safest supported grain is **{GRAIN_LABEL}**. `order_id` is unique, but one product per row and fractional quantities from {clean["quantity"].min():.2f} to {clean["quantity"].max():.2f} do not establish customer-order grain.

- Raw rows: {len(raw)}
- Unique source order IDs: {raw.iloc[:, 0].nunique()}
- Exact duplicate extra copies: {raw.duplicated().sum()}
- Generated analytical primary key: `record_id`

Order count, AOV, and average items per order remain unsupported.""",
    )
    write_text(
        REPORTS_DIR / "data_quality" / "data_quality_report.md",
        f"""# Data Quality Report

The extract contains {quality["row_count"]} rows and {quality["column_count"]} columns from {quality["date_min"]} through {quality["date_max"]}. No required-value, date, nonpositive measure, or exact-duplicate issue was found. Whitespace variants are repaired transparently. Currency, quantity unit, and customer-order grain remain unknown.""",
    )
    write_text(
        REPORTS_DIR / "kpis" / "kpi_definitions.md",
        """# KPI Definitions

| KPI | Formula | Grain | Limitation |
|---|---|---|---|
| Total revenue | sum(price × quantity) | sales record | Currency, discount, tax, cost, and profit unknown |
| Total sales records | count distinct record_id | sales record | Not customer orders |
| Total quantity sold | sum(quantity) | sales record | Quantity unit undocumented |
| Average selling price | total revenue / total quantity | dataset | Not AOV |
| Active sales days | count distinct date | day | Unobserved calendar days excluded |
| Average/median daily revenue | aggregate active-day revenue | active day | Active days only |
| Total orders / AOV / items per order | not calculated | order | Unsupported grain |""",
    )
    pareto_lines = "\n".join(
        f"- **{name}**: {values['members_to_80_percent']} members reach 80% of recorded revenue; HHI={values['hhi']:.3f}."
        for name, values in concentration_summary.items()
    )
    write_text(
        REPORTS_DIR / "analysis" / "pareto_summary.md",
        f"# Pareto and Concentration Summary\n\n{pareto_lines}\n\nConcentration may support focus or indicate dependency; neither is confirmed without demand, cost, inventory, and capacity evidence.",
    )
    write_text(
        REPORTS_DIR / "analysis" / "manager_analysis_limitations.md",
        "# Manager Analysis Limitations\n\nManager results are descriptive and may be confounded by city, date coverage, traffic, menu mix, purchase type, staffing, and capacity.",
    )
    opportunity_lines = "\n".join(
        f"- **{row.segment} ({row.dimension})** — score {row.priority_score:.1f}: {row.observation}"
        for row in opportunities.head(8).itertuples(index=False)
    )
    write_text(
        REPORTS_DIR / "insights" / "opportunity_summary.md",
        f"# Opportunity Summary\n\nCandidates are deterministic validation hypotheses, not forecasts or confirmed recommendations.\n\n{opportunity_lines}",
    )
    write_text(
        REPORTS_DIR / "insights" / "executive_insight_brief.md",
        "# Executive Insight Brief\n\nRecorded revenue is analyzed as price × quantity at aggregated product-record grain. Customer-order behavior, profit, margin, retention, and causal impact cannot be inferred.",
    )
    write_text(
        REPORTS_DIR / "limitations.md",
        """# Limitations

- Currency and quantity unit are unknown.
- Recorded revenue is not profit; cost and margin are unavailable.
- Customer identifiers and order-level grain are unavailable.
- Manager comparisons are descriptive and potentially confounded.
- Transaction records do not prove causality.
- Historical 2022 data may not reflect current operations.""",
    )
    product = outputs["product_performance"].iloc[0]
    city = outputs["city_performance"].iloc[0]
    write_text(
        REPORTS_DIR / "restaurant_performance_summary.md",
        f"""# Restaurant Performance Intelligence

## Analytical Scope
Recorded performance from {clean["date"].min().date()} through {clean["date"].max().date()}.

## Validated Results
Recorded revenue is {clean["revenue"].sum():,.2f} across {len(clean)} sales records and {clean["date"].nunique()} active days. {product["product"]} has the largest product share ({product["revenue_share"]:.1%}); {city["city"]} has the largest city share ({city["revenue_share"]:.1%}).

## Interpretation
Revenue is decomposed into recorded quantity and weighted selling price. Order KPIs, profit, customer preference, and causal conclusions are unavailable.

## Decision Use
Use the opportunity matrix as a list of validation hypotheses, not guaranteed recommendations.""",
    )
