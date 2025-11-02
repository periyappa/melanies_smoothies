import streamlit as st
import requests

# Existing smoothie customization app
st.title("🥤 Customize Your Smoothie!")

name_on_smoothie = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_smoothie)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    ["Apples", "Banana", "Cantaloupe", "Figs", "Watermelon"],
)

if st.button("Submit Order"):
    if name_on_smoothie:
        st.success(f"✅ Your Smoothie is ordered, {name_on_smoothie}!")
    else:
        st.warning("Please enter a name for your smoothie!")

# 🆕 New section to display SmoothieFroot nutrition information
# (Updated per task instructions)
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
