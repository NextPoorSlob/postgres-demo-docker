-- noinspection SqlNoDataSourceInspectionForFile

BEGIN;

CREATE TABLE customers (
    customer_id         SERIAL NOT NULL,
    first_name          VARCHAR(50) NOT NULL,
    last_name           VARCHAR(50) NOT NULL,
    organization_name   VARCHAR(100) NOT NULL,
    addresses           TEXT NOT NULL
);

CREATE TABLE products (
    product_id              SERIAL NOT NULL,
    name                    VARCHAR(255) NOT NULL,
    description             TEXT NOT NULL,
    cost                    DECIMAL(12, 2) NOT NULL,
    category                VARCHAR(50) NOT NULL,
    additional_information  TEXT NOT NULL
);

CREATE TABLE orders (
    order_id        SERIAL NOT NULL,
    customer_id     BIGINT NOT NULL,
    product_id      BIGINT NOT NULL,
    quantity        INTEGER NOT NULL,
    "authorization"   TEXT NOT NULL,
    notes           TEXT NOT NULL
);

\COPY customers(first_name, last_name, organization_name, addresses) FROM '/docker-entrypoint-initdb.d/customers.csv' WITH DELIMITER ',' CSV HEADER;

\COPY products(name, description, cost, category, additional_information) FROM '/docker-entrypoint-initdb.d/products.csv' WITH DELIMITER ',' CSV HEADER;

\COPY orders(customer_id, product_id, quantity, "authorization", notes) FROM '/docker-entrypoint-initdb.d/orders.csv' WITH DELIMITER ',' CSV HEADER;

COMMIT;
