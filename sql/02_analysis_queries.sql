USE restaurant_sales_insight;

-- 1. Total revenue
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM restaurant_sales;

-- 2. Total orders
SELECT COUNT(DISTINCT order_id) AS total_orders
FROM restaurant_sales;

-- 3. Top selling menu by revenue
SELECT
    product,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM restaurant_sales
GROUP BY product
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. Sales by category
SELECT
    product_category,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM restaurant_sales
GROUP BY product_category
ORDER BY total_revenue DESC;

-- 5. Sales by day
SELECT
    order_date,
    DAYNAME(order_date) AS day_name,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(*) AS row_count
FROM restaurant_sales
GROUP BY order_date
ORDER BY order_date;

-- 6. Sales by month
SELECT
    YEAR(order_date) AS sales_year,
    MONTH(order_date) AS sales_month_num,
    DATE_FORMAT(order_date, '%b %Y') AS sales_month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(*) AS row_count
FROM restaurant_sales
GROUP BY YEAR(order_date), MONTH(order_date), DATE_FORMAT(order_date, '%b %Y')
ORDER BY sales_year, sales_month_num;

-- 7. Sales by hour
-- Source limitation:
-- The Kaggle dataset does not include transaction timestamps or hour fields.
-- Replace `order_hour` with a real hour column when POS timestamp data is available.
/*
SELECT
    HOUR(order_timestamp) AS order_hour,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM restaurant_sales
GROUP BY HOUR(order_timestamp)
ORDER BY order_hour;
*/

-- 8. Average order value
SELECT ROUND(SUM(revenue) / COUNT(DISTINCT order_id), 2) AS average_order_value
FROM restaurant_sales;

-- Optional extra cut: revenue by purchase type
SELECT
    purchase_type,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM restaurant_sales
GROUP BY purchase_type
ORDER BY total_revenue DESC;

-- Optional extra cut: revenue by city
SELECT
    city,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM restaurant_sales
GROUP BY city
ORDER BY total_revenue DESC;
