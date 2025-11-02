# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

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

# Text input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the snowpark dataframe
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

# Multiselect box for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)
order_filled = st.checkbox("Mark order as FILLED")

# If user selects ingredients
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        # Fetch smoothie fruit data for each chosen fruit
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    combined_value = ingredients_string.strip()

    # SQL insert statement
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders(name_on_order, ingredients)
    VALUES ('{name_on_order}', '{ingredients_string.strip()}', {str(order_filled).upper()})
    """


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
