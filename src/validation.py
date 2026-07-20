"""Schema, value, and duplicate validation for raw restaurant records."""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

import pandas as pd

from src.config import DATE_FORMAT, EXPECTED_COLUMNS, TEXT_COLUMNS
from src.exceptions import SchemaValidationError


def normalize_column_names(columns: Iterable[object]) -> list[str]:
    """Convert arbitrary headings to stable snake_case names."""
    return [
        re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(column).strip().lower())).strip("_") for column in columns
    ]


def clean_text(series: pd.Series) -> pd.Series:
    """Normalize whitespace while preserving missing text as nullable strings."""
    result = series.astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
    return result.mask(result.str.lower().isin(["", "nan", "none", "null", "n/a"]))


def require_columns(frame: pd.DataFrame) -> None:
    """Raise a specific schema error when required columns are missing."""
    missing = sorted(set(EXPECTED_COLUMNS) - set(frame.columns))
    if missing:
        raise SchemaValidationError(
            f"Kolom wajib tidak ditemukan: {missing}. Kolom yang tersedia: {sorted(frame.columns)}"
        )


def classify_duplicates(frame: pd.DataFrame) -> pd.DataFrame:
    """Classify exact, possible line-item, conflicting, and uncertain duplicates."""
    work = frame.copy()
    work.columns = normalize_column_names(work.columns)
    require_columns(work)
    rows: list[dict[str, Any]] = []
    for index in work.index[work.duplicated(keep=False)]:
        rows.append(
            {
                "source_row_number": int(index) + 2,
                "order_id": work.at[index, "order_id"],
                "classification": "exact_duplicate_row",
                "details": "All supplied fields repeat.",
            }
        )
    for order_id, group in work.groupby("order_id", dropna=False):
        if len(group) < 2 or group.duplicated(keep=False).all():
            continue
        product_count = group["product"].nunique(dropna=False)
        invariant = ["date", "purchase_type", "payment_method", "manager", "city"]
        conflicts = any(group[column].nunique(dropna=False) > 1 for column in invariant)
        if conflicts:
            label = "conflicting_duplicate_record"
            detail = "Repeated order_id has conflicting contextual attributes."
        elif product_count > 1:
            label = "repeated_order_id_possible_line_items"
            detail = "Repeated order_id has multiple products; validity depends on source grain."
        else:
            label = "uncertain_repeated_record"
            detail = "Repeated order_id is not exact but line-item validity cannot be proven."
        for index in group.index:
            rows.append(
                {
                    "source_row_number": int(index) + 2,
                    "order_id": order_id,
                    "classification": label,
                    "details": detail,
                }
            )
    return pd.DataFrame(rows, columns=["source_row_number", "order_id", "classification", "details"])


def validate_data_contract(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    """Validate schema and domain rules without silently discarding records."""
    data = frame.copy()
    data.columns = normalize_column_names(data.columns)
    require_columns(data)
    dates = pd.to_datetime(data["date"], format=DATE_FORMAT, errors="coerce")
    price = pd.to_numeric(data["price"], errors="coerce")
    quantity = pd.to_numeric(data["quantity"], errors="coerce")
    issues: list[list[str]] = [[] for _ in range(len(data))]

    def add(mask: pd.Series, reason: str) -> None:
        for position in mask[mask].index:
            issues[data.index.get_loc(position)].append(reason)

    add(data["order_id"].isna(), "missing_order_id")
    add(dates.isna(), "invalid_date")
    add(price.isna(), "invalid_price")
    add(price.lt(0), "negative_price")
    add(price.eq(0), "zero_price")
    add(quantity.isna(), "invalid_quantity")
    add(quantity.lt(0), "negative_quantity")
    add(quantity.eq(0), "zero_quantity")
    for column in TEXT_COLUMNS:
        add(clean_text(data[column]).isna(), f"blank_{column}")
    issue_text = pd.Series(["|".join(row) for row in issues], index=data.index, dtype="string")
    invalid = data.loc[issue_text.ne("")].copy()
    invalid.insert(0, "source_row_number", invalid.index + 2)
    invalid["validation_issues"] = issue_text[issue_text.ne("")].values
    duplicates = classify_duplicates(data)
    summary: dict[str, Any] = {
        "row_count": len(data),
        "column_count": len(data.columns),
        "required_columns": list(EXPECTED_COLUMNS),
        "missing_columns": [],
        "unexpected_columns": sorted(set(data.columns) - set(EXPECTED_COLUMNS)),
        "null_counts": {column: int(value) for column, value in data.isna().sum().items()},
        "invalid_record_count": len(invalid),
        "exact_duplicate_extra_copies": int(data.duplicated().sum()),
        "duplicate_order_id_extra_rows": int(data.duplicated("order_id").sum()),
        "date_min": dates.min().date().isoformat() if dates.notna().any() else None,
        "date_max": dates.max().date().isoformat() if dates.notna().any() else None,
        "active_dates": int(dates.nunique()),
    }
    return invalid, duplicates, summary
