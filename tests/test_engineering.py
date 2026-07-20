from pathlib import Path

import pandas as pd
import pytest

from src.analysis import dimension_table
from src.cleaning import clean_sales_data
from src.exceptions import InputFileNotFoundError, ProductMappingError
from src.pipeline import load_raw_data


@pytest.fixture
def synthetic_sales() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [1, "01-01-2024", "Burgers", 10, 2, "Online", "Cash", "Manager A", "City A"],
            [2, "02-01-2024", "Fries", 5, 3, "In-store", "Credit Card", "Manager A", "City A"],
            [3, "03-01-2024", "Beverages", 2, 4, "Drive-thru", "Gift Card", "Manager B", "City B"],
        ],
        columns=[
            "Order ID", "Date", "Product", "Price", "Quantity", "Purchase Type",
            "Payment Method", "Manager", "City",
        ],
    )


def test_missing_raw_file_has_specific_error(tmp_path: Path) -> None:
    with pytest.raises(InputFileNotFoundError, match="Raw dataset tidak ditemukan"):
        load_raw_data(tmp_path / "missing.csv")


def test_missing_mapping_has_specific_error(synthetic_sales: pd.DataFrame, tmp_path: Path) -> None:
    with pytest.raises(ProductMappingError, match="mapping produk tidak ditemukan"):
        clean_sales_data(synthetic_sales, tmp_path / "missing_mapping.csv")


def test_malformed_mapping_has_specific_error(synthetic_sales: pd.DataFrame, tmp_path: Path) -> None:
    mapping = tmp_path / "mapping.csv"
    pd.DataFrame({"product_standardized": ["Burgers"]}).to_csv(mapping, index=False)
    with pytest.raises(ProductMappingError, match="harus memiliki kolom"):
        clean_sales_data(synthetic_sales, mapping)


@pytest.mark.parametrize("dimension", ["city", "payment_method", "manager"])
def test_dimension_revenue_and_contribution_reconcile(
    synthetic_sales: pd.DataFrame,
    dimension: str,
) -> None:
    clean, _, _, _ = clean_sales_data(synthetic_sales)
    result = dimension_table(clean, dimension)
    assert result["revenue"].sum() == pytest.approx(clean["revenue"].sum())
    assert result["revenue_share"].sum() == pytest.approx(1.0)
