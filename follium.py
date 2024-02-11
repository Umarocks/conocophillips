import folium
from folium import *
import webbrowser
from folium.plugins import *
import json
import random
import pandas as pd

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

m = folium.Map(
    location=(45.5236, -122.6750),
    tiles=tile_layer,
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

folium.Marker(
    location=(45, -122),
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Circle(
    location=(45, -122),
    radius=1000,
    color='purple',
    fill=True,
    fill_color='purple'
).add_to(m)

folium.Circle(
    location=(45, -122),
    radius=100,
    color='blue',
    fill=True,
    fill_color='blue',
    fill_opacity=0.6,
    weight=1,
    popup='Water Amount: 100000'
).add_to(m)


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

with open('datasets/world-countries.json') as handle:
    country_geo = json.loads(handle.read())

country_layer = folium.FeatureGroup(name='Countries')
country_layer.add_to(m)

for feature in country_geo['features']:
    folium.GeoJson(feature).add_to(country_layer)

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

time = TimestampedWmsTileLayers([w0, w1])

time.add_to(m)

layer_control = folium.LayerControl()
layer_control.add_to(m)

# Load the CSV file into a DataFrame
df = pd.read_csv('Backend/CSV/owid-energy-data.csv')
numpy_array = df.to_numpy()
# Specify the year and country you want to filter
desired_year = 2008
desired_country = 'USA'

# Filter the DataFrame based on the specified year and country
filtered_df = df[(df['year'] == desired_year) & (df['iso_code'] == desired_country)]

filtered_df = filtered_df.dropna(subset=['latitude', 'longitude'])  # Drop rows with NaN values in latitude and longitude columns

filtered_df = filtered_df.to_json(orient='records')

# Add the filtered DataFrame to the map
for i in range(0, len(numpy_array)):
    folium.Marker([numpy_array[i][2], numpy_array[i][3]], popup=numpy_array[i][0]).add_to(m)

m.save("index.html")
webbrowser.open("index.html")

