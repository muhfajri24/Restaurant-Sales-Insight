USE restaurant_sales_insight;
WITH product_sales AS (
 SELECT product, SUM(revenue) AS revenue, SUM(quantity) AS quantity,
        COUNT(DISTINCT record_id) AS sales_records
 FROM fact_sales GROUP BY product
), ranked AS (
 SELECT *, revenue / NULLIF(SUM(revenue) OVER (), 0) AS revenue_share,
        RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
 FROM product_sales
)
SELECT *, SUM(revenue_share) OVER (ORDER BY revenue DESC, product ROWS UNBOUNDED PRECEDING) AS cumulative_revenue_share
FROM ranked ORDER BY revenue DESC, product;
