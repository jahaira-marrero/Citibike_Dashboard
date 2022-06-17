import streamlit as st
import snowflake
import snowflake.connector
import pandas as pd

st.title('Citibike Dashboard')

# def get_citi_list():
#     with my_cnx.cursor() as my_cur:
#         my_cur.execute("select * from trips limit 20")
#         return my_cur.fetchall()

conn = snowflake.connector.connect(**st.secrets["snowflake"])

if st.button('Get List'):
        data = pd.read_sql("select * from trips limit 100;", conn)
        st.write(data)

