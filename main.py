import streamlit as st 
import yfinance as yf 
import pandas as pd

st.title("Stock Market Dashboard")
tickers = ('TSLA', 'AAP', 'MSFT', 'BTC-USD', 'ETH-USD', 'GOOGL', 'AMZN', 'AAPL', 'NFLX', 'NVDA')

# Sidebar for user input
st.sidebar.header("Settings")
dropdown = st.sidebar.multiselect('Pick your assets', tickers)
start = st.sidebar.date_input('Start date', value=pd.to_datetime('2023-01-01'))
end = st.sidebar.date_input('End date', value=pd.to_datetime('today'))

# Function to calculate cumulative returns
def relativeret(df):
    rel = df.pct_change()
    cumret = (1 + rel).cumprod() - 1
    cumret = cumret.fillna(0)
    return cumret

# Fetch and display data
if len(dropdown) > 0:
    df = relativeret(yf.download(dropdown, start=start, end=end)['Adj Close'])
    st.header('{}'. format(dropdown))
    st.line_chart(df)

    # Display raw data in a table
    st.write("Raw Data:")
    st.dataframe(yf.download(dropdown, start=start, end=end)['Adj Close'])

    # Display descriptive statistics
    st.write("Descriptive Statistics:")
    st.write(df.describe())

    # Add a download button for CSV
    csv_export_button = st.button("Export Data to CSV")
    if csv_export_button:
        df.to_csv('cumulative_returns_data.csv', index=False)
        st.success("Data exported to 'cumulative_returns_data.csv'")

    # Add informative text
    st.markdown("""
    * Cumulative Return: The cumulative return is calculated based on the percentage change in the adjusted close prices.
    """)
