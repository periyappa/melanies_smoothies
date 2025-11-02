import streamlit as st
import pandas as pd
import requests

st.title("🍓 Customize Your Smoothie!")

st.write("Choose the fruits you want in your custom Smoothie!")

name_on_smoothie = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_smoothie)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", 
                                  ["Avocado", "Banana", "Blackberry", "Blueberry", 
                                   "Cherry", "Coconut", "Fig", "Grape", 
                                   "Guava", "Kiwi", "Lemon", "Lime", 
                                   "Mango", "Orange", "Papaya", "Peach", 
                                   "Pineapple", "Pomegranate", "Raspberry", 
                                   "Strawberry", "Tangerine", "Watermelon", "Ximenia", "Yerba Mate"])

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefruit_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefruit_response.json(), use_container_width=True)
