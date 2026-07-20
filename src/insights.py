"""Deterministic, evidence-bounded opportunity rules."""

from __future__ import annotations

import pandas as pd

from src.analysis import dimension_table

OPPORTUNITY_COLUMNS = [
    "dimension",
    "segment",
    "observation",
    "metric_evidence",
    "business_hypothesis",
    "recommended_validation_action",
    "risk_or_limitation",
    "priority_score",
    "evidence_strength",
]


def build_opportunities(data: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Rank validation hypotheses without forecasting impact or causality."""
    rows: list[dict[str, object]] = []
    overall_price = float(data["revenue"].sum() / data["quantity"].sum())
    for dimension in ["city", "purchase_type", "day_name"]:
        performance = dimension_table(data, dimension)
        volume_median = performance["quantity"].median()
        for _, row in performance.iterrows():
            if row["quantity"] >= volume_median and row["average_selling_price"] < overall_price:
                gap = (overall_price - row["average_selling_price"]) / overall_price
                rows.append(
                    {
                        "dimension": dimension,
                        "segment": row[dimension],
                        "observation": "Recorded volume is at or above the dimension median while weighted selling price is below the overall average.",
                        "metric_evidence": f"quantity={row['quantity']:.2f}; weighted_price={row['average_selling_price']:.2f}; baseline={overall_price:.2f}",
                        "business_hypothesis": "The observed mix may contain a larger share of lower-priced products.",
                        "recommended_validation_action": "Review product mix, price realization, discounting, and cost/capacity data before acting.",
                        "risk_or_limitation": "Aggregated records do not identify customers, individual orders, discounts, or costs.",
                        "priority_score": round(min(100, 50 + gap * 100), 1),
                        "evidence_strength": "moderate",
                    }
                )
    for _, row in products.head(3).iterrows():
        if row["revenue_share"] >= 0.15:
            rows.append(
                {
                    "dimension": "product",
                    "segment": row["product"],
                    "observation": "The product represents a material share of recorded revenue.",
                    "metric_evidence": f"revenue_share={row['revenue_share']:.1%}; cumulative_share={row['cumulative_revenue_share']:.1%}",
                    "business_hypothesis": "Concentration may simplify operational focus while increasing dependency on a limited menu set.",
                    "recommended_validation_action": "Validate contribution margin, inventory resilience, substitution, and demand stability.",
                    "risk_or_limitation": "Revenue concentration is neither profit nor evidence of operational risk by itself.",
                    "priority_score": round(50 + row["revenue_share"] * 100, 1),
                    "evidence_strength": "strong_descriptive",
                }
            )
    return (
        pd.DataFrame(rows, columns=OPPORTUNITY_COLUMNS)
        .sort_values("priority_score", ascending=False)
        .reset_index(drop=True)
    )


def build_business_insights(opportunities: pd.DataFrame) -> pd.DataFrame:
    """Convert opportunity rows to the stable business-insight schema."""
    insights = opportunities.rename(
        columns={
            "segment": "title",
            "metric_evidence": "supporting_metric",
            "business_hypothesis": "possible_explanation",
            "recommended_validation_action": "recommended_next_analysis",
            "risk_or_limitation": "limitation",
        }
    ).copy()
    insights["business_dimension"] = insights["dimension"]
    insights["comparison_baseline"] = "See supporting_metric"
    return insights
