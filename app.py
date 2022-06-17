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

st.subheader('Hourly Statistics')
df = pd.read_sql(f'select date_trunc("hour", starttime) as "date", count(*) as"num_trips", avg(tripduration)/60 as "avg duration (mins)", avg(haversine(start_station_latitude, start_station_longitude, end_station_latitude,end_station_longitude)) as "avg distance (km)" from trips group by 1 order by 1;', conn)
df['date'] = pd.to_datetime(df['date'])

st.write(df)