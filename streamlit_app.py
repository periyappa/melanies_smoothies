# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  # previous import from earlier task

# Create Snowflake connection (SniS style)
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:' ,name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    combined_value = ingredients_string + " (" + name_on_order + ")"

    my_insert_stmt = f"""
       INSERT INTO smoothies.public.orders(ingredients)
    VALUES ('{combined_value}')
"""

    time_to_insert = st.button('Submit Order')

    if time
