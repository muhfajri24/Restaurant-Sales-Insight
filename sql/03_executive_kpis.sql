USE restaurant_sales_insight;
WITH daily AS (
  SELECT sale_date, SUM(revenue) AS daily_revenue FROM fact_sales GROUP BY sale_date
), totals AS (
  SELECT SUM(revenue) AS total_revenue, SUM(quantity) AS total_quantity,
         COUNT(DISTINCT record_id) AS total_sales_records,
         COUNT(DISTINCT sale_date) AS active_sales_days
  FROM fact_sales
)
SELECT total_revenue, total_sales_records, total_quantity,
       total_revenue / NULLIF(total_quantity, 0) AS weighted_selling_price,
       active_sales_days, total_revenue / NULLIF(active_sales_days, 0) AS average_active_day_revenue,
       NULL AS total_orders, NULL AS average_order_value
FROM totals;
