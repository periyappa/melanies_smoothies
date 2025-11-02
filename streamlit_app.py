import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🍓 Customize Your Smoothie!")

# Text input for smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Get the current Snowflake session
session = get_active_session()

# Load fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Display dataframe to verify the SEARCH_ON column
st.dataframe(data=my_dataframe, use_container_width=True)

# Stop execution here temporarily
st.stop()

# Multiselect to choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)
