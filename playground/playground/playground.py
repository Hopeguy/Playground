"""Main module."""
import json
from google.transit import gtfs_realtime_pb2
import pandas as pd
import streamlit as st
import requests
import datetime
# Color gradient for color of box
def get_color(value):
    # Map the value to a color gradient from red to yellow to green
    if value <= 3:
        red = 255
        green = 0
        blue = 0
    elif value <= 5:
        red = 255
        green = 255
        blue = 0
    else:
        red = 0
        green = 255
        blue = 0
    return f'rgb({red},{green},{blue})'

st.set_page_config(
    page_title="Real-Time Dashboard",
    page_icon="✅",
)
df = pd.read_csv("playground\playground\Static_SL_df.csv")

#"Gets the station of interest "
stop_id = df[(df["stop_name"] == "Tekniska högskolan")]
subway_stop_id= ["9022001002221001", "9022001002221002"] #Spår 2 är söderut (in mot stan). Spår 1 är norrut (ut till mörby)
#gets real time data
feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://opendata.samtrafiken.se/gtfs-rt/sl/TripUpdates.pb?key=73f1656eaba44dddad530693523cd44a')
now = datetime.datetime.now()
feed.ParseFromString(response.content)

subway =  {} 
subway["Arrival_time_train_to_Mörby_Centrum"] = []
subway["Arrival_time_train_to_T-centralen"] = []
# Iterate over the feed entities and search for the desired stop_id
for entity in feed.entity:
    if entity.HasField('trip_update'):
        for stop_time_update in entity.trip_update.stop_time_update:
            if stop_time_update.stop_id in subway_stop_id:
                # Perform actions on the entity with the desired stop_id
                #print("Found stop_id:", stop_time_update.stop_id)
                arrival_time_minutes = str(int((datetime.datetime.fromtimestamp(stop_time_update.arrival.time) - now).total_seconds() // 60))
                if stop_time_update.stop_id == subway_stop_id[0]:
                #departure_time = datetime.datetime.fromtimestamp(stop_time_update.departure.time).strftime('%H:%M:%S')
                    subway["Arrival_time_train_to_Mörby_Centrum"].append([arrival_time_minutes])
                if  stop_time_update.stop_id == subway_stop_id[1]:
                #departure_time = datetime.datetime.fromtimestamp(stop_time_update.departure.time).strftime('%H:%M:%S')
                    subway["Arrival_time_train_to_T-centralen"].append([arrival_time_minutes])
                #print("Departure Time:", departure_time)


# STUFF FOR STREAMLIT

st.title("Tekniska Högskolan Avgångar")
st.write(f'call made at: {now.strftime("%H:%M")}')

ride_to_morby = subway["Arrival_time_train_to_Mörby_Centrum"]
ride_to_T_centralen = subway["Arrival_time_train_to_T-centralen"]
# Calculate the corresponding colors for the boxes



data = {'Next train to Mörby Centrum': ride_to_morby,
        'Next train to T-centralen': ride_to_T_centralen}
df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in data.items()]))

df = df.applymap(lambda x: int(x[0]) if isinstance(x, list) else x)

next_ride_morby = df["Next train to Mörby Centrum"].loc[df['Next train to Mörby Centrum'] > 0].head(1).values
next_ride_tcentral = df["Next train to T-centralen"].loc[df['Next train to T-centralen'] > 0].head(1).values
# Create the boxes using the selected colors


        




# Display the boxes above the respective columns
#st.markdown(f'<div style="display: flex; justify-content: space-between;">{box_html1}{box_html2}</div>', unsafe_allow_html=True)

morby_series = df["Next train to Mörby Centrum"]
tcentralen_series = df["Next train to T-centralen"]

# Create the two columns
col1, col2 = st.columns(2)

# Create the first box using st.markdown in the first column
with col1:
    color1 = get_color(next_ride_morby)

    st.markdown(f'<div style="background-color: {color1}; height: 100px; width: 100%; color: black">' \
        f'<p style="font-size: 24px; line-height: 1.2; font-weight: bold; text-align: center">' \
        f'Mörby Centrum<br/>{next_ride_morby[0]} Minutes</p></div>', unsafe_allow_html=True)

    st.dataframe(morby_series.to_frame(), use_container_width=True)

# Create the second box using st.markdown in the second column
with col2:
    color2 = get_color(next_ride_tcentral)
    st.markdown(f'<div style="background-color: {color2}; height: 100px; width: 100%; color: black">' \
        f'<p style="font-size: 24px; line-height: 1.2; font-weight: bold; text-align: center">' \
        f'T-centralen<br/>{int(next_ride_tcentral[0])} Minutes</p></div>', unsafe_allow_html=True)

    st.dataframe(tcentralen_series.to_frame(), use_container_width=True)