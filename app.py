import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🍽️ Zomato Dashboard – Interactive Dropdowns Only")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# --- SIDEBAR DROPDOWN CONTROLS ---
st.sidebar.header("🔽 Dashboard Filters")

# Dropdown 1 → Select Location
location = st.sidebar.selectbox("📍 Select Location", sorted(df.location.unique()))

# Dropdown 2 → Select metric to visualize
metric = st.sidebar.selectbox(
    "📊 Select Metric to Display",
    ["rate", "approx_cost"]
)

# Dropdown 3 → Select number of restaurants
top_n = st.sidebar.selectbox(
    "🔢 Select Top N Restaurants",
    [5, 10, 15, 20],
    index=1
)

# --- FILTERING AND GROUPING ---
filtered = df[df.location == location]

gr = (
    filtered.groupby("name")[[ "rate", "approx_cost" ]]
    .mean()
    .sort_values(by=metric, ascending=False)
    .head(top_n)
    .reset_index()
)

# --- HEADER ---
st.subheader(
    f"📍 Top {top_n} Restaurants in **{location}** by **{metric}**"
)

# --- PLOT ---
fig, ax = plt.subplots(figsize=(14, 7))
sb.barplot(data=gr, x='name', y=metric, palette='summer', ax=ax)
plt.xticks(rotation=45, ha='right')
plt.xlabel("Restaurant Name")
plt.ylabel(metric.replace("_", " ").title())

st.pyplot(fig)
