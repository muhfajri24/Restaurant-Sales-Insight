"""Deterministic static figures for reports and portfolio presentation."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.analysis import dimension_table
from src.config import FIGURE_DPI, FIGURES_DIR


def _save(name: str) -> None:
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / name, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close()


def _annotate(frame: pd.DataFrame, x: str, y: str, label: str) -> None:
    for row in frame.itertuples(index=False):
        plt.text(getattr(row, x), getattr(row, y), str(getattr(row, label)), fontsize=8)


def _trend_figures(outputs: dict[str, pd.DataFrame]) -> None:
    daily = outputs["daily_performance"]
    plt.figure(figsize=(11, 5))
    sns.lineplot(daily, x="date", y="revenue", label="Recorded revenue")
    sns.lineplot(daily, x="date", y="rolling_7_active_day_revenue", label="7-active-day average")
    plt.title("How did recorded revenue vary across active sales days?")
    plt.xlabel("Date")
    plt.ylabel("Recorded revenue (currency unspecified)")
    _save("executive_revenue_trend.png")


def _menu_figures(products: pd.DataFrame) -> None:
    products = products.sort_values("revenue", ascending=False)
    _, left = plt.subplots(figsize=(10, 5))
    left.bar(products["product"], products["revenue"], color="#2563EB")
    left.set_ylabel("Recorded revenue (currency unspecified)")
    left.tick_params(axis="x", rotation=18)
    right = left.twinx()
    right.plot(products["product"], products["cumulative_revenue_share"], color="#D97706", marker="o")
    right.set_ylabel("Cumulative revenue share")
    right.set_ylim(0, 1.05)
    left.set_title("How concentrated is recorded revenue across products?")
    _save("product_pareto.png")

    plt.figure(figsize=(9, 6))
    sns.scatterplot(products, x="quantity", y="revenue", hue="portfolio_class", s=140)
    _annotate(products, "quantity", "revenue", "product")
    plt.title("Which products combine recorded volume and revenue?")
    plt.xlabel("Recorded quantity (unit unspecified)")
    plt.ylabel("Recorded revenue (currency unspecified)")
    _save("product_portfolio_matrix.png")

    _, left = plt.subplots(figsize=(10, 5))
    left.bar(products["product"], products["revenue"], color="#2563EB")
    left.set_ylabel("Recorded revenue (currency unspecified)")
    left.tick_params(axis="x", rotation=18)
    right = left.twinx()
    right.plot(products["product"], products["cumulative_revenue_share"], color="#D97706", marker="o", linewidth=2.5)
    right.axhline(0.8, color="#64748B", linestyle="--", linewidth=1)
    right.set_ylabel("Cumulative revenue share")
    right.set_ylim(0, 1.05)
    left.set_title("Three products account for at least 80% of recorded revenue")
    _save("pareto_chart.png")

    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        products,
        x="quantity",
        y="revenue",
        hue="portfolio_class",
        size="revenue_share",
        sizes=(150, 700),
        palette="colorblind",
    )
    _annotate(products, "quantity", "revenue", "product")
    plt.title("Menu contribution reflects different volume and price combinations")
    plt.xlabel("Recorded quantity (unit unspecified)")
    plt.ylabel("Recorded revenue (currency unspecified)")
    _save("portfolio_matrix.png")


def _dimension_figures(data: pd.DataFrame, outputs: dict[str, pd.DataFrame]) -> None:
    city = outputs["city_performance"].sort_values("revenue", ascending=False)
    plt.figure(figsize=(9, 6))
    sns.scatterplot(city, x="quantity", y="average_selling_price", size="revenue", sizes=(100, 700))
    _annotate(city, "quantity", "average_selling_price", "city")
    plt.title("Do city results reflect volume or weighted selling price?")
    plt.xlabel("Recorded quantity (unit unspecified)")
    plt.ylabel("Weighted selling price (currency unspecified)")
    _save("city_volume_vs_aov.png")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        city,
        x="quantity",
        y="average_selling_price",
        size="revenue",
        sizes=(180, 850),
        color="#0F766E",
        alpha=0.78,
        legend=False,
    )
    for row in city.itertuples(index=False):
        plt.text(row.quantity, row.average_selling_price, f"{row.city} ({row.revenue_share:.1%})", fontsize=9)
    plt.title("City revenue positions separate recorded volume from weighted price")
    plt.xlabel("Recorded quantity (unit unspecified)")
    plt.ylabel("Weighted selling price (currency unspecified)")
    _save("city_analysis.png")

    purchase = outputs["purchase_type_performance"].sort_values("revenue", ascending=False)
    for name, title in [
        ("purchase_type_performance.png", "How is recorded revenue distributed by purchase type?"),
        ("channel_analysis.png", "Online records contribute the largest observed purchase-type share"),
    ]:
        plt.figure(figsize=(8, 5))
        sns.barplot(purchase, x="purchase_type", y="revenue", hue="purchase_type", legend=False)
        plt.title(title)
        plt.xlabel("Purchase type")
        plt.ylabel("Recorded revenue (currency unspecified)")
        _save(name)

    payment = outputs["payment_method_performance"].sort_values("revenue", ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(payment, x="payment_method", y="revenue", hue="payment_method", legend=False)
    plt.title("Credit card records hold the largest observed payment share")
    plt.xlabel("Payment method")
    plt.ylabel("Recorded revenue (currency unspecified)")
    _save("payment_analysis.png")

    weekend = dimension_table(data.assign(period=np.where(data["is_weekend"], "Weekend", "Weekday")), "period")
    plt.figure(figsize=(7, 5))
    sns.barplot(weekend, x="period", y="average_daily_revenue", hue="period", legend=False)
    plt.title("How does average active-day revenue compare?")
    plt.xlabel("")
    plt.ylabel("Average active-day revenue (currency unspecified)")
    _save("weekday_weekend_profile.png")


def _driver_figures(data: pd.DataFrame) -> None:
    driver = pd.DataFrame(
        {
            "driver": ["Sales records", "Recorded quantity", "Weighted selling price"],
            "index": [1.0, 1.0, 1.0],
        }
    )
    plt.figure(figsize=(9, 4))
    sns.barplot(driver, x="driver", y="index", hue="driver", legend=False)
    plt.title("Which observable components define recorded revenue?")
    plt.ylabel("Index (overall = 1.0)")
    _save("revenue_driver_decomposition.png")

    fig, axis = plt.subplots(figsize=(11, 4.5))
    axis.axis("off")
    quantity = data["quantity"].sum()
    weighted_price = data["revenue"].sum() / quantity
    boxes = [
        ("Recorded Quantity", f"{quantity:,.2f}", 0.18),
        ("Weighted Selling Price", f"{weighted_price:,.2f}", 0.50),
        ("Recorded Revenue", f"{data['revenue'].sum():,.2f}", 0.82),
    ]
    for label, value, x_pos in boxes:
        axis.text(
            x_pos,
            0.55,
            f"{value}\n{label}",
            ha="center",
            va="center",
            fontsize=13,
            bbox={"boxstyle": "round,pad=.8", "facecolor": "#ECFDF5", "edgecolor": "#0F766E"},
        )
    axis.text(0.34, 0.55, "×", ha="center", va="center", fontsize=24, color="#D97706")
    axis.text(0.66, 0.55, "=", ha="center", va="center", fontsize=24, color="#D97706")
    axis.set_title("Recorded revenue is observed through quantity and weighted selling price", pad=20)
    axis.text(0.5, 0.14, "Order volume and AOV are unsupported by the verified grain.", ha="center")
    fig.savefig(FIGURES_DIR / "revenue_drivers.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)


def _executive_kpis(data: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.4))
    metrics = [
        ("Recorded Revenue", f"{data['revenue'].sum():,.2f}"),
        ("Sales Records", f"{data['record_id'].nunique():,}"),
        ("Recorded Quantity", f"{data['quantity'].sum():,.2f}"),
        ("Weighted Price", f"{data['revenue'].sum() / data['quantity'].sum():,.2f}"),
        ("Active Days", f"{data['date'].nunique():,}"),
    ]
    for axis, (label, value) in zip(axes, metrics, strict=True):
        axis.axis("off")
        axis.text(0.5, 0.62, value, ha="center", fontsize=17, fontweight="bold", color="#0F766E")
        axis.text(0.5, 0.30, label, ha="center", fontsize=9, color="#334155")
    fig.suptitle("What is the validated scale of recorded restaurant performance?")
    fig.text(
        0.5, 0.02, "Currency and quantity units are unspecified; customer-order KPIs are unavailable.", ha="center"
    )
    fig.savefig(FIGURES_DIR / "executive_kpis.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)


def _concentration_figures(outputs: dict[str, pd.DataFrame], opportunities: pd.DataFrame) -> None:
    concentration = outputs["revenue_concentration"]
    product = concentration[concentration["dimension"].eq("product")]
    plt.figure(figsize=(9, 5))
    sns.barplot(product, x="member", y="revenue_share", hue="member", legend=False)
    plt.title("What share of recorded revenue comes from each product?")
    plt.xlabel("Product")
    plt.ylabel("Revenue share")
    plt.xticks(rotation=20)
    _save("revenue_concentration.png")

    top = opportunities.sort_values("priority_score", ascending=False).head(10)
    plt.figure(figsize=(9, 5))
    sns.barplot(top, y="segment", x="priority_score", hue="dimension", dodge=False)
    plt.title("Which evidence-based hypotheses merit validation first?")
    plt.xlabel("Rule-based priority score (0–100)")
    plt.ylabel("Candidate segment")
    _save("opportunity_priority_matrix.png")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(top, x="priority_score", y="segment", hue="dimension", s=190)
    plt.title("Evidence-review candidates are prioritized, not guaranteed recommendations")
    plt.xlabel("Rule-based priority score (0–100)")
    plt.ylabel("Candidate segment")
    _save("opportunity_matrix.png")


def export_figures(
    data: pd.DataFrame,
    outputs: dict[str, pd.DataFrame],
    opportunities: pd.DataFrame,
) -> None:
    """Generate all required noninteractive figures from validated outputs."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="colorblind")
    _trend_figures(outputs)
    _driver_figures(data)
    _menu_figures(outputs["product_performance"])
    _dimension_figures(data, outputs)
    _executive_kpis(data)
    _concentration_figures(outputs, opportunities)
