# BI Data Model

This is a small **dashboard-ready analytical model**, not a production data warehouse.

## Tables and relationships

- `fact_sales`: one aggregated product sales record; primary key `record_id`.
- `dim_date`: one calendar date; join `fact_sales.date` → `dim_date.date` (many-to-one).
- `dim_product`: one product; join on `product` (many-to-one).
- `dim_location`: one city; join on `city` (many-to-one).
- `dim_channel`: observed purchase-type/payment-method combinations; join on both fields (many-to-one).

Revenue is `price × quantity`. Currency and the unit of quantity are unknown. Do not build order-count or AOV measures from this model unless a richer source verifies customer-order grain.
