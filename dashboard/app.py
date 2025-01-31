import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# **Helper function** untuk analisis data
def create_daily_summary(df):
    # Data summary harian
    daily_summary = df.groupby("dteday").agg({
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    }).reset_index()
    daily_summary.rename(columns={
        "cnt": "total_rentals",
        "registered": "registered_users",
        "casual": "casual_users"
    }, inplace=True)
    return daily_summary

def create_hourly_summary(df):
    # Data summary per jam
    hourly_summary = df.groupby("hr").agg({
        "cnt": "mean",
        "registered": "mean",
        "casual": "mean"
    }).reset_index()
    hourly_summary.rename(columns={
        "cnt": "avg_rentals",
        "registered": "avg_registered_users",
        "casual": "avg_casual_users"
    }, inplace=True)
    return hourly_summary

def create_season_summary(df):
    # Data summary berdasarkan musim
    season_summary = df.groupby("season").agg({
        "cnt": "sum"
    }).reset_index()
    season_summary.rename(columns={"cnt": "total_rentals"}, inplace=True)
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    season_summary["season"] = season_summary["season"].map(season_map)
    return season_summary

# Load dataset
day_data = pd.read_csv("../data/day.csv")
hour_data = pd.read_csv("../data/hour.csv")

# Konversi tanggal
day_data["dteday"] = pd.to_datetime(day_data["dteday"])

# Siapkan summary data
daily_summary = create_daily_summary(day_data)
hourly_summary = create_hourly_summary(hour_data)
season_summary = create_season_summary(day_data)

# Sidebar: Filter rentang tanggal
with st.sidebar:
    st.title("Filter Data")
    min_date = day_data["dteday"].min()
    max_date = day_data["dteday"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Filter data berdasarkan tanggal
    filtered_daily = daily_summary[
        (daily_summary["dteday"] >= pd.Timestamp(start_date)) & 
        (daily_summary["dteday"] <= pd.Timestamp(end_date))
    ]

# Dashboard Header
st.header("Dashboard Penyewaan Sepeda :bike:")
st.caption("Data analisis dari day.csv dan hour.csv")

# **1. Daily Summary**
st.subheader("Total Penyewaan Harian")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = filtered_daily["total_rentals"].sum()
    st.metric("Total Rentals", total_rentals)

with col2:
    total_registered = filtered_daily["registered_users"].sum()
    st.metric("Total Registered Users", total_registered)

with col3:
    total_casual = filtered_daily["casual_users"].sum()
    st.metric("Total Casual Users", total_casual)

# Line plot total rentals harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(filtered_daily["dteday"], filtered_daily["total_rentals"], marker='o', color="#90CAF9")
ax.set_title("Total Rentals Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
st.pyplot(fig)

# **2. Hourly Summary**
st.subheader("Rata-rata Penyewaan Per Jam")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="hr", y="avg_rentals", data=hourly_summary, marker='o', color="#FFA726", ax=ax)
ax.set_title("Rata-rata Penyewaan per Jam", fontsize=20)
ax.set_xlabel("Jam", fontsize=15)
ax.set_ylabel("Rata-rata Rentals", fontsize=15)
st.pyplot(fig)

# **3. Seasonal Summary**
st.subheader("Penyewaan Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x="season", y="total_rentals", data=season_summary, palette="Blues", ax=ax)
ax.set_title("Penyewaan Berdasarkan Musim", fontsize=20)
ax.set_xlabel("Musim", fontsize=15)
ax.set_ylabel("Total Rentals", fontsize=15)
st.pyplot(fig)

# Footer
st.caption("Copyright © Your Project 2023")
