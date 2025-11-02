import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie!")

# Text input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options from Snowflake
my_dataframe = session.table('smoothies.public.fruit_options').select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# Convert Snowpark DataFrame → Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Multiselect for up to 5 fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# When fruits are selected
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        # Use Pandas loc to get the SEARCH_ON value
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Display the search value (optional)
        # st.write('The search value for', fruit_chosen, 'is', search_on, '.')

        # Display nutrition info header
        st.subheader(fruit_chosen + ' Nutrition Information')

        # Use the SEARCH_ON value in the API call
        smoothiefruit_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        # Convert response to JSON and display as dataframe
        st.dataframe(
            data=smoothiefruit_response.json(),
            use_container_width=True
        )
