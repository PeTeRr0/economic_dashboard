# app.py

import streamlit as st
import plotly.express as px
from data import (
    get_us_gdp,
    get_unemployment_rate,
    get_financial_stress_index,
)
from trading_economics_data import (
    get_global_stock_indices,
    get_index_historical_data,
)
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Economic Dashboard",
    page_icon="💹",
    layout="wide",
)

# Sidebar options
st.sidebar.title("Navigation")
options = st.sidebar.selectbox(
    "Select a section:",
    ("Overview", "U.S. GDP", "U.S. Unemployment Rate", "Overall Risk Index", "Global Stock Indices"),
)

# Main content
if options == "Overview":
    st.title("💹 Economic Dashboard")
    st.write("""
    Welcome to the Economic Dashboard. Navigate through the sections using the sidebar to explore various economic indicators and financial data.
    """)
elif options == "U.S. GDP":
    st.header("🇺🇸 U.S. Gross Domestic Product (GDP)")
    df_gdp = get_us_gdp()
    if df_gdp.empty:
        st.write("No GDP data available for the last 100 days.")
    else:
        st.write("### GDP Over the Last 100 Days")
        fig = px.line(df_gdp, x='Date', y='Value', title='U.S. GDP Over the Last 100 Days', labels={'Value': 'GDP Value'})
        st.plotly_chart(fig)
        st.write("### Recent GDP Data")
        st.write(df_gdp.tail())
elif options == "U.S. Unemployment Rate":
    st.header("📈 U.S. Unemployment Rate")
    df_unemployment = get_unemployment_rate()
    if df_unemployment.empty:
        st.write("No unemployment rate data available for the last 100 days.")
    else:
        st.write("### Unemployment Rate Over the Last 100 Days")
        fig = px.line(df_unemployment, x='Date', y='Value', title='U.S. Unemployment Rate Over the Last 100 Days', labels={'Value': 'Unemployment Rate (%)'})
        st.plotly_chart(fig)
        st.write("### Recent Unemployment Data")
        st.write(df_unemployment.tail())
elif options == "Overall Risk Index":
    st.header("⚠️ Overall Financial Stress Index")
    df_stress = get_financial_stress_index()
    if df_stress.empty:
        st.write("No financial stress index data available for the last 100 days.")
    else:
        latest_value_percent = df_stress['Value_Percent'].iloc[-1]
        # Define risk levels based on percentage
        if latest_value_percent <= 20:
            risk_level = "Very Safe"
            color = "green"
        elif 20 < latest_value_percent <= 40:
            risk_level = "Safe"
            color = "lightgreen"
        elif 40 < latest_value_percent <= 60:
            risk_level = "Neutral"
            color = "yellow"
        elif 60 < latest_value_percent <= 80:
            risk_level = "Risky"
            color = "orange"
        else:
            risk_level = "Very Risky"
            color = "red"

        # Display current index value and risk level
        st.markdown(
            f"<h3 style='color:{color};'>Current Financial Stress Index: {latest_value_percent:.2f}%</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h3 style='color:{color};'>Risk Level: {risk_level}</h3>",
            unsafe_allow_html=True
        )

        # Display the index over time
        st.write("### Financial Stress Index Over Time (Percentage)")
        fig = px.line(
            df_stress, x='Date', y='Value_Percent', title='Financial Stress Index Over Time (Percentage)',
            labels={'Value_Percent': 'Financial Stress Index (%)'}
        )
        st.plotly_chart(fig)

        # Display recent data
        st.write("### Recent Financial Stress Index Data")
        st.write(df_stress[['Date', 'Value_Percent']].tail())
elif options == "Global Stock Indices":
    st.header("📊 Global Stock Market Indices")
    df_indices = get_global_stock_indices()
    if df_indices.empty:
        st.write("No global stock indices data available.")
    else:
        st.write("### Real-Time Global Stock Indices")
        st.dataframe(df_indices[['symbol', 'name', 'close', 'daily_change', 'daily_percentual_change']].head(50))

        # Fetch and display historical data for selected indices
        st.write("### Historical Data for Selected Indices (Last 100 Days)")
        selected_indices = st.multiselect(
            "Select Indices",
            options=df_indices['symbol'].unique(),
            default=df_indices['symbol'].unique()[:5]
        )
        for symbol in selected_indices:
            df_hist = get_index_historical_data(symbol)
            if not df_hist.empty:
                df_hist['DateTime'] = pd.to_datetime(df_hist['DateTime'])
                df_hist = df_hist.sort_values('DateTime')
                st.write(f"**{symbol} Historical Data**")
                fig = px.line(df_hist, x='DateTime', y='Close', title=f'{symbol} Closing Prices Over Last 100 Days')
                st.plotly_chart(fig)
            else:
                st.write(f"No historical data available for {symbol}")
