import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.title("🍽️ Zomato Analysis – Top 10 Restaurants by Rating")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Show unique locations
st.write("### Available Locations:")
st.write(df.location.unique())

# Location input using dropdown
location = st.selectbox("Select Location:", sorted(df.location.unique()))

# Filter location data
lo = df[df.location == location]

# Group and get top restaurants
gr = (
    lo.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

# Plot
st.write(f"### Top 10 Restaurants in {location} by Rating")

fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(data=gr, x='name', y='approx_cost', palette='summer', ax=ax)
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)
