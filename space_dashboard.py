import pandas as pd
import streamlit as st
import plotly.express as px

# Page setup
st.set_page_config(page_title="🚀 Space Missions Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("space-mission-data.csv")
    df["country"] = df["location"].apply(lambda x: x.split(",")[-1].strip())
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filters")
companies = st.sidebar.multiselect("Select Companies", df["company"].unique(), default=None)
countries = st.sidebar.multiselect("Select Countries", df["country"].unique(), default=None)

filtered_df = df.copy()
if companies:
    filtered_df = filtered_df[filtered_df["company"].isin(companies)]
if countries:
    filtered_df = filtered_df[filtered_df["country"].isin(countries)]

# --- KPIs ---
total_missions = len(filtered_df)
success_rate = filtered_df["successful"].mean() * 100
avg_price = filtered_df["price"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Missions", total_missions)
col2.metric("Success Rate", f"{success_rate:.1f}%")
col3.metric("Average Launch Price", f"${avg_price:,.0f}")

st.markdown("---")

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    top_companies = filtered_df["company"].value_counts().head(10)
    fig1 = px.bar(top_companies, title="Top 10 Companies by Mission Count",
                  labels={"value": "Missions", "index": "Company"})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top_countries = filtered_df["country"].value_counts().head(10)
    fig2 = px.bar(top_countries, title="Top 10 Countries by Mission Count",
                  labels={"value": "Missions", "index": "Country"})
    st.plotly_chart(fig2, use_container_width=True)

# --- Timeline ---
fig3 = px.histogram(filtered_df, x="date", title="Missions Over Time", nbins=50)
st.plotly_chart(fig3, use_container_width=True)

# --- Scatter plot ---
fig4 = px.scatter(filtered_df, x="price", y="successful", color="company",
                  title="Launch Price vs Mission Success", hover_data=["mission"])
st.plotly_chart(fig4, use_container_width=True)

st.markdown("📊 *Data Source: Plotly Space Mission Dataset*")
