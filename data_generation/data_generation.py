import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime

# --- DATABASE CONNECTION ---
engine = create_engine('postgresql://postgres:""@localhost:5432/profit_optimization')
print("Connection to the database established successfully!")

# --- PARAMETERS ---
n_rows = 500000
start_date = datetime(2024, 1, 1)
current_date = datetime.now()
total_days = (current_date - start_date).days

np.random.seed(42)

# --- FX RATES ---
def generate_fx(days):
    dates = pd.date_range(start_date, periods=days)
    usd_try = 30 + np.cumsum(np.random.normal(0.015, 0.12, days))
    usd_eur = 0.9 + np.cumsum(np.random.normal(0.0002, 0.008, days))
    return pd.DataFrame({'date': dates.date, 'usd_try': usd_try, 'usd_eur': usd_eur})

fx_df = generate_fx(total_days)
fx_df.to_sql('fx_rates', engine, if_exists='replace', index=False)

# --- COST STRUCTURE ---
cost_data = [
    {'country': 'TR', 'channel': 'D2C', 'base_shipping': 2.5, 'base_marketing': 5.0, 'labor_ratio': 0.08},
    {'country': 'TR', 'channel': 'B2B', 'base_shipping': 8.0, 'base_marketing': 1.0, 'labor_ratio': 0.05},
    {'country': 'DE', 'channel': 'D2C', 'base_shipping': 7.0, 'base_marketing': 12.0, 'labor_ratio': 0.25},
    {'country': 'DE', 'channel': 'B2B', 'base_shipping': 25.0, 'base_marketing': 3.0, 'labor_ratio': 0.15},
    {'country': 'UAE', 'channel': 'D2C', 'base_shipping': 12.0, 'base_marketing': 20.0, 'labor_ratio': 0.12},
    {'country': 'UAE', 'channel': 'B2B', 'base_shipping': 40.0, 'base_marketing': 5.0, 'labor_ratio': 0.08},
]
pd.DataFrame(cost_data).to_sql('cost_structure', engine, if_exists='replace', index=False)

# --- ORDERS GENERATION ---
df_orders = pd.DataFrame({
    'order_id': np.arange(1, n_rows + 1),
    'order_date': np.random.choice(fx_df['date'], n_rows),
    'country': np.random.choice(['TR', 'DE', 'UAE'], n_rows, p=[0.45, 0.35, 0.20]),
    'channel': np.random.choice(['B2B', 'D2C'], n_rows, p=[0.35, 0.65])
})

# --- SEGMENTATION ---
df_orders['segment'] = 'Entry'
for country, probs in zip(['TR', 'DE', 'UAE'], [[0.7, 0.2, 0.1], [0.3, 0.5, 0.2], [0.1, 0.3, 0.6]]):
    mask = df_orders['country'] == country
    df_orders.loc[mask, 'segment'] = np.random.choice(['Entry', 'Mid', 'Premium'], mask.sum(), p=probs)

# --- BASE USD PRICE ---
df_orders['base_price_usd'] = 0.0
masks = {s: df_orders['segment'] == s for s in ['Entry', 'Mid', 'Premium']}
df_orders.loc[masks['Entry'], 'base_price_usd'] = np.random.uniform(20, 80, masks['Entry'].sum())
df_orders.loc[masks['Mid'], 'base_price_usd'] = np.random.uniform(80, 250, masks['Mid'].sum())
df_orders.loc[masks['Premium'], 'base_price_usd'] = np.random.uniform(250, 1500, masks['Premium'].sum())

# --- MERGE FX ---
df_orders = df_orders.merge(fx_df, left_on='order_date', right_on='date', how='left')

# --- UNIT PRICE LOCAL CURRENCY ---
df_orders['unit_price'] = df_orders['base_price_usd']
df_orders.loc[df_orders['country'] == 'TR', 'unit_price'] *= df_orders['usd_try']
df_orders.loc[df_orders['country'] == 'DE', 'unit_price'] *= df_orders['usd_eur']

# --- QUANTITY ---
df_orders['quantity'] = 1
b2b_mask = df_orders['channel'] == 'B2B'
df_orders.loc[b2b_mask, 'quantity'] = np.random.randint(10, 100, b2b_mask.sum())
df_orders.loc[~b2b_mask & masks['Entry'], 'quantity'] = np.random.randint(1, 5, (~b2b_mask & masks['Entry']).sum())
df_orders.loc[~b2b_mask & masks['Mid'], 'quantity'] = np.random.randint(1, 4, (~b2b_mask & masks['Mid']).sum())
df_orders.loc[~b2b_mask & masks['Premium'], 'quantity'] = np.random.randint(1, 3, (~b2b_mask & masks['Premium']).sum())

# --- BEHAVIOR TABLE ---
behavior_df = pd.DataFrame({'order_id': df_orders['order_id']})
behavior_df['is_returned'] = False
for s, prob in zip(['Entry', 'Mid', 'Premium'], [0.28, 0.14, 0.04]):
    behavior_df.loc[masks[s], 'is_returned'] = np.random.random(masks[s].sum()) < prob

behavior_df['days_to_payment'] = np.random.randint(1, 10, n_rows)
behavior_df.loc[b2b_mask, 'days_to_payment'] = np.random.randint(30, 120, b2b_mask.sum())

# --- EXPORT TO DATABASE ---
orders_final = df_orders[['order_id', 'order_date', 'country', 'channel', 'segment', 'quantity', 'unit_price']]
orders_final.to_sql('orders', engine, if_exists='replace', index=False, chunksize=15000, method='multi')

behavior_df.to_sql('behavior', engine, if_exists='replace', index=False, chunksize=15000, method='multi')

print(f"{start_date.date()} - {current_date.date()} | {n_rows} rows of orders and behavior data generated successfully!")