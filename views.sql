-- MASTER PROFITABILITY VIEW


DROP VIEW IF EXISTS v_master_profitability;

CREATE OR REPLACE VIEW v_master_profitability AS
WITH base_data AS (
    SELECT
        o.order_id,
        o.order_date,
        o.country,
        o.channel,
        o.segment,
        o.quantity,
        o.unit_price,          -- local currency
        b.is_returned,
        
        -- FX ile USD revenue
        CASE 
            WHEN o.country='TR' THEN (o.unit_price * o.quantity) / fr.usd_try
            WHEN o.country='DE' THEN (o.unit_price * o.quantity) / fr.usd_eur
            ELSE (o.unit_price * o.quantity) / 3.67
        END AS gross_revenue_usd,
        
        -- Base USD price (unit)
        CASE
            WHEN o.country='TR' THEN o.unit_price / fr.usd_try
            WHEN o.country='DE' THEN o.unit_price / fr.usd_eur
            ELSE o.unit_price / 3.67
        END AS base_price_usd,
        
        -- Costs from reference table
        cs.base_shipping,
        cs.base_marketing,
        cs.labor_ratio
    FROM orders o
    LEFT JOIN behavior b ON o.order_id = b.order_id
    LEFT JOIN fx_rates fr ON o.order_date = fr.date
    LEFT JOIN cost_structure cs ON o.country = cs.country AND o.channel = cs.channel
)

SELECT
    *,
    
    -- Net revenue after returns
    CASE WHEN is_returned THEN 0 ELSE gross_revenue_usd END AS net_revenue_usd,
    
    -- Costs
    (base_shipping * quantity) AS total_shipping_cost,
    (base_marketing * quantity) AS total_marketing_cost,
    (base_price_usd * quantity) AS cogs,
    (gross_revenue_usd * labor_ratio) AS labor_cost,
    
    -- FINAL NET PROFIT
    (CASE WHEN is_returned THEN 0 ELSE gross_revenue_usd END)
        - (base_price_usd * quantity)
        - (base_shipping * quantity)
        - (base_marketing * quantity)
        - (gross_revenue_usd * labor_ratio)
    AS net_profit_usd

FROM base_data;