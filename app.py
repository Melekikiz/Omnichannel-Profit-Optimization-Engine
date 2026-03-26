import streamlit as st 
import requests
import pandas as pd 
import plotly.graph_objects as go

st.set_page_config(page_title="Profit Engine Dashboard", layout="wide")

st.title("Omnichannel Profit Optimization Simulator")
st.write("Adjust levers below to see the impact on global profit.")

#Sidebar
st.sidebar.header("Simulation Parameters")
mkt = st.sidebar.slider("Marketing Change (%)", -50, 100, 5) / 100
ret=st.sidebar.slider("Return Improvement (%)", 0, 100, 20) / 100
shipp = st.sidebar.slider("Shipping Cost Shock (%)", 0, 100, 10) /100

#Api call
if st.button("Run Simulation"):
    payload={
        "mkt_change": mkt,
        "return_improve":ret,
        "shipping_cost_shock": shipp
    }

    response = requests.post("http://127.0.1:8000/simulate", json=payload)

    if response.status_code == 200:
        result = response.json()
        baseline_profit=result['baseline_profit']
        new_profit = result['simulated_profit']
        wf = result['waterfall']

        

        
        delta = new_profit - baseline_profit
        pct_change = (delta / abs(baseline_profit)) * 100 if baseline_profit != 0 else 0

        col1, col2, col3 = st.columns(3)

        col1.metric("Baseline Profit", f"${baseline_profit:,.0f}")
        col2.metric("Simulated Profit", f"${new_profit:,.0f}")
        col3.metric("Change", f"${delta:,.0f}", f"{pct_change:.2f}%")

        

        if new_profit < 0:
            st.warning("The profit is still in LOSS. Further optimization needed!")
        else: 
            st.success("Target achieved! The company is now PROFITABLE!")

        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x = ["Gross", "COGS", "Returns", "Shipping", "Marketing", "Labor", "Net Profit"],
            y = [wf['Gross'], -wf['COGS'], -wf['Returns_Loss'], -wf['Shipping'], -wf['Marketing'], -wf['Labor'], wf['Net_Profit']],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"#EF553B"}},
            increasing = {"marker":{"color":"#00CC96"}},
            totals = {"marker":{"color":"#636EFA"}}
        ))
        fig.update_layout(title = "Simulated Profit Waterfall", showlegend = False)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("API connection failed. Please try again later.")

    
   
    