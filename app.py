import streamlit as st
import snowflake
import snowflake.connector
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt

st.title('Citibike Dashboard')

conn = snowflake.connector.connect(**st.secrets["snowflake"])
data = pd.read_sql("select * from trips limit 10000;", conn)
data.rename(columns={'START_STATION_LATITUDE':'lat', 'START_STATION_LONGITUDE':'lon'}, inplace=True)
data['old_date'] = data['STARTTIME'].astype(str)
#convert to pandas timestamp
data["old_date"] = pd.to_datetime(data.old_date)

#split columns
data["new_date"] = data["old_date"].dt.date
data["new_time"] = data["old_date"].dt.time
# data["date"] = data['STARTTIME'].date
# data["time"] = data['STARTTIME'].time
if st.button('Get List'):
        st.write(data)

chart_data = pd.DataFrame(data['GENDER'].value_counts())
if st.button('By Gender'):
    st.bar_chart(chart_data)
 
midpoint = (np.average(data['lat']), np.average(data['lon']))
df = pd.DataFrame(data, columns=['lat','lon'])

# st.subheader('Hourly Statistics')
hour = st.slider("Hour to look at", 0, 23)
data = data[data['new_time'].dt.hour == hour]

st.markdown("Bike rides between %i:00 and %i:00" %(hour, (hour +1)))
filtered = data[data['new_time'].dt.hour >= hour & (data['new_time'].dt.hour < (hour + 1))]
st.subheader("Popular Pick Up Locations")

st.write(pdk.Deck(
           map_style="mapbox://styles/mapbox/light-v9",
           initial_view_state= {
                        "latitude":midpoint[0],
                        "longitude": midpoint[1],
                       "zoom":11,
                        "pitch":50,
           },
           layers = [
                      pdk.Layer(
                                 "HexagonLayer",
                                data=data,
                                 get_position=["lon", "lat"],
                                 radius=100,
                                 extruded=True,
                                 pickable = True,
                                 elevation_scale=4,
                                 elevation_range=[1,1000],
                      ),
           ],
))




#     data.dropna(subset = ["LATITUDE", "LONGITUDE"], inplace=True)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis = 'columns', inplace=True)
#     data.rename(columns={'crash date_crash time': 'date/time'}, inplace=True)
#     return data
# df = pd.read_sql(f'select date_trunc("hour", starttime) as "date", count(*) as"num_trips", avg(tripduration)/60 as "avg duration (mins)", avg(haversine(start_station_latitude, start_station_longitude, end_station_latitude,end_station_longitude)) as "avg distance (km)" from trips group by 1 order by 1;', conn)


# st.header("Where are the most people injured in NYC?")
# injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 14)
# st.map(data.query("number of injured persons>= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

# st.header("How many collisions occur during a given time of day?")
# hour = st.slider("Hour to look at", 0, 23)
# data = data[data['date/time'].dt.hour == hour]


# st.markdown("Vehicle collisions between %i:00 and %i:00" %(hour, (hour +1)))

# midpoint = (np.average(data['latitude']), np.average(data['longitude']))
# st.write(pdk.Deck(
#            map_style="mapbox://styles/mapbox/light-v9",
#            initial_view_state={
#                       "latitude": midpoint[0],
#                       "longitude": midpoint[1],
#                       "zoom": 11,
#                       "pitch": 50,
#            },
#            layers = [
#                       pdk.Layer(
#                                  "HexagonLayer",
#                                  data=data[['date/time', 'latitude', 'longitude']],
#                                  get_position=['latitude', 'longitude'],
#                                  radius=100,
#                                  extruded=True,
#                                  pickable = True,
#                                  elevation_scale=4,
#                                  elevation_range=[1,1000],
#                       ),
#            ],
# ))

# st.subheader("Breakdown by minute between %i:00 and %i:00" %(hour, (hour +1) %24))
# filtered = data[
#     (data['date/time'].dt.hour >= hour) & data['date/time'].dt.hour < (hour + 1)
# ]
# hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
# chart_data = pd. DataFrame({'minute': range(60), 'crashes': hist})
# fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height = 400)
# st.write(fig)


# st.header("Top 5 Dangerous Collision Streets by Type")
# select = st.selectbox('Affected Type:', ['Pedestrians', 'Cyclists', 'Motorists'])

# if select == 'Pedestrians':
#            st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
