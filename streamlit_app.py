import streamlit as st
import requests

# Smoothie Customization App
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

# Display nutrition info for selected fruits
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
