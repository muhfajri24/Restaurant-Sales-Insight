"""Deterministic cleaning with audit, removal, and conflict outputs."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.config import DATE_FORMAT, MAPPING_PATH, TEXT_COLUMNS
from src.exceptions import ProductMappingError, SchemaValidationError
from src.validation import classify_duplicates, clean_text, normalize_column_names, require_columns


def _load_mapping(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise ProductMappingError(f"File mapping produk tidak ditemukan: {path}")
    mapping = pd.read_csv(path, dtype="string")
    required = {"product_standardized", "product_category"}
    if not required.issubset(mapping.columns):
        raise ProductMappingError(
            f"Mapping produk harus memiliki kolom {sorted(required)}; tersedia {sorted(mapping.columns)}"
        )
    mapping["product_standardized"] = clean_text(mapping["product_standardized"])
    if mapping["product_standardized"].duplicated().any():
        raise ProductMappingError("Mapping produk memuat product_standardized duplikat.")
    return mapping


def clean_sales_data(
    raw: pd.DataFrame,
    mapping_path: Path = MAPPING_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Clean source records and return clean, audit, removed, and flagged frames."""
    data = raw.copy()
    data.columns = normalize_column_names(data.columns)
    try:
        require_columns(data)
    except SchemaValidationError:
        raise
    data.insert(0, "source_row_number", np.arange(2, len(data) + 2))
    audit: list[dict[str, Any]] = []
    for column in TEXT_COLUMNS:
        before = data[column].copy()
        data[column] = clean_text(data[column])
        changed = before.astype("string").fillna("") != data[column].fillna("")
        for index in data.index[changed]:
            audit.append(
                {
                    "source_row_number": int(data.at[index, "source_row_number"]),
                    "action": "repaired",
                    "field": column,
                    "reason": "standardized_whitespace",
                    "old_value": before.at[index],
                    "new_value": data.at[index, column],
                }
            )
    data["date"] = pd.to_datetime(data["date"], format=DATE_FORMAT, errors="coerce")
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce")
    invalid = (
        data["order_id"].isna()
        | data["date"].isna()
        | data[list(TEXT_COLUMNS)].isna().any(axis=1)
        | data["price"].isna()
        | data["quantity"].isna()
        | data["price"].le(0)
        | data["quantity"].le(0)
    )
    exact_duplicate = data.drop(columns="source_row_number").duplicated(keep="first")
    removed = data.loc[invalid | exact_duplicate].copy()
    removed["removal_reason"] = np.where(
        exact_duplicate.loc[removed.index], "verified_exact_duplicate", "invalid_required_value"
    )
    for _, row in removed.iterrows():
        audit.append(
            {
                "source_row_number": int(row["source_row_number"]),
                "action": "removed",
                "field": "record",
                "reason": row["removal_reason"],
                "old_value": "",
                "new_value": "",
            }
        )
    duplicate_analysis = classify_duplicates(data.drop(columns="source_row_number"))
    conflicts = set(
        duplicate_analysis.loc[
            duplicate_analysis["classification"].isin(["conflicting_duplicate_record", "uncertain_repeated_record"]),
            "source_row_number",
        ]
    )
    flagged = data[data["source_row_number"].isin(conflicts)].copy()
    flagged["flag_reason"] = "conflicting_or_uncertain_repeated_order_id"
    clean = data.loc[~(invalid | exact_duplicate)].copy()
    clean["product_original"] = clean["product"]
    clean["product"] = clean["product"].str.title().replace({"Sides & Other": "Sides & Other"})
    clean = clean.merge(
        _load_mapping(mapping_path),
        left_on="product",
        right_on="product_standardized",
        how="left",
        validate="many_to_one",
    ).drop(columns="product_standardized")
    clean["product_category"] = clean["product_category"].fillna("Other")
    clean["revenue"] = (clean["price"] * clean["quantity"]).round(2)
    clean["record_id"] = clean.apply(
        lambda row: (
            "rec_"
            + hashlib.sha256(
                f"{int(row.source_row_number)}|{row.order_id}|{row.date}|{row.product}|{row.price}|{row.quantity}".encode()
            ).hexdigest()[:16]
        ),
        axis=1,
    )
    clean["year"] = clean["date"].dt.year
    clean["month_num"] = clean["date"].dt.month
    clean["month_name"] = clean["date"].dt.strftime("%b")
    clean["month"] = clean["date"].dt.to_period("M").astype(str)
    clean["week_start"] = clean["date"] - pd.to_timedelta(clean["date"].dt.weekday, unit="D")
    clean["week_num"] = clean["date"].dt.isocalendar().week.astype(int)
    clean["day_num"] = clean["date"].dt.day
    clean["day_name"] = clean["date"].dt.day_name()
    clean["day_of_week_num"] = clean["date"].dt.weekday + 1
    clean["is_weekend"] = clean["day_of_week_num"].ge(6)
    clean["period_type"] = "complete_day"
    clean = clean.sort_values(["date", "record_id"]).reset_index(drop=True)
    audit_frame = pd.DataFrame(
        audit, columns=["source_row_number", "action", "field", "reason", "old_value", "new_value"]
    )
    return clean, audit_frame, removed, flagged
