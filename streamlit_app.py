import pandas as pd
import streamlit as st
import folium
from streamlit.components.v1 import html

# Load the summary DataFrame
summary_df = pd.read_csv('dataframe.csv')

# Title of the app
st.set_page_config(
    page_title="Station Variable Availability",
    layout="wide",  # Use the "wide" layout which uses more screen space
)

# Create a selection box for stations
stations = summary_df['Code_and_Name'].unique()
selected_stations = st.multiselect('Select Stations', stations)

# Create two columns for layout (left for variable availability, right for the map)
col1, col2 = st.columns(2)  # Make both columns equal width

# If the user has selected any stations, display the variable availability and the map
if selected_stations:
    with col1:  # Left column for text (variable availability)
        for station in selected_stations:
            station_data = summary_df[summary_df['Code_and_Name'] == station]
            station_name = station_data['Name'].values[0]
            altitude = station_data['Altitude'].values[0]

            st.subheader(f"Station: {station_name}")
            st.write(f"**Altitude:** {altitude} m")

            # Iterate through the variables and display availability
            for var in summary_df.columns:
                if var.endswith('_Available'):  # Only check availability columns
                    availability = station_data[var].values[0]
                    start_date = station_data[f'{var.split("_")[0]}_Start_Date'].values[0]
                    end_date = station_data[f'{var.split("_")[0]}_End_Date'].values[0]
                    continuity = station_data[f'{var.split("_")[0]}_Continuous'].values[0]

                    if availability:
                        if continuity:
                            st.write(f"**{var[:-9]}** - Available from {start_date} to {end_date}")
                            st.write(f"continuity: data is :green[continuous].")
                        else:
                            st.write(f"**{var[:-9]}** - Available from {start_date} to {end_date}")
                            st.write(f"Continuity: data has gaps.")
                    else:
                        st.write(f"**{var[:-9]}** - Not Available")

    with col2:  # Right column for the map
        # Create a map centered around the average lat/lon of all stations (initial view)
        map_center = [summary_df['Latitude'].mean(), summary_df['Longitude'].mean()]
        mymap = folium.Map(location=map_center, zoom_start=6)

        # Add markers for each selected station
        for station in selected_stations:
            station_data = summary_df[summary_df['Code_and_Name'] == station]
            station_name = station_data['Name'].values[0]
            lat = station_data['Latitude'].values[0]
            lon = station_data['Longitude'].values[0]
            altitude = station_data['Altitude'].values[0]

            # Add a marker to the map for the station
            station_info = f"Name: {station_name}<br>Altitude: {altitude} m"
            folium.Marker([lat, lon], popup=station_info).add_to(mymap)

        # Save the folium map to an HTML file and render it using Streamlit
        map_html = mymap._repr_html_()  # This converts the folium map to HTML
        html(map_html, width=700, height=500)  # Display the HTML map in Streamlit

        # Display the variable descriptions below the map (in markdown format)
        st.markdown("""
        **RR** : quantité de précipitation tombée en 24 heures (de 06h FU le jour J à 06h FU le jour J+1). La valeur relevée à J+1 est affectée au jour J (en mm et 1/10).

        **TN** : température minimale sous abri (en °C et 1/10).

        **HTN** : heure de TN (hhmm).

        **TX** : température maximale sous abri (en °C et 1/10).

        **HTX** : heure de TX (hhmm).

        **TM** : moyenne quotidienne des températures horaires sous abri (en °C et 1/10).
    
        **TNTXM** : moyenne quotidienne (TN+TX)/2 (en °C et 1/10).

        **TAMPLI** : amplitude thermique quotidienne : écart entre TX et TN quotidiens (TX-TN) (en °C et 1/10).

        **TNSOL** : température quotidienne minimale à 10 cm au-dessus du sol (en °C et 1/10).

        **TN50** : température quotidienne minimale à 50 cm au-dessus du sol (en °C et 1/10).

        **DG** : durée de gel sous abri (T ≤ 0°C) (en mn).

        **FFM** : moyenne quotidienne de la force du vent moyenné sur 10 mn, à 10 m (en m/s et 1/10).

        **FF2M** : moyenne quotidienne de la force du vent moyenné sur 10 mn, à 2 m (en m/s et 1/10).

        **FXY** : maximum quotidien de la force maximale horaire du vent moyenné sur 10 mn, à 10 m (en m/s et 1/10).

        **DXY** : direction de FXY (en rose de 360).

        **HXY** : heure de FXY (hhmm).

        **FXI** : maximum quotidien de la force maximale horaire du vent instantané, à 10 m (en m/s et 1/10).

        **DXI** : direction de FXI (en rose de 360).

        **HXI** : heure de FXI (hhmm).

        **FXI2** : maximum quotidien de la force maximale horaire du vent instantané, à 2 m (en m/s et 1/10).

        **DXI2** : direction de FXI2 (en rose de 360).

        **HXI2** : heure de FXI2 (hhmm).

        **FXI3S** : maximum quotidien de la force maximale horaire du vent moyenné sur 3 s, à 10 m (en m/s et 1/10).

        **DXI3S** : direction de FXI3S (en rose de 360).

        **HXI3S** : heure de FXI3S (hhmm).

        **DRR** : durée des précipitations (en mn).
        """)
else:
    st.write("Select one or more stations to view available variables.")
