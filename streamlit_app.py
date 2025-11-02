# Import python packages
import streamlit as st
import pandas as pd  # ✅ Added pandas as requested
from snowflake.snowpark.functions import col
import requests  # Required for API calls

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_list = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Prepare order string
ingredients_string = ", ".join(ingredients_list)
combined_value = ingredients_string + " (" + name_on_order + ")"

# Build the insert statement
my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(ingredients)
    VALUES ('{combined_value}')
"""

# ✅ Always show the Submit Order button
time_to_insert = st.button('Submit Order')

# Handle order submission
if time_to_insert:
    if ingredients_list:
        session.sql(my_insert_stmt).collect()
        st.success('✅ Your Smoothie is ordered!', icon="✅")
    else:
        st.warning("⚠️ Please select at least one fruit before submitting.")

# ✅ Display fruit nutrition info when selected
if ingredients_list:
    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)

        if smoothiefroot_response.status_code == 200:
            data = smoothiefroot_response.json()
            if "error" in data:
                st.warning(f"Sorry, {fruit_chosen} is not in our database.")
            else:
                # Convert API response to DataFrame for cleaner display
                st.dataframe(pd.DataFrame([data]), use_container_width=True)
        else:
            st.error(f"Could not fetch data for {fruit_chosen} (status: {smoothiefroot_response.status_code})")
