from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
COLOR_SEQUENCE = ["#0F766E", "#2563EB", "#D97706", "#7C3AED", "#DC2626"]


st.set_page_config(
    page_title="Restaurant Performance Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    clean = pd.read_csv(OUTPUT_DIR / "restaurant_sales_cleaned.csv", parse_dates=["date", "week_start"])
    return {
        "sales": clean,
        "kpis": pd.read_csv(OUTPUT_DIR / "kpis" / "executive_kpis.csv"),
        "daily": pd.read_csv(OUTPUT_DIR / "analysis" / "daily_performance.csv", parse_dates=["date"]),
        "products": pd.read_csv(OUTPUT_DIR / "analysis" / "product_performance.csv"),
        "categories": pd.read_csv(OUTPUT_DIR / "analysis" / "category_performance.csv"),
        "cities": pd.read_csv(OUTPUT_DIR / "analysis" / "city_performance.csv"),
        "payments": pd.read_csv(OUTPUT_DIR / "analysis" / "payment_method_performance.csv"),
        "purchase_types": pd.read_csv(OUTPUT_DIR / "analysis" / "purchase_type_performance.csv"),
        "day_of_week": pd.read_csv(OUTPUT_DIR / "analysis" / "day_of_week_performance.csv"),
        "concentration": pd.read_csv(OUTPUT_DIR / "analysis" / "revenue_concentration.csv"),
        "opportunities": pd.read_csv(OUTPUT_DIR / "insights" / "opportunity_matrix.csv"),
    }


def money(value: float) -> str:
    return f"{value:,.2f}"


def weighted_price(df: pd.DataFrame) -> float:
    quantity = float(df["quantity"].sum())
    return float(df["revenue"].sum() / quantity) if quantity else 0.0


def dimension_performance(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    result = (
        df.groupby(dimension, dropna=False)
        .agg(
            revenue=("revenue", "sum"),
            quantity=("quantity", "sum"),
            sales_records=("record_id", "nunique"),
            active_days=("date", "nunique"),
        )
        .reset_index()
    )
    result["weighted_selling_price"] = result["revenue"].div(result["quantity"])
    result["revenue_share"] = result["revenue"].div(result["revenue"].sum())
    return result


def style_app() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 0.8rem;}
        .grain-note {background:#fff7ed; border-left:4px solid #d97706; padding:.8rem 1rem; border-radius:.35rem; margin:.5rem 0 1.2rem 0;}
        .opportunity-card {border:1px solid #dbe3ec; border-radius:.8rem; padding:1rem; margin-bottom:.8rem; background:#ffffff;}
        .eyebrow {color:#0f766e; font-weight:700; text-transform:uppercase; letter-spacing:.08em; font-size:.78rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def unavailable_order_metrics() -> None:
    st.markdown(
        '<div class="grain-note"><strong>Order KPI tidak tersedia.</strong> '
        "Sumber hanya membuktikan satu record penjualan produk teragregasi. Total Orders dan AOV ditampilkan sebagai N/A agar tidak mengubah record menjadi pesanan pelanggan secara keliru.</div>",
        unsafe_allow_html=True,
    )


def executive_overview(data: dict[str, pd.DataFrame]) -> None:
    sales, daily, products = data["sales"], data["daily"], data["products"]
    st.subheader("Executive Overview")
    st.caption(
        "Ringkasan recorded revenue pada 7 November–29 Desember 2022; mata uang dan unit quantity tidak ditentukan sumber."
    )
    cols = st.columns(6)
    cols[0].metric("Recorded Revenue", money(sales["revenue"].sum()))
    cols[1].metric("Total Orders", "N/A", help="Tidak didukung oleh grain data.")
    cols[2].metric("AOV", "N/A", help="Tidak didukung oleh grain data.")
    cols[3].metric("Recorded Quantity", money(sales["quantity"].sum()))
    cols[4].metric("Sales Records", f"{sales['record_id'].nunique():,}")
    cols[5].metric("Weighted Price", money(weighted_price(sales)))
    unavailable_order_metrics()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["revenue"],
            mode="lines",
            name="Recorded revenue",
            line={"color": COLOR_SEQUENCE[1], "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["rolling_7_active_day_revenue"],
            mode="lines",
            name="7-active-day average",
            line={"color": COLOR_SEQUENCE[2], "width": 3},
        )
    )
    fig.update_layout(
        title="Recorded revenue varies by active sales day",
        xaxis_title="Date",
        yaxis_title="Recorded revenue (currency unspecified)",
        hovermode="x unified",
        legend_title_text="",
    )
    st.plotly_chart(fig, width="stretch")

    top = products.sort_values("revenue", ascending=False).iloc[0]
    st.markdown(
        f"""**Executive summary.** Recorded revenue totals **{money(sales["revenue"].sum())}** across **{sales["date"].nunique()} active sales days**. 
        **{top["product"]}** has the largest observed product contribution at **{top["revenue_share"]:.1%}**. The source supports mix, volume, weighted-price, location, channel, and time analysis—but not customer-order behavior, profit, or causal conclusions."""
    )


def revenue_drivers(data: dict[str, pd.DataFrame]) -> None:
    sales = data["sales"]
    st.subheader("Revenue Drivers")
    st.caption(
        "Revenue = recorded quantity × weighted selling price. Order Volume dan AOV tidak dapat dihitung pada grain yang tersedia."
    )
    a, b, c = st.columns([1, 0.25, 1])
    a.metric("Recorded Quantity", money(sales["quantity"].sum()))
    b.markdown("<h2 style='text-align:center;padding-top:1rem'>×</h2>", unsafe_allow_html=True)
    c.metric("Weighted Selling Price", money(weighted_price(sales)))
    st.metric("Recorded Revenue", money(sales["revenue"].sum()))
    unavailable_order_metrics()

    choices = {
        "Weekday vs Weekend": "is_weekend",
        "City": "city",
        "Payment": "payment_method",
        "Purchase Type": "purchase_type",
        "Category": "product_category",
    }
    label = st.selectbox("Bandingkan driver", list(choices))
    dimension = choices[label]
    perf = dimension_performance(
        sales.assign(is_weekend=sales["is_weekend"].map({True: "Weekend", False: "Weekday"})), dimension
    )
    perf = perf.sort_values("revenue", ascending=False)
    fig = px.bar(
        perf,
        x=dimension,
        y="revenue",
        color="weighted_selling_price",
        text_auto=".3s",
        color_continuous_scale="Tealgrn",
        title=f"Recorded revenue by {label.lower()}",
    )
    fig.update_layout(
        yaxis_title="Recorded revenue (currency unspecified)",
        xaxis_title=label,
        coloraxis_colorbar_title="Weighted price",
    )
    st.plotly_chart(fig, width="stretch")
    st.dataframe(
        perf.rename(columns={dimension: label}),
        width="stretch",
        hide_index=True,
        column_config={
            "revenue_share": st.column_config.ProgressColumn(
                "Revenue contribution", format="%.1%%", min_value=0, max_value=1
            )
        },
    )
    st.info(
        "Baca perubahan secara deskriptif: revenue yang lebih besar dapat diamati bersama quantity yang lebih tinggi, weighted price yang lebih tinggi, atau kombinasi keduanya. Data ini tidak membuktikan penyebab perubahan."
    )


def menu_intelligence(data: dict[str, pd.DataFrame]) -> None:
    products, categories = data["products"].copy(), data["categories"].copy()
    st.subheader("Menu Intelligence")
    sort_label = st.radio("Urutkan produk berdasarkan", ["Revenue", "Quantity", "Contribution"], horizontal=True)
    sort_col = {"Revenue": "revenue", "Quantity": "quantity", "Contribution": "revenue_share"}[sort_label]
    ranked = products.sort_values(sort_col, ascending=False)
    left, right = st.columns(2)
    with left:
        fig = px.bar(
            ranked,
            x=sort_col,
            y="product",
            orientation="h",
            color="product_category",
            text_auto=".3s",
            title=f"Product ranking by {sort_label.lower()}",
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, legend_title_text="Category")
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = px.bar(
            categories.sort_values("revenue"),
            x="revenue",
            y="product_category",
            orientation="h",
            text_auto=".3s",
            title="Category contribution to recorded revenue",
            color="product_category",
            color_discrete_sequence=COLOR_SEQUENCE,
        )
        fig.update_layout(showlegend=False, xaxis_title="Recorded revenue", yaxis_title="Category")
        st.plotly_chart(fig, width="stretch")

    pareto = products.sort_values("revenue", ascending=False)
    fig = go.Figure()
    fig.add_bar(x=pareto["product"], y=pareto["revenue"], name="Recorded revenue", marker_color=COLOR_SEQUENCE[1])
    fig.add_scatter(
        x=pareto["product"],
        y=pareto["cumulative_revenue_share"],
        name="Cumulative share",
        yaxis="y2",
        mode="lines+markers",
        line={"color": COLOR_SEQUENCE[2], "width": 3},
    )
    fig.update_layout(
        title="Three products account for at least 80% of recorded revenue",
        yaxis_title="Recorded revenue",
        yaxis2={
            "title": "Cumulative revenue share",
            "overlaying": "y",
            "side": "right",
            "tickformat": ".0%",
            "range": [0, 1.05],
        },
        legend_title_text="",
    )
    st.plotly_chart(fig, width="stretch")

    portfolio = px.scatter(
        products,
        x="quantity",
        y="revenue",
        size="revenue_share",
        color="portfolio_class",
        text="product",
        title="Product portfolio: recorded volume versus revenue",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    portfolio.update_traces(textposition="top center")
    portfolio.update_layout(
        xaxis_title="Recorded quantity (unit unspecified)",
        yaxis_title="Recorded revenue (currency unspecified)",
        legend_title_text="Portfolio class",
    )
    st.plotly_chart(portfolio, width="stretch")
    st.dataframe(ranked, width="stretch", hide_index=True)


def business_explorer(data: dict[str, pd.DataFrame]) -> None:
    sales = data["sales"]
    st.subheader("Business Explorer")
    st.caption("Filter record penjualan dan lihat kontribusi serta product mix pada scope terpilih.")
    f1, f2, f3 = st.columns(3)
    cities = f1.multiselect("City", sorted(sales["city"].unique()))
    managers = f2.multiselect("Manager", sorted(sales["manager"].unique()))
    payments = f3.multiselect("Payment", sorted(sales["payment_method"].unique()))
    f4, f5, f6 = st.columns(3)
    purchase = f4.multiselect("Purchase Type", sorted(sales["purchase_type"].unique()))
    categories = f5.multiselect("Category", sorted(sales["product_category"].unique()))
    dates = f6.date_input(
        "Date range",
        value=(sales["date"].min().date(), sales["date"].max().date()),
        min_value=sales["date"].min().date(),
        max_value=sales["date"].max().date(),
    )
    filtered = sales.copy()
    for col, values in [
        ("city", cities),
        ("manager", managers),
        ("payment_method", payments),
        ("purchase_type", purchase),
        ("product_category", categories),
    ]:
        if values:
            filtered = filtered[filtered[col].isin(values)]
    if isinstance(dates, (tuple, list)) and len(dates) == 2:
        filtered = filtered[filtered["date"].between(pd.Timestamp(dates[0]), pd.Timestamp(dates[1]))]
    if filtered.empty:
        st.warning("Tidak ada record untuk kombinasi filter ini.")
        return
    contribution = filtered["revenue"].sum() / sales["revenue"].sum()
    cols = st.columns(5)
    cols[0].metric("Revenue", money(filtered["revenue"].sum()))
    cols[1].metric("Orders", "N/A", help="Tidak didukung oleh grain data.")
    cols[2].metric("AOV", "N/A", help="Tidak didukung oleh grain data.")
    cols[3].metric("Quantity", money(filtered["quantity"].sum()))
    cols[4].metric("Contribution", f"{contribution:.1%}")
    mix = dimension_performance(filtered, "product").sort_values("revenue", ascending=False)
    fig = px.bar(
        mix,
        x="product",
        y="revenue",
        color="revenue_share",
        text_auto=".3s",
        title="Product mix within the selected scope",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis_title="Recorded revenue", xaxis_title="Product", coloraxis_colorbar_title="Scope share")
    st.plotly_chart(fig, width="stretch")
    st.dataframe(
        filtered[
            [
                "date",
                "record_id",
                "product",
                "product_category",
                "city",
                "manager",
                "purchase_type",
                "payment_method",
                "quantity",
                "revenue",
            ]
        ],
        width="stretch",
        hide_index=True,
    )


def opportunity_matrix(data: dict[str, pd.DataFrame]) -> None:
    opportunities = data["opportunities"].sort_values("priority_score", ascending=False)
    st.subheader("Opportunity Matrix")
    st.caption("Kandidat berbasis aturan untuk validasi lanjutan—bukan rekomendasi atau estimasi dampak yang terjamin.")
    dimensions = st.multiselect(
        "Filter opportunity dimension",
        sorted(opportunities["dimension"].unique()),
        default=sorted(opportunities["dimension"].unique()),
    )
    shown = opportunities[opportunities["dimension"].isin(dimensions)]
    fig = px.scatter(
        shown,
        x="priority_score",
        y="segment",
        color="dimension",
        size="priority_score",
        hover_data=["observation", "evidence_strength"],
        title="Priority score ranks evidence-review candidates",
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_title="Rule-based priority score (0–100)", yaxis_title="Candidate")
    st.plotly_chart(fig, width="stretch")
    for _, row in shown.iterrows():
        st.markdown(
            f"""<div class="opportunity-card"><div class="eyebrow">{row["dimension"]} · score {row["priority_score"]:.1f} · {row["evidence_strength"]}</div>
            <h3>{row["segment"]}</h3><p><strong>Observation</strong><br>{row["observation"]}</p>
            <p><strong>Evidence</strong><br>{row["metric_evidence"]}</p>
            <p><strong>Business hypothesis</strong><br>{row["business_hypothesis"]}</p>
            <p><strong>Next validation</strong><br>{row["recommended_validation_action"]}</p>
            <p><strong>Limitation</strong><br>{row["risk_or_limitation"]}</p></div>""",
            unsafe_allow_html=True,
        )


def main() -> None:
    style_app()
    data = load_data()
    st.markdown('<div class="eyebrow">Portfolio analytics case study</div>', unsafe_allow_html=True)
    st.title("Restaurant Performance Intelligence")
    st.markdown("Diagnosing the drivers of recorded restaurant revenue across menu, location, channel, and time.")
    tabs = st.tabs(
        ["Executive Overview", "Revenue Drivers", "Menu Intelligence", "Business Explorer", "Opportunity Matrix"]
    )
    with tabs[0]:
        executive_overview(data)
    with tabs[1]:
        revenue_drivers(data)
    with tabs[2]:
        menu_intelligence(data)
    with tabs[3]:
        business_explorer(data)
    with tabs[4]:
        opportunity_matrix(data)
    st.caption("Source period: 7 Nov–29 Dec 2022 · Currency and quantity unit unspecified · Revenue is not profit")


if __name__ == "__main__":
    main()
