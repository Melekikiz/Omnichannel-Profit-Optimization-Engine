CREATE TABLE orders(
    order_id INT PRIMARY KEY,
    order_date DATE,
    country VARCHAR(10),
    channel VARCHAR(10),
    segment VARCHAR(10),
    quantity INT,
    unit_price DECIMAL(12,2) -- local currency
);

CREATE TABLE behavior(
    order_id INT PRIMARY KEY,
    is_returned BOOLEAN,
    days_to_payment INT
);

CREATE TABLE cost_structure(
    id SERIAL PRIMARY KEY,
    country VARCHAR(10),
    channel VARCHAR(10),
    base_shipping DECIMAL(10,2),
    base_marketing DECIMAL(10,2),
    labor_ratio DECIMAL(5,4)
);

CREATE TABLE fx_rates(
    date DATE PRIMARY KEY,
    usd_try DECIMAL(12,4),
    usd_eur DECIMAL(12,4)
);

-----