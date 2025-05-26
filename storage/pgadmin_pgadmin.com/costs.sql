-- Get the amount of disk space used by the relation (table).
SELECT pg_relation_size('orders');
-- 7,778,410,496

-- Need number of blocks. Blocks are the fundamental units of storage within Postgres.
-- You can set this to a different value.
SHOW block_size;
-- 1 Block = 8k = 8 * 1024 = 8192.0

-- Number of blocks in table
SELECT pg_relation_size('orders') / 8192.0;
-- 949,513 <- NUMBER OF BLOCKS IN TABLE

-- The planner is part of Postgres' tool to analyze and develop execution plans for queries.

--Get page cost:  the planner's estimate of the cost of a disk page fetch that is part of a series of sequential fetches.
-- You can set this to a different value.
SHOW seq_page_cost;
-- 1

-- Number of records in a table.
SELECT COUNT(*) FROM orders;
-- 20000000

-- CPU Tuple Cost (Tuple == Row): the planner's estimate of the cost of processing each row during a query.
-- You can set this to a different value.
SHOW cpu_tuple_cost;
-- 0.01

-- CPU Operator Cost:  the planner's estimate of the cost of processing each operator or function executed during a query.
-- You can set this to a different value.
SHOW cpu_operator_cost;
-- 0.0025

-- Putting it all together:
SELECT (pg_relation_size('orders') / 8192.0 * 1.0)
    + ((SELECT COUNT(*) FROM orders) * 0.01)
	+ ((SELECT COUNT(*) FROM orders) * 0.0025) AS estimated_cost;
-- 1,199,513

-- Get actual data with EXPLAIN ANALYZE.
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE order_id = 123456
ORDER BY order_id
LIMIT 1;

