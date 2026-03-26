# Omnichannel-Profit-Optimization-Engine

## 🚀 Live Demo
You can access the interactive simulation dashboard here: 
[Profit Optimization Engine - Live Dashboard](https://omnichannel-profit-optimization-engine-hvvkn5b5lgzrxmswescfmr.streamlit.app/)


🚨 **Despite generating $1.98B in revenue, this company is losing $617M.**

This project builds a decision engine to identify why  and simulate how to fix it.


📌 **Executive Summary**
This project delivers a high-performance decision-support system for a global e-commerce entity operating in Turkey, Germany, and the UAE across D2C and B2B channels. Despite generating approximately $1.98 Billion in gross revenue, the company faced a critical $617.8 Million net loss.

This platform transforms static historical data into an interactive simulation engine, allowing executives to test "What-If" scenarios regarding marketing spend, return rates, and shipping shocks in seconds.
<img width="793" height="375" alt="Baseline-Profit" src="https://github.com/user-attachments/assets/f23e0c51-daba-48ed-b153-8fdb75d3f5d1" />
<img width="793" height="375" alt="Baseline Simulated-Waterfall" src="https://github.com/user-attachments/assets/d75c7cb6-5037-4e0e-86c7-de0f0dae3d7c" />
<img width="793" height="375" alt="Profit-Per-Order-Country-Segment" src="https://github.com/user-attachments/assets/d9210c64-0a6a-47ae-979c-9302ec3288fd" />

---

📉 **The Business Challenge (Data-Driven Insights)**
Comprehensive analysis identified several critical "Profit Leaks":

Erosive Return Rates: An overall 17.81% return rate significantly impacts the bottom line, resulting in a $178.6 Million loss in net revenue.

Segment-Specific Crises:

Efficiency Crisis (UAE D2C Entry): This segment exhibits the lowest efficiency with a profit margin plummeting to -34.89%.

Unit Loss Crisis (Germany B2B Premium): Analysis shows the highest loss per order occurs in this segment, reaching up to -$10,000 per transaction.

FX & Operational Pressure: With COGS and shipping costs heavily influenced by USD exposure, international logistics costs ($197.2M) create unpredictable margin pressure.

Marketing Inefficiency: High spending in segments with negative ROI prevents top-line growth from converting into sustainable profit.

---

🎯 **Project Objectives & Strategic Goals**
The core mission is to provide an actionable framework for profit stabilization:

Granular Profitability Mapping: Visualizing net margins across Country x Channel x Segment using multidimensional heatmaps.

Real-time Scenario Simulation: Utilizing a Waterfall architecture to monitor how variables like marketing shifts or shipping cost shocks affect the final net profit.

Strategic Optimization: Identifying "Quick Win" segments (e.g., UAE D2C Entry) where targeted interventions in return rates can maximize investment efficiency.

---

🛠️ **Technology Stack & Architecture**
Built on a modern data science stack designed for speed and scalability:

FastAPI: Serves the simulation logic as a high-performance, asynchronous backend API.

Streamlit: Provides a user-centric frontend with interactive sliders for real-time strategic testing.

Pandas & NumPy: Handles complex calculations across 300K+ rows of simulated transaction data.

Plotly: Powers dynamic Waterfall and Heatmap visualizations.

PostgreSQL / SQLAlchemy: Ensures production-ready data persistence and structured querying.

---

📊 **Success Metrics**
Decision Agility: Reduced complex "What-If" analysis time from hours (manual Excel) to under 1 second.

Impact Potential: Simulations demonstrate that a 20% improvement in return rates can reduce total losses by over $140 Million.

Model Consistency:The generated data maintains internal consistency across financial metrics and business logic.

---

👤 **User Stories**
Marketing Manager: "If I increase the D2C Premium budget by 20% while reducing returns by 10%, how does the net margin shift?"

Operations Director: "How will a 15% shock in shipping costs (FX-driven) impact our German B2B segment viability?"

---

📂 **Data Architecture**

The schema is designed to enable full traceability from order-level transactions to final profitability metrics.

orders: Core transaction data (Country, Channel, Segment, Revenue).

cost_structure: Detailed breakdown of COGS, labor, shipping, and marketing.

behavior: Tracking return status and payment cycles.

fx_rates: Historical and simulated currency conversion rates.

---

🚀 **Recommended Strategy**

Based on simulation results, the most effective path to reduce losses is:

1. Prioritize return rate reduction in D2C channels
   → Even a 20% improvement reduces losses significantly

2. Reduce exposure to unprofitable B2B Premium segments
   → High loss per order makes this segment structurally unsustainable

3. Optimize marketing allocation
   → Shift budget toward segments with lower return rates and higher efficiency

4. Closely monitor shipping cost volatility (FX-driven)
   → Implement dynamic pricing or cost controls
   
---

👉 **Key Insight:**
Profitability improvement is not driven by revenue growth, but by cost and return optimization.
The primary driver of losses is not insufficient revenue, but structural inefficiencies:

- High return rates eliminate realized revenue
- COGS nearly equals gross revenue, leaving no margin buffer
- Fixed costs (marketing, logistics, labor) push the business into negative profitability

👉 This indicates a fundamentally broken unit economics model.


💡 **Final Takeaway:**
This is not a revenue problem  it is a unit economics problem.

Without structural fixes, scaling revenue will only scale losses.


---

## 👤 Author

**Melek İkiz**  
Building data-driven decision systems  

📍 Türkiye  
🔗 LinkedIn: [(https://www.linkedin.com/in/melek-ikiz-520065373/)] 

