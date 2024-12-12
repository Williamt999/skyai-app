import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static, st_folium
import folium

import streamlit as st
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# CSS Styling
css = '''
.stApp {
    background: linear-gradient(135deg, hsl(292, 30%, 35%), hsl(292, 30%, 65%));
    color: white;
}

.stApp > header {
    background-color: transparent;
}

# .stApp h1, h2 {
#     text-align: center;
#     color: white;
# }

# div.stButton > button:first-child {
#     border: 1px solid darkgreen;
#     border-radius: 6px;
#     background-color: green;
#     color: white;
}
'''

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


### Demand Forecasting for City - part 1 ###

df_city_names = pd.read_csv('./data/output_passengers.csv')
unique_metropolitan_areas_df = pd.DataFrame(df_city_names['metropolitan_area'].unique(), columns=['metropolitan_area'])

st.header(":airplane: Passenger flow Predictor in Brazil :airplane:")
st.text("Please select your Brazilian city of interest from the dropdown")
user_input_city = st.selectbox('Select a Brazilian city of interest', df_city_names['city_name'])
st.text(f'You selected the city: {user_input_city}')

params = {
    'city_name': user_input_city,
}

response = requests.get('https://skyai-wagon-108938723002.us-central1.run.app/demand_forecast', params=params)
if response.status_code == 200:
    data = response.json()
    outcome = data
    st.text(f"The predicted passenger flow (inbound and outbound combined) for this city is {outcome}")
else:
    st.text(f"Request failed with status code {response.status_code}")

# Streamlit title
st.title("New airport demand heatmap")

# Load the shapefiles
no_airport_gdf_2 = gpd.read_file('./data/shapefiles/no_airport_gdf_2.shp')  # Update with the correct path
gdf = gpd.read_file('./data/shapefiles/max_flow_per_ma.shp')  # Update with the correct path

# Split the GeoDataFrame into regions with and without airports
no_airport_gdf_2 = no_airport_gdf_2.copy()
has_airport_gdf = gdf[gdf['total_airp'] > 0]

# Create a Folium map centered on Brazil
brazil_map = leafmap.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Define a color map for the categorical labels
color_mapping = {
    '0 - 1,000': '#f7fcf0',
    '1,001 - 10,000': '#ccebc5',
    '10,001 - 25,000': '#a1d99b',
    '25,001 - 50,000': '#74c476',
    '50,001 - 100,000': '#41ab5d',
    '100,001 - 200,000': '#238b45',
    '200,001 - 300,000': '#005a32',
    '>300,000': '#00240d'
}

# Add regions with no airports, color-coded by estimated passenger range
folium.GeoJson(
    no_airport_gdf_2,
    name='No Airports',
    style_function=lambda feature: {
        'fillColor': color_mapping.get(
            feature['properties']['est_pass_r'], 'grey'
        ),  # Default to grey if no match
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(fields=['NM_RGI', 'metropolit', 'est_pass_r', 'pred_final'],
                                  aliases=['Region Name', 'Area Code', 'Passenger Range', 'Estimated Demand'])
).add_to(brazil_map)

# Metropolitan areas with airports colored grey
folium.GeoJson(
    has_airport_gdf,
    name='With Airports',
    style_function=lambda x: {
        'fillColor': 'grey',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.9
    }
).add_to(brazil_map)

legend_html="""
<head>
    <style>
        .color-bar-container {
            display: flex;
            align-items: center;
            width: 100%;
            margin-bottom: 5px;
        }
        .color-bar {
            height: 30px;
            flex-grow: 1;
        }
        .color-bar-labels {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            margin-top: 3px;
        }
    </style>
</head>
<body>
    <div class="color-bar-container">
        <div class="color-bar" style="background: grey; flex: 1;"></div>
        <div class="color-bar" style="background: #f7fcf0; flex: 1;"></div>
        <div class="color-bar" style="background: #ccebc5; flex: 1;"></div>
        <div class="color-bar" style="background: #a1d99b; flex: 1;"></div>
        <div class="color-bar" style="background: #74c476; flex: 1;"></div>
        <div class="color-bar" style="background: #41ab5d; flex: 1;"></div>
        <div class="color-bar" style="background: #238b45; flex: 1;"></div>
        <div class="color-bar" style="background: #005a32; flex: 1;"></div>
        <div class="color-bar" style="background: #00240d; flex: 1;"></div>
    </div>
    <div class="color-bar-labels">
        <span>Existing Airports</span>
        <span>0</span>
        <span>1,000 </span>
        <span>10,000</span>
        <span>25,000</span>
        <span>50,000</span>
        <span>100,000</span>
        <span>200,000</span>
        <span>>300,000</span>

    </div>
</body>

"""
st.html(legend_html)
# Define the legend
legend_dict = {
    '0 - 1,000': '#f7fcf0',
    '1,001 - 10,000': '#ccebc5',
    '10,001 - 25,000': '#a1d99b',
    '25,001 - 50,000': '#74c476',
    '50,001 - 100,000': '#41ab5d',
    '100,001 - 200,000': '#238b45',
    '200,001 - 300,000': '#005a32',
    '>300,000': '#00240d',
    'Existing Airports': 'grey'
}

# Add the legend
# Add a layer control to toggle visibility
folium.LayerControl().add_to(brazil_map)

# Create a legend using HTML
# Import necessary functions from branca library
from branca.element import Template, MacroElement

# Add the legend to the map
#brazil_map.get_root().html.add_child(folium.Element(legend_html))

# Add the legend to the map
#macro = MacroElement()
#macro._template = Template(legend_html)
#brazil_map.get_root().add_child(macro)

# Display the map in Streamlit
folium_static(brazil_map, width=725)
#brazil_map
