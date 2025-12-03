import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🍽️ Zomato Interactive Analysis Dashboard")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Location dropdown
location = st.sidebar.selectbox("📍 Select Location", sorted(df.location.unique()))

# Top N dropdown
top_n = st.sidebar.selectbox("🔢 Show Top Restaurants", [5, 10, 15, 20], index=1)

# Sorting dropdown
sort_by = st.sidebar.selectbox("📊 Sort By", ["rate", "approx_cost"])

# Restaurant name search
search_text = st.sidebar.text_input("🔎 Search Restaurant Name (optional)").lower()

# Filter dataset
filtered_df = df[df.location == location]

if search_text:
    filtered_df = filtered_df[filtered_df['name'].str.lower().str.contains(search_text)]

# Group & sort
gr = (
    filtered_df.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .sort_values(by=sort_by, ascending=False)
    .head(top_n)
    .reset_index()
)

# Display selected info
st.subheader(f"📍 Top {top_n} Restaurants in **{location}** Sorted by **{sort_by.capitalize()}**")

# Plot
fig, ax = plt.subplots(figsize=(14, 7))
sb.barplot(data=gr, x='name', y=sort_by, palette='viridis', ax=ax)
plt.xticks(rotation=45, ha='right')
plt
