# APL Logistics — Commercial Intelligence Dashboard

A full-stack supply chain analytics web app built with Python and Streamlit, designed to give logistics and operations teams real-time visibility into revenue, profitability, and customer value across global markets.

![Dashboard Preview](screenshot.png)
> 📸 *Add a screenshot of your running app here — drag it into the repo and update this path*

**[▶ Live Demo](https://apl-logistics-dashboard-683uc2txfeyzt36fmsbfc9.streamlit.app/)**
> 🔗 *Deploy to [Streamlit Community Cloud](https://streamlit.io/cloud) for free and paste your URL here*

---

## The Business Problem

Supply chain profitability data was scattered across markets, regions, and customer segments — making it impossible to quickly identify which customers were generating losses, where discounts were eroding margins, and how pricing changes would impact the bottom line.

---

## What This Dashboard Does

### KPI Summary
Live metrics for total revenue, total profit, and average profit margin — filterable by market, product category, and customer segment.

### Customer Value Analysis
Ranks customers into top 10 value generators and bottom 10 loss-makers, enabling targeted retention and repricing decisions.

### Discount vs Profit Scatter
Visualises the relationship between discount rates and profit ratios across markets — exposing where discounting is actively destroying margin.

### Regional Profitability Treemap
Hierarchical heatmap of profit across markets and sub-regions using a red-green colour scale for instant identification of underperforming territories.

### What-If Discount Simulator ⭐
Interactive slider that models the revenue, profit, and margin impact of changing the global discount rate — giving decision-makers a risk-free way to test pricing scenarios before committing.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3 |
| Web App | Streamlit |
| Data Processing | Pandas |
| Visualisation | Plotly Express |
| Data | CSV (cleaned supply chain dataset) |

---

## How to Run Locally

```bash
git clone https://github.com/omesh247/apl-logistics-dashboard
cd apl-logistics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## Key Features at a Glance

- Multi-filter sidebar (market, category, customer segment)
- All charts update dynamically based on active filters
- What-if simulator with live delta metrics
- Treemap with profit-loss colour coding

---

## About

Built during a Data Analytics Fellowship at Unified Mentor as part of a commercial intelligence project for APL Logistics. The goal was to replace static reports with an interactive tool that lets teams explore margin erosion and customer profitability without needing SQL or Excel.
