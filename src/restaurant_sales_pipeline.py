from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "restaurant_sales_raw.csv"
OUTPUT_DIR = BASE_DIR / "output"
FIGURES_DIR = OUTPUT_DIR / "figures"
CLEANED_PATH = OUTPUT_DIR / "restaurant_sales_cleaned.csv"
KPI_PATH = OUTPUT_DIR / "kpi_summary.csv"


def load_raw_data(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_sales_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    text_columns = ["product", "purchase_type", "payment_method", "manager", "city"]
    for column in text_columns:
        df[column] = df[column].astype(str).str.replace(r"\s+", " ", regex=True).str.strip()

    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df = df.dropna(subset=["date", "product", "price", "quantity"])
    df = df.drop_duplicates(subset=["order_id"])

    df["revenue"] = (df["price"] * df["quantity"]).round(2)
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["day_name"] = df["date"].dt.day_name()
    df["week_num"] = df["date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["day_name"].isin(["Saturday", "Sunday"])

    category_map = {
        "beverages": "Beverage",
        "burgers": "Main Course",
        "chicken sandwiches": "Main Course",
        "fries": "Sides",
        "sides & other": "Sides",
    }
    df["product_category"] = (
        df["product"].str.lower().map(category_map).fillna("Other")
    )

    return df.sort_values("date").reset_index(drop=True)


def build_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    total_orders = df["order_id"].nunique()
    total_revenue = df["revenue"].sum()
    average_order_value = total_revenue / total_orders if total_orders else 0.0

    return pd.DataFrame(
        [
            {"metric": "Total Revenue", "value": round(total_revenue, 2)},
            {"metric": "Total Orders", "value": int(total_orders)},
            {"metric": "Average Order Value", "value": round(average_order_value, 2)},
        ]
    )


def export_figures(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", palette="Set2")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    daily_sales = df.groupby("date", as_index=False)["revenue"].sum()
    product_sales = (
        df.groupby("product", as_index=False)
        .agg(total_revenue=("revenue", "sum"))
        .sort_values("total_revenue", ascending=False)
    )
    category_sales = (
        df.groupby("product_category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    city_sales = (
        df.groupby("city", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    day_sales = df.groupby("day_name", as_index=False)["revenue"].sum()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_sales["day_name"] = pd.Categorical(day_sales["day_name"], categories=day_order, ordered=True)
    day_sales = day_sales.sort_values("day_name")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    sns.lineplot(data=daily_sales, x="date", y="revenue", marker="o", ax=axes[0, 0])
    axes[0, 0].set_title("Daily Revenue Trend")
    axes[0, 0].tick_params(axis="x", rotation=45)

    sns.barplot(data=product_sales, x="product", y="total_revenue", ax=axes[0, 1])
    axes[0, 1].set_title("Top Menu by Revenue")
    axes[0, 1].tick_params(axis="x", rotation=20)

    sns.barplot(data=category_sales, x="product_category", y="revenue", ax=axes[1, 0])
    axes[1, 0].set_title("Revenue by Category")

    sns.barplot(data=city_sales, x="city", y="revenue", ax=axes[1, 1])
    axes[1, 1].set_title("Revenue by City")
    axes[1, 1].tick_params(axis="x", rotation=20)

    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "sales_overview.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    plt.figure(figsize=(10, 5))
    sns.barplot(data=day_sales, x="day_name", y="revenue")
    plt.title("Revenue by Day of Week")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "sales_by_day.png", dpi=150, bbox_inches="tight")
    plt.close()


def run_pipeline() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = load_raw_data()
    clean_df = clean_sales_data(raw_df)
    kpi_df = build_kpi_summary(clean_df)

    clean_df.to_csv(CLEANED_PATH, index=False)
    kpi_df.to_csv(KPI_PATH, index=False)
    export_figures(clean_df)

    return {
        "rows": int(len(clean_df)),
        "total_orders": int(clean_df["order_id"].nunique()),
        "total_revenue": round(float(clean_df["revenue"].sum()), 2),
        "cleaned_path": str(CLEANED_PATH),
        "kpi_path": str(KPI_PATH),
        "figures_dir": str(FIGURES_DIR),
    }
