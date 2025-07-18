import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📈 Moving Average Strategy Visualizer")

# --- Ticker and Date Input ---
ticker = st.text_input("Enter stock ticker (e.g., AAPL, SPY):", "AAPL")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", datetime(2023, 1, 1))
with col2:
    end_date = st.date_input("End date", datetime.today())

# --- MA Window Settings ---
col3, col4 = st.columns(2)
with col3:
    short_window = st.slider("Short MA window", 5, 50, 12)
with col4:
    long_window = st.slider("Long MA window", 10, 100, 26)

if ticker:
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.error("Couldn't fetch data. Try a different ticker.")
    else:
        df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
        df['Long_MA'] = df['Close'].rolling(window=long_window).mean()
        df['Signal'] = (df['Short_MA'] > df['Long_MA']).astype(int)

        # --- Plot Chart ---
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(df.index, df['Close'], label='Close Price')
        ax.plot(df.index, df['Short_MA'], label=f'{short_window}-day MA', linestyle='--')
        ax.plot(df.index, df['Long_MA'], label=f'{long_window}-day MA', linestyle='--')
        ax.fill_between(df.index, df['Close'].min(), df['Close'].max(),
                        where=df['Signal'] == 1, alpha=0.1, color='green', label='Long')
        ax.set_title(f"{ticker.upper()} - Moving Average Crossover")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
