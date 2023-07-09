"""Main module."""
import streamlit as st
import FetchFunctions
import time


def main():
        # read in static data to use to find the stop id for interesting station (manually)
        # df = pd.read_csv("playground\playground\Static_SL_df.csv")
        # df_aspudden = df[df["stop_name"] == "Aspudden"]
        # stop_id = df[(df["stop_name"] == "Tekniska högskolan")]


        subway_stop_id_dict_tekniska = {"Tekniska-tcentralen": "9022001002221001", "Tekniska-Mörby": "9022001002221002"} # Spår 2 är söderut (in mot stan). Spår 1 är norrut (ut till mörby)
        subway_stop_id_dict_aspudden = {"Aspudden-tcentralen": "9022001002611001", "Aspudden-Norsborg": "9022001002611002"} # Spår 1 går norrut (in mot stan). Spår 2 går söderut (ut mot Norborg)

        st.set_page_config(page_title="Real-Time Dashboard",
                           layout="wide")
        st.title("Real Time")

        placeholder = st.empty()

        
        with placeholder.container():
            


            if st.button("Refresh"):
                st.write(f'Last API call made at: {FetchFunctions.get_time().strftime("%H:%M")}') # Writes out last time the site was updated

                feed = FetchFunctions.fetch_data("https://opendata.samtrafiken.se/gtfs-rt/sl/TripUpdates.pb?key=73f1656eaba44dddad530693523cd44a")

                # Creates a list for the next arrival times for each stop id
                ride_to_morby = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_tekniska["Tekniska-Mörby"])
                ride_to_T_centralen = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_tekniska["Tekniska-tcentralen"])
                ride_to_T_centralen_aspudden = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_aspudden["Aspudden-tcentralen"])
                ride_to_norsborg = FetchFunctions.get_trip_data(feed, subway_stop_id_dict_aspudden["Aspudden-Norsborg"])

                #gets the temperature in stockholm and shows that with streamlit
                st.metric(value=str(FetchFunctions.get_stockholm_temperature())+" °C", label="Temperature Stockholm")

                st.header("Tekniska Högskolan Avgångar")

                # Divide the site into two columns, one for each train direction (north/south)
                col1, col2 = st.columns(2)

                # Crates the table and block with color of arrival times in streamlit.
                with col1: # for mörby
                    FetchFunctions.create_timetable(ride_to_morby, "Mörby Centrum")

                # Create the second box using st.markdown in the second column
                with col2: # for tcentralen

                    FetchFunctions.create_timetable(ride_to_T_centralen, "T-centralen")

                    
                st.header("Aspudden Avgångar")
                
                col3, col4 = st.columns(2)

                                # Create the first box using st.markdown in the first column
                with col3: # for norsborg

                    FetchFunctions.create_timetable(ride_to_norsborg, "Norsborg")

                # Create the second box using st.markdown in the second column
                with col4: # for tcentralen
                    FetchFunctions.create_timetable(ride_to_T_centralen_aspudden, "T-centralen")

                
          
if __name__ == "__main__":
    main()