import streamlit as st 
import requests
import pandas as pd 
import plotly.graph_objects as go

st.set_page_config(page_title="Profit Engine Dashboard", layout="wide")

st.title("Omnichannel Profit Optimization Simulator")
st.write("Adjust levers below to see the impact on global profit.")

# --- SIDEBAR ---
st.sidebar.header("Simulation Parameters")

# Sliders for user input
mkt = st.sidebar.slider("Marketing Change (%)", -50, 100, 5) / 100
ret = st.sidebar.slider("Return Improvement (%)", 0, 100, 20) / 100
shipp = st.sidebar.slider("Shipping Cost Shock (%)", 0, 100, 10) / 100

# --- API CONFIGURATION ---
API_URL = "https://omnichannel-profit-optimization-engine.onrender.com/simulate"

# --- ACTION BUTTON ---
if st.button("Run Simulation"):
    payload = {
        "mkt_change": mkt,
        "return_improve": ret,
        "shipping_cost_shock": shipp
    }

    try:
        # Sending the request to the FastAPI backend
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            baseline_profit = result['baseline_profit']
            new_profit = result['simulated_profit']
            wf = result['waterfall']

            # METRIC CALCULATIONS
            delta = new_profit - baseline_profit
            pct_change = (delta / abs(baseline_profit)) * 100 if baseline_profit != 0 else 0

            # DISPLAY METRICS
            col1, col2, col3 = st.columns(3)
            col1.metric("Baseline Profit", f"${baseline_profit:,.0f}")
            col2.metric("Simulated Profit", f"${new_profit:,.0f}")
            col3.metric("Change", f"${delta:,.0f}", f"{pct_change:.2f}%")

            # STATUS ALERTS
            if new_profit < 0:
                st.warning("The profit is still in LOSS. Further optimization needed!")
            else: 
                st.success("Target achieved! The company is now PROFITABLE!")

            # WATERFALL CHART VISUALIZATION
            fig = go.Figure(go.Waterfall(
                orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total"],
                x = ["Gross", "COGS", "Returns", "Shipping", "Marketing", "Labor", "Net Profit"],
                y = [
                    wf['Gross'], 
                    -wf['COGS'], 
                    -wf['Returns_Loss'], 
                    -wf['Shipping'], 
                    -wf['Marketing'], 
                    -wf['Labor'], 
                    wf['Net_Profit']
                ],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
                decreasing = {"marker":{"color":"#EF553B"}},
                increasing = {"marker":{"color":"#00CC96"}},
                totals = {"marker":{"color":"#636EFA"}}
            ))
            
            fig.update_layout(
                title = "Simulated Profit Waterfall", 
                showlegend = False,
                height = 600
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error(f"API Error: {response.status_code}. Please check if the backend service is running.")
            
    except Exception as e:
        st.error(f"Connection Failed: Could not reach the API. Error: {e}")
