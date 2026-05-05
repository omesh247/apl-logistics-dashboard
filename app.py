import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="APL Logistics Dashboard", layout="wide")

# ==========================================
# 2. DATA LOADING & CLEANING
# ==========================================
@st.cache_data
def load_data():
    # Make sure your CSV file is named exactly 'your_cleaned_data.csv'
    df = pd.read_csv("your_cleaned_data.csv")
    
    # Force conversion for Sales and Profit (remove $, commas)
    columns_to_fix = ['Sales', 'Order Profit Per Order']
    for col in columns_to_fix:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Force conversion for Discount (remove %)
    if 'Order Item Discount Rate' in df.columns:
        df['Order Item Discount Rate'] = df['Order Item Discount Rate'].astype(str).str.replace('%', '', regex=False)
        df['Order Item Discount Rate'] = pd.to_numeric(df['Order Item Discount Rate'], errors='coerce') / 100.0
        
    return df

df = load_data()

# ==========================================
# 3. HEADER & FILTERS
# ==========================================
st.title("Global Supply Chain & Sales Overview")

# Create 3 columns to hold the specific required filters
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    market_filter = st.multiselect("Filter by Market / Region", options=df['Market'].dropna().unique())
with filter_col2:
    if 'Category Name' in df.columns:
        category_filter = st.multiselect("Filter by Category", options=df['Category Name'].dropna().unique())
    else:
        category_filter = []
with filter_col3:
    if 'Customer Segment' in df.columns:
        segment_filter = st.multiselect("Filter by Customer Segment", options=df['Customer Segment'].dropna().unique())
    else:
        segment_filter = []

# Connect all filters to the data
filtered_df = df.copy()
if market_filter:
    filtered_df = filtered_df[filtered_df['Market'].isin(market_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df['Category Name'].isin(category_filter)]
if segment_filter:
    filtered_df = filtered_df[filtered_df['Customer Segment'].isin(segment_filter)]

# ==========================================
# ROW 1: CORE KPIs
# ==========================================
st.markdown("---")
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Order Profit Per Order'].sum()
avg_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Revenue", f"${total_sales:,.2f}")
kpi2.metric("Total Profit", f"${total_profit:,.2f}")
kpi3.metric("Avg. Profit Margin", f"{avg_margin:.2f}%")

# ==========================================
# ROW 2: CATEGORY & DISCOUNT (Side-by-Side)
# ==========================================
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Profit by Category")
    if 'Category Name' in filtered_df.columns:
        cat_profit = filtered_df.groupby('Category Name')['Order Profit Per Order'].sum().reset_index()
        fig_cat = px.bar(cat_profit, x='Category Name', y='Order Profit Per Order')
        st.plotly_chart(fig_cat, use_container_width=True)

with chart_col2:
    st.subheader("Discount vs Profit Ratio")
    if 'Order Item Discount Rate' in filtered_df.columns and 'Order Item Profit Ratio' in filtered_df.columns:
        fig_discount = px.scatter(filtered_df, x='Order Item Discount Rate', y='Order Item Profit Ratio', color='Market')
        st.plotly_chart(fig_discount, use_container_width=True)

# ==========================================
# ROW 3: CUSTOMER ANALYSIS (Side-by-Side)
# ==========================================
st.markdown("---")
st.subheader("Customer Value Analysis")
cust_col1, cust_col2 = st.columns(2)

if 'Customer Id' in filtered_df.columns:
    customer_profit = filtered_df.groupby('Customer Id')['Order Profit Per Order'].sum().reset_index()
    top_customers = customer_profit.sort_values(by='Order Profit Per Order', ascending=False).head(10)
    bottom_customers = customer_profit.sort_values(by='Order Profit Per Order', ascending=True).head(10)

    with cust_col1:
        fig_top = px.bar(top_customers, x='Customer Id', y='Order Profit Per Order', color_discrete_sequence=['#2E8B57'], title="Top 10 VIP Customers")
        fig_top.update_xaxes(type='category') # Fixes the thin bar issue
        st.plotly_chart(fig_top, use_container_width=True)

    with cust_col2:
        fig_bot = px.bar(bottom_customers, x='Customer Id', y='Order Profit Per Order', color_discrete_sequence=['#DC143C'], title="Bottom 10 Loss-Making Customers")
        fig_bot.update_xaxes(type='category') # Fixes the thin bar issue
        st.plotly_chart(fig_bot, use_container_width=True)

# ==========================================
# ROW 4: REGIONAL HEATMAP
# ==========================================
st.markdown("---")
st.subheader("Regional Profitability Heatmap")
if 'Market' in filtered_df.columns and 'Order Region' in filtered_df.columns:
    market_profit = filtered_df.groupby(['Market', 'Order Region'])['Order Profit Per Order'].sum().reset_index()
    fig_market = px.treemap(market_profit, path=['Market', 'Order Region'], values=market_profit['Order Profit Per Order'].abs(),
                            color='Order Profit Per Order', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_market, use_container_width=True)

# ==========================================
# ROW 5: WHAT-IF SIMULATOR
# ==========================================
st.markdown("---")
st.subheader("What-If Scenario: Discount Impact Simulator")
simulated_discount = st.slider("Simulated Global Discount Rate (%)", min_value=0.0, max_value=30.0, value=5.0, step=1.0)

# Simulator Math
actual_revenue = filtered_df['Sales'].sum()
actual_profit = filtered_df['Order Profit Per Order'].sum()
actual_margin = (actual_profit / actual_revenue) * 100 if actual_revenue > 0 else 0

if 'Order Item Discount Rate' in filtered_df.columns:
    avg_current_discount = filtered_df['Order Item Discount Rate'].mean() * 100 if pd.notnull(filtered_df['Order Item Discount Rate'].mean()) else 0
else:
    avg_current_discount = 0

discount_difference = (simulated_discount - avg_current_discount) / 100
simulated_revenue = actual_revenue * (1 - discount_difference)
profit_impact = actual_revenue * discount_difference
simulated_profit = actual_profit - profit_impact
simulated_margin = (simulated_profit / simulated_revenue) * 100 if simulated_revenue > 0 else 0

sim_col1, sim_col2, sim_col3 = st.columns(3)
sim_col1.metric("Simulated Total Revenue", f"${simulated_revenue:,.2f}", f"${simulated_revenue - actual_revenue:,.2f}")
sim_col2.metric("Simulated Total Profit", f"${simulated_profit:,.2f}", f"${simulated_profit - actual_profit:,.2f}")
sim_col3.metric("Simulated Profit Margin", f"{simulated_margin:.2f}%", f"{simulated_margin - actual_margin:.2f}%")
