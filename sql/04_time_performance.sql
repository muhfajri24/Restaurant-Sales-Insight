USE restaurant_sales_insight;
WITH monthly AS (
 SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month,
        SUM(revenue) AS revenue, SUM(quantity) AS quantity,
        COUNT(DISTINCT record_id) AS sales_records,
        MIN(sale_date) AS period_start, MAX(sale_date) AS period_end
 FROM fact_sales GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
)
SELECT *, LAG(revenue) OVER (ORDER BY month) AS previous_revenue,
       (revenue - LAG(revenue) OVER (ORDER BY month)) /
       NULLIF(LAG(revenue) OVER (ORDER BY month), 0) AS growth_rate,
       CASE WHEN DAY(period_start) <> 1 OR DAY(period_end) <> DAY(LAST_DAY(period_end)) THEN 1 ELSE 0 END AS is_partial_period
FROM monthly ORDER BY month;

SELECT WEEKDAY(sale_date) + 1 AS day_of_week_num, DAYNAME(sale_date) AS day_name,
       SUM(revenue) AS revenue, SUM(quantity) AS quantity,
       COUNT(DISTINCT record_id) AS sales_records
FROM fact_sales GROUP BY WEEKDAY(sale_date) + 1, DAYNAME(sale_date)
ORDER BY day_of_week_num;
