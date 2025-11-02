from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Session
import streamlit as st

st.title("🍓 Customize Your Smoothie!")

# Text input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Try to get active session or create one if missing
try:
    session = get_active_session()
except Exception:
    session = Session.builder.getOrCreate()

# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME", "SEARCH_ON")

st.dataframe(data=my_dataframe, use_container_width=True)

st.stop()

ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe)
