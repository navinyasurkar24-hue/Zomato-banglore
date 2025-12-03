import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

st.title("🍽️ Zomato Analysis – Top 10 Restaurants by Rating")

# Load Zomato Live Dataset
df = pd.read_csv("Zomato_Live.csv")

# Dropdown for location (replacing input())
location = st.selectbox("Select Location:", sorted(df.location.unique()))

# Filter based on selected location
lo = df[df.location == location]

# Grouping: top 10 by rating
gr = (
    lo.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

# Plot the bar chart
st.subheader(f"Top 10 Restaurants in {location} by Rating")

fig, ax = plt.subplots(figsize=(16, 6))
sb.barplot(x=gr['name'], y=gr['approx_cost'], palette='summer', ax=ax)
plt.xticks(rotation=45, ha='right')
plt.ylabel("Approx Cost for Two")
plt.xlabel("Restaurant Name")

st.pyplot(fig)
