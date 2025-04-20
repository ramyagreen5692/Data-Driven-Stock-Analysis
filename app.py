import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ---------- Secure DB Connection ----------
DATABASE_URL = "mysql+pymysql://KUjMcLa9iTZrfjU.root:Fd8vm7Rtr3stcucS@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Stock?ssl_ca=D:\\Streamlit\\isrgrootx.pem"
engine = create_engine(DATABASE_URL)

# ---------- Helper Function to Fetch Data ----------
def fetch_table(table_name):
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
        return df
    except Exception as e:
        st.error(f"Error loading {table_name}: {e}")
        return pd.DataFrame()

# ---------- Streamlit Layout ----------
st.set_page_config(layout="wide")
st.title("📊 Nifty 50 Stock Performance Dashboard")

# ---------- Volatility Analysis ----------
st.header("📉 Top 10 Most Volatile Stocks")
volatility_df = fetch_table("volatility_analysis")

if not volatility_df.empty:
    top_volatility = volatility_df.sort_values(by='volatility', ascending=False).head(10)
    fig_volatility = px.bar(top_volatility, x='ticker', y='volatility', title="Top 10 Most Volatile Stocks")
    st.plotly_chart(fig_volatility, use_container_width=True)
    st.markdown(
        "> 📈 **Insight:** These stocks have the highest price fluctuations, indicating high risk and potential high reward."
    )

# ---------- Cumulative Return ----------
st.header("📈 Cumulative Returns of Top 5 Performing Stocks")
cum_df = fetch_table("cumulative_returns")

if not cum_df.empty:
    top_stocks = cum_df.groupby("ticker")["cumulative_return"].max().sort_values(ascending=False).head(5).index
    top_cum_df = cum_df[cum_df["ticker"].isin(top_stocks)]
    fig_cum = px.line(top_cum_df, x='date', y='cumulative_return', color='ticker', title="Top 5 Stocks by Cumulative Return")
    st.plotly_chart(fig_cum, use_container_width=True)
    st.markdown(
        "> 🚀 **Insight:** These top 5 stocks have consistently outperformed others over time, indicating strong growth trends."
    )

# ---------- Sector-wise Performance ----------
st.header("🏢 Sector-wise Cumulative Return by Sector")
sector_df = fetch_table("sector_performance")

if not sector_df.empty:
    fig_sector = px.bar(
        sector_df,
        x='sector',
        y='cumulative_return',
        title="Cumulative Return by Sector",
        color='sector'
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    st.markdown(
        "> 🔍 **Insight:** Sectors with the highest average returns can guide long-term investment decisions."
    )

# ---------- Correlation Heatmap ----------
st.header("📊 Stock Price Correlation Heatmap")
corr_df = fetch_table("correlation_matrix")

if not corr_df.empty and {"ticker1", "ticker2", "correlation"}.issubset(corr_df.columns):
    pivot_corr = corr_df.pivot(index="ticker1", columns="ticker2", values="correlation")

    fig_corr = px.imshow(
        pivot_corr,
        labels=dict(color="correlation"),
        x=pivot_corr.columns,
        y=pivot_corr.index,
        title="Stock Price Correlation Heatmap",
        color_continuous_scale="RdBu",
        zmin=-1, zmax=1
    )

    fig_corr.update_layout(
        width=1000,
        height=1000,
        xaxis=dict(tickangle=45),
        margin=dict(l=50, r=50, t=80, b=100),
        font=dict(size=12)
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown(
        "> 🧰 **Insight:** Strongly correlated stocks often move together, which helps in risk diversification strategies."
    )
else:
    st.warning("Correlation matrix table doesn't have expected columns.")

# ---------- Monthly Top Gainers/Losers ----------
st.header("🗕️ Monthly Top 5 Gainers and Losers")
monthly_df = fetch_table("monthly_returns")

if not monthly_df.empty:
    selected_month = st.selectbox("Select a Month", sorted(monthly_df["month"].unique()))
    monthly_selected = monthly_df[monthly_df["month"] == selected_month]

    gainers = monthly_selected.sort_values(by="monthly_return", ascending=False).head(5)
    losers = monthly_selected.sort_values(by="monthly_return").head(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📈 Top 5 Gainers - {selected_month}")
        fig_gainers = px.bar(gainers, x="ticker", y="monthly_return", color="ticker")
        st.plotly_chart(fig_gainers, use_container_width=True)
        st.markdown(
            "> 📊 **Insight:** These stocks saw the highest monthly returns, possibly due to strong earnings, news, or sector momentum."
        )

    with col2:
        st.subheader(f"📉 Top 5 Losers - {selected_month}")
        fig_losers = px.bar(losers, x="ticker", y="monthly_return", color="ticker")
        st.plotly_chart(fig_losers, use_container_width=True)
        st.markdown(
            "> 📉 **Insight:** These underperforming stocks may indicate sector weakness or negative sentiment."
        )
