import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zomato Cost vs Rating", layout="wide")

st.title("🍽️ Zomato Restaurant Rating & Cost Analysis")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("../Datasets/zomato.csv")

    # Drop unwanted columns
    df = df.drop(
        ['url','phone','address','reviews_list','menu_item',
         'listed_in(type)','listed_in(city)'], 
        axis=1
    )

    # Rename and clean
    df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
    df = df.fillna(0)
    df.approx_cost = df.approx_cost.replace('[,]', '', regex=True).astype('int64')

    df.rate = df.rate.replace('[/5]', '', regex=True)
    df.rate = df.rate.replace(['NEW', '-'], 0).astype('float64')

    return df

df = load_data()

# Sidebar for selecting location
st.sidebar.header("Filters")
locations = sorted(df.location.unique())
location_choice = st.sidebar.selectbox("Select a Location:", locations)

# Filter dataset based on location
filtered_df = df[df.location == location_choice]

st.subheader(f"📍 Top 10 Restaurants in **{location_choice}** by Rating")

# Group and plot
gr = (
    filtered_df.groupby('name')[['rate', 'approx_cost']]
    .mean()
    .nlargest(10, 'rate')
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 6))
sb.barplot(data=gr, x="name", y="approx_cost", palette="summer", ax=ax)
plt.xticks(rotation=45, ha='right')
plt.ylabel("Approx Cost for Two")
plt.xlabel("Restaurant Name")

st.pyplot(fig)

# Show raw table if user wants
if st.checkbox("Show Raw Data"):
    st.write(df)
