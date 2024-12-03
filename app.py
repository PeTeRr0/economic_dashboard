# app.py

import streamlit as st
from data import (
    get_us_gdp,
    get_unemployment_rate,
    get_financial_stress_index,
)
from trading_economics_data import (
    get_global_stock_indices,
    get_index_historical_data,
)


st.set_page_config(page_title="Economic Dashboard", page_icon="💹", layout="wide")

st.sidebar.title("Navigation")
options = st.sidebar.selectbox(
    "Select a section:",
    ["Overview", "U.S. GDP", "U.S. Unemployment Rate", "Overall Risk Index", "Global Stock Indices"],
)

if options == "Overview":
    st.title("💹 Economic Dashboard")
    st.write("Welcome to the Economic Dashboard! This tool provides a real-time overview of key economic indicators.")
elif options == "U.S. GDP":
    st.header("U.S. Gross Domestic Product (GDP)")
    df_gdp = get_us_gdp()
    if not df_gdp.empty:
        st.line_chart(df_gdp.set_index("Date")["Value"])
        st.write("Recent GDP Data")
        st.write(df_gdp.tail())
elif options == "U.S. Unemployment Rate":
    st.header("U.S. Unemployment Rate")
    df_unemployment = get_unemployment_rate()
    if not df_unemployment.empty:
        st.line_chart(df_unemployment.set_index("Date")["Value"])
        st.write("Recent Unemployment Data")
        st.write(df_unemployment.tail())
elif options == "Overall Risk Index":
    st.header("Overall Financial Stress Index")
    df_stress = get_financial_stress_index()
    if not df_stress.empty:
        st.line_chart(df_stress.set_index("Date")["Value_Percent"])
        st.write("Recent Financial Stress Index Data")
        st.write(df_stress.tail())
elif options == "Global Stock Indices":
    st.header("Global Stock Market Indices")
    df_indices = get_global_stock_indices()
    if not df_indices.empty:
        st.write("Real-Time Global Stock Indices")
        st.dataframe(df_indices.head(50))
