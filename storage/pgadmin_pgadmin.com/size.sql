-- Postgres Version
SELECT VERSION();

-- Explain the full query.
EXPLAIN
SELECT *
FROM orders
WHERE order_id = 123456
ORDER BY order_id
LIMIT 1;

-- Start with something less complex.
EXPLAIN
SELECT *
FROM orders;

-- Sample data
SELECT * FROM orders LIMIT 20;

-- Number of rows in the orders table
SELECT COUNT(*) FROM orders;
-- 20,000,000

-- Average Row Size
SELECT (SUM(pg_column_size(o.*)) / count(*)) AS avg_row_size
FROM orders o;
-- 370

