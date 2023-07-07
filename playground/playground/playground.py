"""Main module."""
import pandas as pd
import streamlit as st
import FetchFunctions
import time

def main():
        # read in static data to use to find the stop id for interesting station (manually)
        # df = pd.read_csv("playground\playground\Static_SL_df.csv")

        # df_aspudden = df[df["stop_name"] == "Aspudden"]
        # stop_id = df[(df["stop_name"] == "Tekniska högskolan")]

        subway_stop_id_dict_tekniska = {"Tekniska-tcentralen": "9022001002221001", "Tekniska-Mörby": "9022001002221002"}

        # subway_stop_id_Tekniska = ["9022001002221001", "9022001002221002"]  # Spår 2 är söderut (in mot stan). Spår 1 är norrut (ut till mörby)
        # subway_stop_id_Aspudden = ["9022001002611001", "9022001002611002"]  # Spår 1 går norrut (in mot stan). Spår 2 går söderut (ut mot Norborg)

        # Streamlit stuff below:

        st.set_page_config(page_title="Real-Time Dashboard")
        st.title("Tekniska Högskolan Avgångar")

        placeholder = st.empty()

        while True:

            with placeholder.container():
                
                st.write(f'Last API call made at: {FetchFunctions.get_time().strftime("%H:%M")}')
                feed = FetchFunctions.fetch_data("https://opendata.samtrafiken.se/gtfs-rt/sl/TripUpdates.pb?key=73f1656eaba44dddad530693523cd44a")


                # STUFF FOR STREAMLIT
                # Writeing out time when last update whas made

                ride_to_morby = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_tekniska["Tekniska-Mörby"])

                ride_to_T_centralen = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_tekniska["Tekniska-tcentralen"])

                st.metric(value=str(FetchFunctions.get_stockholm_temperature())+" °C", label="Temperature Stockholm")


                # Create the two columns
                col1, col2 = st.columns(2)

                # Create the first box using st.markdown in the first column
                with col1: # for mörby
                    color1 = FetchFunctions.get_color(FetchFunctions.get_next_ride(ride_to_morby))

                    st.markdown(f'<div style="background-color: {color1}; height: 100px; width: 100%; color: black">'
                                f'<p style="font-size: 24px; line-height: 1.2; font-weight: bold; text-align: center">'
                                f'Mörby Centrum<br/>{FetchFunctions.get_next_ride(ride_to_morby)} Minutes</p></div>',
                                unsafe_allow_html=True)

                    st.dataframe(pd.DataFrame(ride_to_morby), use_container_width=True)

                # Create the second box using st.markdown in the second column
                with col2: # for tcentralen
                    color2 = FetchFunctions.get_color(FetchFunctions.get_next_ride(ride_to_T_centralen))
                    st.markdown(f'<div style="background-color: {color2}; height: 100px; width: 100%; color: black">'
                                f'<p style="font-size: 24px; line-height: 1.2; font-weight: bold; text-align: center">'
                                f'T-centralen<br/>{int(FetchFunctions.get_next_ride(ride_to_T_centralen))} Minutes</p></div>',
                                unsafe_allow_html=True)

                    st.dataframe(pd.DataFrame(ride_to_T_centralen),
                                    use_container_width=True)

                time.sleep(200)
        
    

if __name__ == "__main__":
    main()