USE restaurant_sales_insight;
WITH city_metrics AS (
 SELECT city, SUM(quantity) AS quantity, SUM(revenue) AS revenue,
        SUM(revenue) / NULLIF(SUM(quantity), 0) AS weighted_selling_price
 FROM fact_sales GROUP BY city
), baseline AS (
 SELECT SUM(revenue) / NULLIF(SUM(quantity), 0) AS overall_weighted_price FROM fact_sales
), ranked AS (
 SELECT c.*, PERCENT_RANK() OVER (ORDER BY quantity) AS volume_percentile,
        b.overall_weighted_price
 FROM city_metrics c CROSS JOIN baseline b
)
SELECT city, quantity, revenue, weighted_selling_price, overall_weighted_price,
       'Validate product mix, discounts, costs, inventory, staffing, and capacity' AS validation_action
FROM ranked WHERE volume_percentile >= 0.5 AND weighted_selling_price < overall_weighted_price
ORDER BY quantity DESC;
