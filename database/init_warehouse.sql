-- Dimension: Product
CREATE TABLE dim_product (
    product_id INTEGER PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL
);

-- Dimension: Customer
CREATE TABLE dim_customer (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Dimension: Time
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    order_datetime TIMESTAMP NOT NULL,
    order_date DATE NOT NULL,
    order_hour INTEGER NOT NULL,
    order_weekday INTEGER NOT NULL
);

-- Fact: Sales
CREATE TABLE fact_sales (
    sales_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
    customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    time_id INTEGER NOT NULL REFERENCES dim_time(time_id),
    quantity INTEGER NOT NULL,
    revenue_usd NUMERIC(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    original_amount NUMERIC(12,2) NOT NULL
);
