import streamlit as st
import snowflake
import snowflake.connector
import pandas as pd

st.title('Citibike Dashboard')

def get_citi_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from trips where starttime='2018-06-21 08:06:24.076'")
        return my_cur.fetchall()

if st.button('Get List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_citi_list()
    my_cnx.close()
    st.dataframe(my_data_rows)
