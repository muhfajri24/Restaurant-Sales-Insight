import json

import numpy as np
import pandas as pd
import pytest

from src.project_validation import validate_project
from src.restaurant_sales_pipeline import (
    BASE_DIR,
    build_concentration,
    build_kpi_summary,
    build_opportunities,
    build_product_outputs,
    build_time_outputs,
    classify_duplicates,
    clean_sales_data,
    normalize_column_names,
    run_pipeline,
    validate_data_contract,
)


@pytest.fixture
def sample():
    return pd.DataFrame(
        [
            [1, "01-01-2024", "Burgers", 10, 2, " Online ", " Cash", " A  Manager ", "City A"],
            [2, "02-01-2024", "Fries", 5, 3, "In-store", "Credit Card", "A Manager", "City A"],
            [3, "03-01-2024", "Beverages", 2, 4, "Drive-thru", "Gift Card", "B Manager", "City B"],
        ],
        columns=[
            "Order ID",
            "Date",
            "Product",
            "Price",
            "Quantity",
            "Purchase Type",
            "Payment Method",
            "Manager",
            "City",
        ],
    )


def test_required_columns(sample):
    assert validate_data_contract(sample)[2]["missing_columns"] == []


def test_missing_required_column(sample):
    with pytest.raises(ValueError):
        clean_sales_data(sample.drop(columns="City"))


def test_column_normalization():
    assert normalize_column_names([" Order ID ", "Payment-Method"]) == ["order_id", "payment_method"]


def test_date_parsing(sample):
    assert clean_sales_data(sample)[0]["date"].notna().all()


def test_numeric_parsing(sample):
    sample["Price"] = "10"
    assert clean_sales_data(sample)[0]["price"].dtype.kind in "fi"


def test_missing_text_handling(sample):
    sample.loc[0, "Product"] = None
    assert len(clean_sales_data(sample)[2]) == 1


def test_exact_duplicate_detection(sample):
    d = pd.concat([sample, sample.iloc[[0]]], ignore_index=True)
    assert (classify_duplicates(d)["classification"] == "exact_duplicate_row").any()


def test_valid_repeated_order_lines_preserved(sample):
    sample.loc[1, "Order ID"] = 1
    clean = clean_sales_data(sample)[0]
    assert len(clean) == 3


def test_conflicting_order_records_flagged(sample):
    sample.loc[1, "Order ID"] = 1
    assert (classify_duplicates(sample)["classification"] == "conflicting_duplicate_record").any()


def test_invalid_price(sample):
    sample.loc[0, "Price"] = -1
    assert "negative_price" in validate_data_contract(sample)[0].iloc[0]["validation_issues"]


def test_invalid_quantity(sample):
    sample.loc[0, "Quantity"] = 0
    assert "zero_quantity" in validate_data_contract(sample)[0].iloc[0]["validation_issues"]


def test_revenue_calculation(sample):
    assert clean_sales_data(sample)[0].iloc[0]["revenue"] == 20


def test_product_mapping_coverage(sample):
    assert not clean_sales_data(sample)[0]["product_category"].eq("Other").any()


def test_kpi_formulas(sample):
    clean = clean_sales_data(sample)[0]
    k = build_kpi_summary(clean).set_index("metric")
    assert k.loc["total_revenue", "value"] == 43


def test_aov_is_unsupported(sample):
    assert np.isnan(
        build_kpi_summary(clean_sales_data(sample)[0]).set_index("metric").loc["average_order_value", "value"]
    )


def test_dimension_aggregation(sample):
    clean = clean_sales_data(sample)[0]
    assert build_product_outputs(clean)["product_performance"]["revenue"].sum() == clean["revenue"].sum()


def test_period_ordering(sample):
    assert build_time_outputs(clean_sales_data(sample)[0])["daily_performance"]["date"].is_monotonic_increasing


def test_incomplete_period_flagging(sample):
    assert build_time_outputs(clean_sales_data(sample)[0])["monthly_performance"]["is_partial_period"].all()


def test_pareto_monotonic(sample):
    clean = clean_sales_data(sample)[0]
    c, _ = build_concentration(clean)
    p = c[c.dimension == "product"]
    assert p.cumulative_revenue_share.is_monotonic_increasing


def test_concentration_ends_at_one(sample):
    clean = clean_sales_data(sample)[0]
    _, s = build_concentration(clean)
    assert 0 < s["product"]["hhi"] <= 1


def test_opportunity_rule_output(sample):
    clean = clean_sales_data(sample)[0]
    assert set(build_opportunities(clean, build_product_outputs(clean)["product_performance"]).columns) >= {
        "observation",
        "priority_score",
    }


def test_no_unsupported_profit_field(sample):
    assert not any("profit" in c for c in clean_sales_data(sample)[0].columns)


def test_generated_output_schemas():
    run_pipeline()
    fact = pd.read_csv(BASE_DIR / "output/bi/fact_sales.csv")
    assert {"record_id", "date", "revenue"} <= set(fact.columns)


def test_project_metadata_and_no_absolute_paths():
    run_pipeline()
    p = BASE_DIR / "output/project_metadata.json"
    data = json.loads(p.read_text())
    assert data["currency_status"] == "unknown" and str(BASE_DIR) not in p.read_text()


def test_phase_one_project_validation():
    run_pipeline()
    result = validate_project()
    assert result["status"] == "passed" and result["checks_passed"] == result["checks_total"]
