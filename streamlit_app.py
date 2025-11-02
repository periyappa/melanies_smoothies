# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# --- Streamlit UI ---
st.title("🥤 Customize Your Smoothie!")
st.write("""
Welcome to the Smoothie Customizer app.  
Choose your fruits, see their nutrition info, and place your order below!
""")

# --- Get name for the order ---
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# --- Checkbox to mark order as filled ---
order_filled = st.checkbox('Mark the order as filled?')
st.write('Order filled status:', order_filled)

# --- Connect to Snowflake ---
cnx = st.connection("snowflake")
session = cnx.session()

# --- Pull fruit data ---
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# --- Convert Snowflake → Pandas ---
pd_df = my_dataframe.to_pandas()

# --- User fruit selection ---
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# --- If fruits are selected ---
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '

        # Lookup SEARCH_ON for the fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Display nutrition info
        st.subheader(f'{fruit_chosen} Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")

        if smoothiefroot_response.status_code == 200:
            data = smoothiefroot_response.json()
            if "error" in data:
                st.warning(f"Sorry, {fruit_chosen} is not in our database.")
            else:
                st.dataframe(data=data, use_container_width=True)
        else:
            st.error(f"Could not fetch data for {fruit_chosen} (status: {smoothiefroot_response.status_code})")

    # Clean trailing comma
    ingredients_string = ingredients_string.rstrip(', ')

    # --- Prepare SQL INSERT statement ---
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED)
        VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()})
    """

    st.write('SQL Preview:', my_insert_stmt)

    # --- Submit order button ---
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Smoothie order for {name_on_order} has been placed!")
