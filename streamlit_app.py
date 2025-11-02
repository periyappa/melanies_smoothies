# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Title and intro text
st.title("🥤 Customize Your Smoothie!")
st.write("""
Welcome to the Smoothie Customizer app.  
Choose your fruits, see their nutrition info, and place your order below!
""")

# Get the user's name for the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Pull data from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Display for debugging (optional)
# st.dataframe(pd_df)

# Let the user choose fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# If fruits are selected
if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '

        # Lookup SEARCH_ON value from Pandas DataFrame
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Display nutrition info from API
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

    # Trim last comma and space
    ingredients_string = ingredients_string.rstrip(', ')

    # ✅ Insert both NAME_ON_ORDER and INGREDIENTS into the orders table
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (NAME_ON_ORDER, INGREDIENTS)
        VALUES ('{name_on_order}', '{ingredients_string}')
    """

    # Display confirmation
    st.success(f"✅ Your Smoothie is ready to order, {name_on_order}!")
    st.write(my_insert_stmt)

    # Submit order button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie has been ordered!', icon="✅")
