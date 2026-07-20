USE restaurant_sales_insight;
SELECT city, SUM(revenue) AS revenue, SUM(quantity) AS quantity,
       COUNT(DISTINCT record_id) AS sales_records,
       SUM(revenue) / NULLIF(SUM(quantity), 0) AS weighted_selling_price,
       SUM(revenue) / NULLIF(COUNT(DISTINCT sale_date), 0) AS average_active_day_revenue
FROM fact_sales GROUP BY city ORDER BY revenue DESC;

SELECT purchase_type, payment_method, SUM(revenue) AS revenue,
       SUM(quantity) AS quantity, COUNT(DISTINCT record_id) AS sales_records,
       SUM(revenue) / NULLIF(SUM(quantity), 0) AS weighted_selling_price
FROM fact_sales GROUP BY purchase_type, payment_method ORDER BY revenue DESC;

SELECT manager, SUM(revenue) AS recorded_revenue, SUM(quantity) AS quantity,
       COUNT(DISTINCT record_id) AS sales_records, COUNT(DISTINCT city) AS cities,
       MIN(sale_date) AS first_date, MAX(sale_date) AS last_date
FROM fact_sales GROUP BY manager ORDER BY recorded_revenue DESC;
