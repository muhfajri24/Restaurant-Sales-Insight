"""KPI calculations that respect the verified dataset grain."""

from __future__ import annotations

import numpy as np
import pandas as pd


def safe_divide(numerator: float, denominator: float) -> float:
    """Return a deterministic zero for an empty denominator."""
    return float(numerator / denominator) if denominator else 0.0


def build_kpi_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Build supported KPIs and explicit nulls for unsupported order metrics."""
    revenue = float(data["revenue"].sum())
    quantity = float(data["quantity"].sum())
    active_days = int(data["date"].nunique())
    daily = data.groupby("date")["revenue"].sum()
    rows = [
        ("total_revenue", revenue, "supported"),
        ("total_orders", np.nan, "unsupported_grain"),
        ("total_line_items", np.nan, "unsupported_grain"),
        ("total_sales_records", len(data), "supported"),
        ("total_quantity_sold", quantity, "supported_as_recorded_measure"),
        ("average_order_value", np.nan, "unsupported_grain"),
        ("average_items_per_order", np.nan, "unsupported_grain"),
        ("average_selling_price", safe_divide(revenue, quantity), "supported_weighted_average"),
        ("active_sales_days", active_days, "supported"),
        ("average_daily_revenue", daily.mean(), "supported_active_days_only"),
        ("median_daily_revenue", daily.median(), "supported_active_days_only"),
    ]
    return pd.DataFrame(rows, columns=["metric", "value", "status"])
