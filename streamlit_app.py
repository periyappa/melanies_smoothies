import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load the table from Snowflake
my_dataframe = session.table('smoothies.public.fruit_options').select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Display the dataframe (optional)
# st.dataframe(pd_df)

# Multiselect for choosing fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# Handle selected fruits
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Use Pandas LOC to find the SEARCH_ON value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Display the search value
        st.write('The search value for', fruit_chosen, 'is', search_on, '.')

        # Nutrition info section
        st.subheader(fruit_chosen + ' Nutrition Information')

        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        fv_data = fruityvice_response.json()

        # Display data
        if 'error' in fv_data:
            st.error("Not found")
        else:
            st.dataframe(fv_data)
