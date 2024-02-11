import folium
from folium import *
import webbrowser
from folium.plugins import *
import json
import random
import pandas as pd
import pycountry

night_layer = folium.TileLayer(
    tiles='https://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}',
    attr='Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
    bounds=[[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
    min_zoom=1,
    max_zoom=8,
    format='jpg',
    time='',
    tilematrixset='GoogleMapsCompatible_Level'
)

tile_layer = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
    min_zoom=3,
)

m = folium.Map(location=[-23, -46],
               zoom_start=3, no_wrap=True,world_copy_jump=True
               )


button_html = """
<div style="position: fixed; top: 10px; left: 10px; z-index: 1000;">
    <button onclick="alert('Button clicked!');" style="padding: 10px 20px; background-color: white; border: none;">Button</button>
</div>
"""

locate_control = LocateControl()
locate_control.add_to(m)

mouse_position = MousePosition()
mouse_position.add_to(m)

'''
# Generate random heatmap data
heatmap_data = []
for _ in range(5000):
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    intensity = random.uniform(0, 1)
    heatmap_data.append([lat, lon, intensity])

# Create HeatMap layer and add it to the map
heatmap = HeatMap(heatmap_data, radius=20, max_zoom=8)
heatmap.add_to(m)
'''

with open('datasets/world-countries.json') as handle:
    country_geo = json.loads(handle.read())

country_layer = folium.FeatureGroup(name='Countries')
country_layer.add_to(m)

year = 2019

# Load the CSV file into a DataFrame
df = pd.read_csv('Backend/CSV/owid-energy-data.csv')
iso_code_dict = {}
for index, row in df.iterrows():
    iso_code = row['iso_code']
    if row['year'] == year and iso_code not in iso_code_dict:
        iso_code_dict[iso_code] = row

columns = [
    'country', 'year', 'iso_code', 'population', 'gdp', 'biofuel_cons_change_pct', 'biofuel_cons_change_twh',
    'biofuel_cons_per_capita', 'biofuel_consumption', 'biofuel_elec_per_capita', 'biofuel_electricity',
    'biofuel_share_elec', 'biofuel_share_energy', 'carbon_intensity_elec', 'coal_cons_change_pct',
    'coal_cons_change_twh', 'coal_cons_per_capita', 'coal_consumption', 'coal_elec_per_capita',
    'coal_electricity', 'coal_prod_change_pct', 'coal_prod_change_twh', 'coal_prod_per_capita',
    'coal_production', 'coal_share_elec', 'coal_share_energy', 'electricity_demand', 'electricity_generation',
    'electricity_share_energy', 'energy_cons_change_pct', 'energy_cons_change_twh', 'energy_per_capita',
    'energy_per_gdp', 'fossil_cons_change_pct', 'fossil_cons_change_twh', 'fossil_elec_per_capita',
    'fossil_electricity', 'fossil_energy_per_capita', 'fossil_fuel_consumption', 'fossil_share_elec',
    'fossil_share_energy', 'gas_cons_change_pct', 'gas_cons_change_twh', 'gas_consumption',
    'gas_elec_per_capita', 'gas_electricity', 'gas_energy_per_capita', 'gas_prod_change_pct',
    'gas_prod_change_twh', 'gas_prod_per_capita', 'gas_production', 'gas_share_elec', 'gas_share_energy',
    'greenhouse_gas_emissions', 'hydro_cons_change_pct', 'hydro_cons_change_twh', 'hydro_consumption',
    'hydro_elec_per_capita', 'hydro_electricity', 'hydro_energy_per_capita', 'hydro_share_elec',
    'hydro_share_energy', 'low_carbon_cons_change_pct', 'low_carbon_cons_change_twh', 'low_carbon_consumption',
    'low_carbon_elec_per_capita', 'low_carbon_electricity', 'low_carbon_energy_per_capita',
    'low_carbon_share_elec', 'low_carbon_share_energy', 'net_elec_imports', 'net_elec_imports_share_demand',
    'nuclear_cons_change_pct', 'nuclear_cons_change_twh', 'nuclear_consumption', 'nuclear_elec_per_capita',
    'nuclear_electricity', 'nuclear_energy_per_capita', 'nuclear_share_elec', 'nuclear_share_energy',
    'oil_cons_change_pct', 'oil_cons_change_twh', 'oil_consumption', 'oil_elec_per_capita', 'oil_electricity',
    'oil_energy_per_capita', 'oil_prod_change_pct', 'oil_prod_change_twh', 'oil_prod_per_capita',
    'oil_production', 'oil_share_elec', 'oil_share_energy', 'other_renewable_consumption',
    'other_renewable_electricity', 'other_renewable_exc_biofuel_electricity', 'other_renewables_cons_change_pct',
    'other_renewables_cons_change_twh', 'other_renewables_elec_per_capita',
    'other_renewables_elec_per_capita_exc_biofuel', 'other_renewables_energy_per_capita',
    'other_renewables_share_elec', 'other_renewables_share_elec_exc_biofuel', 'other_renewables_share_energy',
    'per_capita_electricity', 'primary_energy_consumption', 'renewables_cons_change_pct',
    'renewables_cons_change_twh', 'renewables_consumption', 'renewables_elec_per_capita', 'renewables_electricity',
    'renewables_energy_per_capita', 'renewables_share_elec', 'renewables_share_energy', 'solar_cons_change_pct',
    'solar_cons_change_twh', 'solar_consumption', 'solar_elec_per_capita', 'solar_electricity',
    'solar_energy_per_capita', 'solar_share_elec', 'solar_share_energy', 'wind_cons_change_pct',
    'wind_cons_change_twh', 'wind_consumption', 'wind_elec_per_capita', 'wind_electricity',
    'wind_energy_per_capita', 'wind_share_elec', 'wind_share_energy'
]

for feature in country_geo['features']:
    iso_code = feature['id']
    
    tooltip = ''
    if iso_code in iso_code_dict:
        data = iso_code_dict[iso_code]
        for column in columns:
            if column in data and not pd.isna(data[column]):
                #feature['properties'][column] = data[column]
                tooltip += f"{column}: {data[column]}"
                if (columns.index(column) + 1) % 3 == 0:
                    tooltip += "<br>"
                else:
                    tooltip += ", "
    folium.GeoJson(
        feature,
        #name=pycountry.countries.get(alpha_3=iso_code).name,
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.25,
        },
        tooltip=tooltip
    ).add_to(country_layer)

search_control = Search(
    layer=country_layer,
    geom_type='Polygon',
    placeholder='Search for a country',
    collapsed=False,
    search_label='name',
    search_zoom=6,
    position='topright'
)
search_control.add_to(m)

w0 = WmsTileLayer(
    "http://this.wms.server/ncWMS/wms",
    name="Test WMS Data",
    styles="",
    fmt="image/png",
    transparent=True,
    layers="test_data",
    COLORSCALERANGE="0,10",
)

w0.add_to(m)

w1 = WmsTileLayer(
    "http://this.wms.server/ncWMS/wms",
    name="Test WMS Data",
    styles="",
    fmt="image/png",
    transparent=True,
    layers="test_data_2",
    COLORSCALERANGE="0,5",
)

w1.add_to(m)

# Add WmsTileLayers to time control.

time = TimestampedWmsTileLayers([w0, w1], period='P1Y')

time.add_to(m)

layer_control = folium.LayerControl()
layer_control.add_to(m)

conoconColor = {
    "Climate Change" : "red",
    "Water" : "blue",
    "Biodiversity" : "lightgreen",
    "Stakeholder Engagement" : "orange"
}

# Parse IconLocationsPercent.txt
icon_data = []

with open('IconLocationsPercent.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            name, variant, lat, lon = line.split(', ')
            lat = -(float(lat) * 180 / 80 - 90)
            lon = float(lon) * 360 / 80 - 180
            color = conoconColor.get(variant, 'red')
            icon_data.append([lat, lon, f'<b>{name}</b>', color])

# Create IconMarkers and add them to the map
for data in icon_data:
    folium.Marker(
        location=(data[0], data[1]),
        icon=folium.Icon(color=data[3]),
        popup=data[2]
    ).add_to(m)

with open('IconLocationsPercent.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            name, variant, lat, lon = line.split(', ')
            lat = -(float(lat) * 180 / 100 - 90) + 30
            lon = float(lon) * 360 / 100 - 180
            color = conoconColor[variant] if variant in conoconColor else 'red'
            icon_data.append([lat, lon, f'<b>{name}</b>: {variant}', color])

# Create IconMarkers and add them to the map
for data in icon_data:
    folium.Marker(
        location=(data[0], data[1]),
        icon=folium.Icon(color=data[3]),
        popup=data[2]
    ).add_to(m)

m.save("index.html")
webbrowser.open("index.html")

