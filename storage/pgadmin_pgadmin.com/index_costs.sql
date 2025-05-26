-- The Order table size without indexes.
SELECT pg_size_pretty(pg_total_relation_size('orders'));
-- 7420 MB

-- Size of the non-existent indexes.
SELECT pg_size_pretty(pg_indexes_size('orders'));
-- 0 bytes

-- Total Size: 7420 MB + 0 Bytes = 7420 MB.

-- Add a primary key on order_id.
ALTER TABLE orders
	ADD PRIMARY KEY (order_id);
-- Query returned successfully in 13 secs 132 msec.

-- Did it work?
SELECT *
FROM pg_indexes
WHERE tablename = 'orders';
-- Yes!
-- "schemaname"	"tablename"	"indexname"	"tablespace"	"indexdef"
-- "public"	    "orders"	"orders_pkey"		        "CREATE UNIQUE INDEX orders_pkey ON public.orders USING btree (order_id)"


-- Now find the size of the indexes
SELECT pg_size_pretty(pg_indexes_size('orders'));
-- 428 MB

-- We can also see the cost of the index in the total relation size.
-- The Order table size with indexes.
SELECT pg_size_pretty(pg_total_relation_size('orders'));
-- 7849 MB, an increase of 7849 - 7420 = 429 MB, which matches the additional index data.

-- Now we have and index!
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE order_id = 123456
ORDER BY order_id
LIMIT 1;
-- Execution Time: 1.862 ms