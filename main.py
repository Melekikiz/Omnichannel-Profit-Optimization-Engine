from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os

app = FastAPI()

# Data Loading - Updated to read from CSV instead of PostgreSQL
FILE_PATH = 'master_data.csv'

def load_data():
    if os.path.exists(FILE_PATH):
        # Reading the LFS-tracked CSV file
        df = pd.read_csv(FILE_PATH)
        return df
    else:
        print(f"ERROR: {FILE_PATH} not found!")
        return pd.DataFrame()

df_master = load_data()

# Pydantic model for input data
class SimulationInput(BaseModel):
    mkt_change: float
    return_improve: float
    shipping_cost_shock: float

# Simulation logic
def run_logic(df, mkt_change, return_improve, shipping_cost_shock):
    sim_df = df.copy()
    
    # Marketing change
    sim_df['total_marketing_cost'] *= (1 + mkt_change)

    # Return improvement logic
    # Ensuring is_returned is treated as boolean
    sim_df['is_returned'] = sim_df['is_returned'].astype(str).str.lower().isin(['true', '1', '1.0'])
    
    returned_idx = sim_df[sim_df['is_returned'] == True].index
    fix_count = int(len(returned_idx) * return_improve)
    
    if fix_count > 0:
        fix_idx = np.random.choice(returned_idx, fix_count, replace=False)
        sim_df.loc[fix_idx, 'is_returned'] = False

    sim_df['net_revenue_usd'] = np.where(sim_df['is_returned'], 0, sim_df['gross_revenue_usd'])
    
    # Shipping cost shock
    sim_df['total_shipping_cost'] *= (1 + shipping_cost_shock)

    # Net Profit calculation
    sim_df['new_net_profit'] = (sim_df['net_revenue_usd'] - 
                                sim_df['cogs'] - 
                                sim_df['total_shipping_cost'] - 
                                sim_df['total_marketing_cost'] - 
                                sim_df['labor_cost'])
    return sim_df

# API Endpoint
@app.post("/simulate")
def simulate(data: SimulationInput):
    if df_master.empty:
        return {"status": "error", "message": "Dataset not loaded."}

    # Baseline calculation
    baseline_df = run_logic(df_master, 0, 0, 0)
    baseline_profit = float(baseline_df['new_net_profit'].sum())

    # Simulated calculation
    result_df = run_logic(
        df_master,
        data.mkt_change,
        data.return_improve,
        data.shipping_cost_shock
    )

    waterfall_results = {
        "Gross": float(result_df['gross_revenue_usd'].sum()),
        "COGS": float(result_df['cogs'].sum()),
        "Returns_Loss": float(result_df['gross_revenue_usd'].sum() - result_df['net_revenue_usd'].sum()),
        "Shipping": float(result_df['total_shipping_cost'].sum()),
        "Marketing": float(result_df['total_marketing_cost'].sum()),
        "Labor": float(result_df['labor_cost'].sum()),
        "Net_Profit": float(result_df['new_net_profit'].sum())
    }

    return {
        "status": "success",
        "baseline_profit": round(baseline_profit, 2),
        "simulated_profit": round(waterfall_results["Net_Profit"], 2),
        "waterfall": waterfall_results, 
        "currency": "USD"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
