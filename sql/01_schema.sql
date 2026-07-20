-- MySQL 8.0 analytical schema. Tested structurally by the repository test suite;
-- execution still requires a local MySQL 8.0 instance.
CREATE DATABASE IF NOT EXISTS restaurant_sales_insight;
USE restaurant_sales_insight;

CREATE TABLE IF NOT EXISTS fact_sales (
    record_id VARCHAR(24) PRIMARY KEY,
    order_id BIGINT NOT NULL,
    sale_date DATE NOT NULL,
    product VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    purchase_type VARCHAR(50) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    manager VARCHAR(100) NOT NULL,
    price DECIMAL(14,4) NOT NULL,
    quantity DECIMAL(14,4) NOT NULL,
    revenue DECIMAL(16,2) NOT NULL,
    CHECK (price > 0), CHECK (quantity > 0), CHECK (revenue >= 0)
);

-- Import output/bi/fact_sales.csv with the MySQL client or LOAD DATA LOCAL
-- INFILE after replacing only the path on your own system. Do not count
-- order_id as customer orders: the verified grain is an aggregated product record.
