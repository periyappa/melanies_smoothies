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

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        # ✅ Display nutrition info only if response is valid JSON
        st.subheader(f"{fruit_chosen} Nutrition Information")
        response = requests.get("https://my.smoothiefroot.com/api/nutrition/" + fruit_chosen)
        if response.status_code == 200:
            try:
                sf_df = st.dataframe(data=response.json(), use_container_width=True)
            except Exception:
                st.warning(f"⚠️ {fruit_chosen} returned invalid JSON.")
        else:
            st.warning(f"⚠️ {fruit_chosen} is not in the Smoothiefroot database.")

    combined_value = ingredients_string.strip(", ") + " (" + name_on_order + ")"

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients)
        VALUES ('{combined_value}')
    """

    st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
    st.write(my_insert_stmt)
    st.stop()

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
