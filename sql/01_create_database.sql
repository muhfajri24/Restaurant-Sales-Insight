CREATE DATABASE IF NOT EXISTS restaurant_sales_insight;
USE restaurant_sales_insight;

DROP TABLE IF EXISTS restaurant_sales;

CREATE TABLE restaurant_sales (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    year SMALLINT NOT NULL,
    month_num TINYINT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    week_num TINYINT NOT NULL,
    day_num TINYINT NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    product VARCHAR(100) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    revenue DECIMAL(12, 2) NOT NULL,
    purchase_type VARCHAR(30) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    manager VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL
);

/*
Load the cleaned CSV exported by the notebook or ETL step.
Update the path to match your local machine before running.
*/
LOAD DATA LOCAL INFILE 'output/restaurant_sales_cleaned.csv'
INTO TABLE restaurant_sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    order_id,
    @order_date,
    year,
    month_num,
    month_name,
    week_num,
    day_num,
    day_name,
    @is_weekend,
    product,
    product_category,
    price,
    quantity,
    revenue,
    purchase_type,
    payment_method,
    manager,
    city
)
SET
    order_date = STR_TO_DATE(@order_date, '%Y-%m-%d'),
    is_weekend = CASE
        WHEN LOWER(@is_weekend) IN ('true', '1') THEN 1
        ELSE 0
    END;
