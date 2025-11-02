# Import required packages
import pandas as pd
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# App title
st.title(f"Example Streamlit App :balloon: {st.__version__}")

# Input: Name on order
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# Input: Fruit selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Input: Order filled checkbox
order_filled = st.checkbox('Mark order as filled')

# Submit button
submit = st.button('Submit Order')

if submit:
    if not name_on_order or not ingredients_list:
        st.error("Please enter a name and select at least one fruit.")
    else:
        # Build ingredients string in exact order with correct formatting
        ingredients_string = ', '.join(ingredients_list)

        # Optional: Display nutrition info
        for fruit_chosen in ingredients_list:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write(f"The search value for {fruit_chosen} is {search_on}.")
            response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            if response.status_code == 200 and isinstance(response.json(), list):
                st.subheader(f"{fruit_chosen} Nutrition Information")
                st.dataframe(data=response.json(), use_container_width=True)
            else:
                st.warning(f"⚠️ {fruit_chosen} is not in the nutrition database.")

        # Insert into orders table
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders(NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
            VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()}, CURRENT_TIMESTAMP)
        """
        session.sql(insert_stmt).collect()
        st.success(f"✅ Order submitted for {name_on_order} with ingredients: {ingredients_string}")
