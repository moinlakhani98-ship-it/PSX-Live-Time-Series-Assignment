import datetime
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="PSX Stocks Analysis", layout="wide")

st.title("📊 PSX Stocks Analysis Dashboard")
st.write("Pakistan Stock Exchange stocks ka price trend, returns, risk aur correlation analysis.")

try:
    import psxdata
except ImportError:
    st.error("psxdata library install nahi hai. Terminal mein yeh chalayein: pip install psxdata")
    st.stop()

# ---- Sidebar Inputs ----
st.sidebar.header("Settings")
all_stocks = ["FCCL", "OGDC", "PPL", "MEBL", "HBL"]
stocks_list = st.sidebar.multiselect(
    "PSX Stocks select karein",
    all_stocks,
    default=all_stocks
)

start_date = st.sidebar.date_input("Start Date", datetime.date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

if st.sidebar.button("Run Analysis"):
    if not stocks_list:
        st.warning("Kam se kam ek stock select karein.")
        st.stop()

    stocks_df = pd.DataFrame()

    with st.spinner("PSX se data download ho raha hai..."):
        for stock in stocks_list:
            st.write(f"Downloading {stock}...")
            data = psxdata.stocks(
                stock,
                start=str(start_date),
                end=str(end_date)
            )
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values('date')
            data = data.set_index('date')
            data = data[~data.index.duplicated(keep='last')]
            stocks_df[stock] = data['close']

        stocks_df = stocks_df.sort_index()

    st.subheader("📄 Latest Data")
    col1, col2 = st.columns(2)
    with col1:
        st.write("First 5 rows")
        st.dataframe(stocks_df.head().style.background_gradient(cmap="viridis"))
    with col2:
        st.write("Last 5 rows")
        st.dataframe(stocks_df.tail().style.background_gradient(cmap="plasma"))

    # ---- Price Trend Chart ----
    st.subheader("📈 Price Trend")
    fig = px.line(
        stocks_df,
        title="PSX Stocks Trend Analysis",
        labels={"date": "Tareeq (Date)", "value": "Stock Price (PKR)"},
        template="plotly_dark"
    )
    fig.update_layout(hovermode="x unified", title_font_size=20, legend_title_text="Company Stocks")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Daily Returns ----
    returns_df = stocks_df.pct_change() * 100
    st.subheader("📊 Daily Returns (%)")
    st.dataframe(returns_df.head().style.background_gradient(cmap="coolwarm"))

    # ---- Cumulative Returns ----
    cumulative_returns_pct = ((1 + stocks_df.pct_change()).cumprod() - 1) * 100
    st.subheader("💰 Cumulative Returns Over Time")
    st.dataframe(cumulative_returns_pct.tail().style.background_gradient(cmap="viridis"))

    fig_cum = px.line(
        cumulative_returns_pct,
        title=f"Investment Growth (%) Since {start_date}",
        labels={"date": "Tareeq (Date)", "value": "Total Return (%)"},
        template="plotly_dark"
    )
    fig_cum.update_layout(hovermode="x unified", title_font_size=20)
    st.plotly_chart(fig_cum, use_container_width=True)

    # ---- Correlation Heatmap ----
    st.subheader("🔗 Stocks Correlation Matrix")
    correlation_matrix = stocks_df.pct_change().corr()
    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Stocks Correlation Matrix (Co-movement)",
        color_continuous_scale="RdBu",
        template="plotly_dark"
    )
    fig_corr.update_layout(title_font_size=20)
    st.plotly_chart(fig_corr, use_container_width=True)

    # ---- Summary Card ----
    st.subheader("🏁 Stock Performance Summary")
    summary_data = {
        "Total Return (%)": cumulative_returns_pct.iloc[-1],
        "Daily Volatility / Risk (%)": stocks_df.pct_change().std() * 100
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(
        summary_df.style
        .background_gradient(cmap="coolwarm", subset=["Total Return (%)"])
        .background_gradient(cmap="YlOrRd", subset=["Daily Volatility / Risk (%)"])
        .format("{:.2f}%")
    )

else:
    st.info("👈 Sidebar se stocks aur date range choose karke 'Run Analysis' dabayein.")
