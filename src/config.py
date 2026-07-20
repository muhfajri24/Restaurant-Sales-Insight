"""Central project configuration and portable repository paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ProjectPaths:
    """All repository paths used by the production pipeline."""

    base: Path = BASE_DIR

    @property
    def data(self) -> Path:
        return self.base / "data" / "restaurant_sales_raw.csv"

    @property
    def mapping(self) -> Path:
        return self.base / "config" / "product_category_mapping.csv"

    @property
    def output(self) -> Path:
        return self.base / "output"

    @property
    def reports(self) -> Path:
        return self.base / "reports"

    @property
    def figures(self) -> Path:
        return self.output / "figures"


PATHS = ProjectPaths()
DATA_PATH = PATHS.data
MAPPING_PATH = PATHS.mapping
OUTPUT_DIR = PATHS.output
REPORTS_DIR = PATHS.reports
FIGURES_DIR = PATHS.figures

EXPECTED_COLUMNS = (
    "order_id",
    "date",
    "product",
    "price",
    "quantity",
    "purchase_type",
    "payment_method",
    "manager",
    "city",
)
TEXT_COLUMNS = ("product", "purchase_type", "payment_method", "manager", "city")
DAY_ORDER = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
GRAIN_LABEL = "one aggregated product sales record with a unique source order_id"
ORDER_KPIS_SUPPORTED = False
DATE_FORMAT = "%d-%m-%Y"
FIGURE_DPI = 160
RANDOM_SEED = 42

KPI_DEFINITIONS = {
    "total_revenue": "sum(price × quantity)",
    "total_sales_records": "count distinct record_id",
    "total_quantity_sold": "sum(quantity)",
    "average_selling_price": "total revenue / total quantity",
    "active_sales_days": "count distinct date",
    "average_daily_revenue": "total revenue / active sales days",
    "median_daily_revenue": "median of active-day revenue",
}

REQUIRED_OUTPUT_DIRECTORIES = (
    "analysis",
    "insights",
    "kpis",
    "bi",
    "figures",
)
