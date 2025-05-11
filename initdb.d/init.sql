-- noinspection SqlNoDataSourceInspectionForFile

BEGIN;

CREATE TABLE customers (
    customer_id         SERIAL,
    first_name          VARCHAR(50),
    last_name           VARCHAR(50),
    organization_name   VARCHAR(100),
    addresses           TEXT
);

CREATE TABLE products (
    product_id              SERIAL,
    name                    VARCHAR(255),
    description             TEXT,
    cost                    DECIMAL(12, 2),
    category                VARCHAR(50),
    additional_information  TEXT
);

\COPY customers(first_name, last_name, organization_name, addresses) FROM '/docker-entrypoint-initdb.d/customers.csv' WITH DELIMITER ',' CSV HEADER;

\COPY products(name, description, cost, category, additional_information) FROM '/docker-entrypoint-initdb.d/products.csv' WITH DELIMITER ',' CSV HEADER;

COMMIT;
