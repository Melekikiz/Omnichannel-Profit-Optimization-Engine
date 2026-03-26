from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

app= FastAPI()

engine=create_engine('postgresql://postgres:""@localhost:5432/profit_optimization')
df_master=pd.read_sql('SELECT * FROM v_master_profitability', engine)

#Pydantic model for input data
class SimulationInput(BaseModel):
    mkt_change:float
    return_improve:float
    shipping_cost_shock:float

#Simulation 
def run_logic(df, mkt_change, return_improve, shipping_cost_shock):
    sim_df=df.copy()
    sim_df['total_marketing_cost'] *= (1 + mkt_change)

    #Return improvement logic
    returned_idx = sim_df[sim_df['is_returned']].index
    fix_count = int(len(returned_idx) * return_improve)
    if fix_count > 0:
        fix_idx = np.random.choice(returned_idx, fix_count, replace=False)
        sim_df.loc[fix_idx, 'is_returned'] = False

    sim_df['net_revenue_usd'] = np.where(sim_df['is_returned'], 0, sim_df['gross_revenue_usd'])
    sim_df['total_shipping_cost'] *= (1 + shipping_cost_shock)

    sim_df['new_net_profit']=(sim_df['net_revenue_usd'] - sim_df['cogs'] -
                              sim_df['total_shipping_cost'] - sim_df['total_marketing_cost']-
                              sim_df['labor_cost'])
    return sim_df

#API Endpoint
@app.post("/simulate")
def simulate(data: SimulationInput):

    baseline_df=run_logic(df_master, 0, 0, 0)
    baseline_profit=float(baseline_df['new_net_profit'].sum())

    result_df=run_logic(
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