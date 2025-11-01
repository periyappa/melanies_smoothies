#Import python packages
import pandas as pd
import streamlit as st
import requests
from snowflake.snowpark.functions import col

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

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

order_filled = st.checkbox('Mark order as filled')

if ingredients_list:
    
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    # Remove trailing comma and space
    ingredients_string = ingredients_string.rstrip(', ')

    # ✅ FIXED INSERT STATEMENT
    my_insert_stmt = f"""
       INSERT INTO smoothies.public.orders(NAME_ON_ORDER, INGREDIENTS, ORDER_FILLED, ORDER_TS)
       VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()}, CURRENT_TIMESTAMP)
    """

    st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

    # ✅ Move this block ABOVE st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    st.write(my_insert_stmt)

    # ⛔️ This must come AFTER the button logic
    st.stop()
