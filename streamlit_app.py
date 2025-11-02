# Import python packages
import streamlit as st
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

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# ✅ Updated section per challenge task
# Select both FRUIT_NAME and SEARCH_ON columns
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'),
    col('SEARCH_ON')
)

# Display the dataframe temporarily for debugging (optional)
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()  # ✅ Added so we can focus on this part for now

# Multiselect dropdown shows FRUIT_NAMEs
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        # ✅ Use SEARCH_ON column for API call instead of FRUIT_NAME
        search_value = my_dataframe.filter(col('FRUIT_NAME') == fruit_chosen).collect()[0]['SEARCH_ON']

        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_value)

        # ✅ Handle missing fruits gracefully
        if smoothiefroot_response.status_code == 200:
            data = smoothiefroot_response.json()
            if "error" in data:
                st.warning(f"Sorry, {fruit_chosen} is not in our database.")
            else:
                st.dataframe(data=data, use_container_width=True)
        else:
            st.error(f"Could not fetch data for {fruit_chosen} (status: {smoothiefroot_response.status_code})")

    combined_value = ingredients_string.strip(", ") + " (" + name_on_order + ")"

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients)
        VALUES ('{combined_value}')
    """

    # ✅ Display confirmation message
    st.success(f"✅ Your Smoothie is ready to order, {name_on_order}!")
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
