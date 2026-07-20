USE restaurant_sales_insight;
SELECT COUNT(*) AS row_count,
       COUNT(DISTINCT record_id) AS unique_record_ids,
       COUNT(DISTINCT order_id) AS unique_source_order_ids,
       SUM(price <= 0) AS nonpositive_price_rows,
       SUM(quantity <= 0) AS nonpositive_quantity_rows,
       SUM(ABS(revenue - ROUND(price * quantity, 2)) > 0.01) AS revenue_mismatch_rows
FROM fact_sales;

SELECT order_id, COUNT(*) AS records
FROM fact_sales GROUP BY order_id HAVING COUNT(*) > 1;
