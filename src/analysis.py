"""Reusable time, dimension, menu, and concentration aggregations."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.config import DAY_ORDER


def dimension_table(data: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Aggregate supported measures for one categorical dimension."""
    if dimension not in data.columns:
        raise KeyError(f"Dimension tidak tersedia: {dimension}")
    result = (
        data.groupby(dimension, dropna=False)
        .agg(
            revenue=("revenue", "sum"),
            sales_records=("record_id", "nunique"),
            quantity=("quantity", "sum"),
            active_sales_days=("date", "nunique"),
        )
        .reset_index()
    )
    result["average_selling_price"] = result["revenue"].div(result["quantity"])
    result["average_daily_revenue"] = result["revenue"].div(result["active_sales_days"])
    result["revenue_share"] = result["revenue"].div(data["revenue"].sum())
    result["record_share"] = result["sales_records"].div(data["record_id"].nunique())
    result["quantity_share"] = result["quantity"].div(data["quantity"].sum())
    return result.sort_values("revenue", ascending=False).reset_index(drop=True)


def build_time_outputs(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create ordered daily, weekly, monthly, and weekday outputs."""
    daily = (
        data.groupby("date")
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            sales_records=("record_id", "nunique"),
        )
        .reset_index()
        .sort_values("date")
    )
    daily["rolling_7_active_day_revenue"] = daily["revenue"].rolling(7, min_periods=1).mean()
    daily["revenue_change"] = daily["revenue"].pct_change()
    weekly = (
        data.groupby("week_start")
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            sales_records=("record_id", "nunique"),
            active_sales_days=("date", "nunique"),
        )
        .reset_index()
        .sort_values("week_start")
    )
    weekly["is_partial_period"] = weekly["active_sales_days"].lt(7)
    weekly["revenue_growth"] = weekly["revenue"].pct_change()
    monthly = (
        data.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            sales_records=("record_id", "nunique"),
            active_sales_days=("date", "nunique"),
            period_start=("date", "min"),
            period_end=("date", "max"),
        )
        .reset_index()
        .sort_values("month")
    )
    monthly["calendar_days_in_month"] = pd.to_datetime(monthly["period_start"]).dt.days_in_month
    monthly["is_partial_period"] = pd.to_datetime(monthly["period_start"]).dt.day.ne(1) | pd.to_datetime(
        monthly["period_end"]
    ).dt.day.ne(monthly["calendar_days_in_month"])
    monthly["revenue_growth"] = monthly["revenue"].pct_change()
    monthly["daily_revenue_mean"] = monthly["revenue"].div(monthly["active_sales_days"])
    weekday = dimension_table(data, "day_name")
    weekday["day_name"] = pd.Categorical(weekday["day_name"], DAY_ORDER, ordered=True)
    weekday = weekday.sort_values("day_name")
    return {
        "daily_performance": daily,
        "weekly_performance": weekly,
        "monthly_performance": monthly,
        "day_of_week_performance": weekday,
    }


def build_product_outputs(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create product, category, and portfolio analysis outputs."""
    product = dimension_table(data, "product")
    category_map = data.drop_duplicates("product").set_index("product")["product_category"]
    product["product_category"] = product["product"].map(category_map)
    product["average_price"] = data.groupby("product")["price"].mean().reindex(product["product"]).values
    product["rank_by_revenue"] = product["revenue"].rank(method="dense", ascending=False).astype(int)
    product["rank_by_quantity"] = product["quantity"].rank(method="dense", ascending=False).astype(int)
    product = product.sort_values("revenue", ascending=False)
    product["cumulative_revenue_share"] = product["revenue_share"].cumsum()
    weekend = data.groupby("product").apply(
        lambda frame: frame.loc[frame["is_weekend"], "revenue"].sum(), include_groups=False
    )
    product["weekend_revenue_share"] = product["product"].map(weekend).fillna(0).div(product["revenue"])
    revenue_median, quantity_median = product["revenue"].median(), product["quantity"].median()
    product["portfolio_class"] = "low revenue / low volume"
    product.loc[product["revenue"].ge(revenue_median) & product["quantity"].ge(quantity_median), "portfolio_class"] = (
        "high revenue / high volume"
    )
    product.loc[product["revenue"].ge(revenue_median) & product["quantity"].lt(quantity_median), "portfolio_class"] = (
        "high revenue / low volume"
    )
    product.loc[product["revenue"].lt(revenue_median) & product["quantity"].ge(quantity_median), "portfolio_class"] = (
        "low revenue / high volume"
    )
    portfolio = product[["product", "revenue", "quantity", "revenue_share", "quantity_share", "portfolio_class"]].copy()
    return {
        "product_performance": product,
        "category_performance": dimension_table(data, "product_category"),
        "product_portfolio_matrix": portfolio,
    }


def build_concentration(data: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, dict[str, Any]]]:
    """Build cumulative revenue shares and HHI by supported dimension."""
    rows: list[dict[str, Any]] = []
    summary: dict[str, dict[str, Any]] = {}
    for dimension in ["product", "product_category", "city", "purchase_type"]:
        grouped = data.groupby(dimension)["revenue"].sum().sort_values(ascending=False)
        shares = grouped / grouped.sum()
        cumulative = shares.cumsum()
        for rank, (member, value) in enumerate(grouped.items(), 1):
            rows.append(
                {
                    "dimension": dimension,
                    "member": member,
                    "rank": rank,
                    "revenue": value,
                    "revenue_share": shares.loc[member],
                    "cumulative_revenue_share": cumulative.loc[member],
                }
            )
        summary[dimension] = {
            "members_to_50_percent": int(cumulative.lt(0.5).sum() + 1),
            "members_to_80_percent": int(cumulative.lt(0.8).sum() + 1),
            "members_to_90_percent": int(cumulative.lt(0.9).sum() + 1),
            "top_3_share": float(shares.head(3).sum()),
            "top_5_share": float(shares.head(5).sum()),
            "hhi": float(shares.pow(2).sum()),
        }
    return pd.DataFrame(rows), summary
