import folium
from folium import *
import webbrowser
from folium.plugins import *
import json
import pandas as pd

def create_map(columns, df):
    tile_layer = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
        min_zoom=3,
    )

    m = folium.Map(location=[-23, -46],
                zoom_start=3, no_wrap=True,world_copy_jump=True, tiles=tile_layer
                )

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
    iso_code_dict = {}
    for index, row in df.iterrows():
        iso_code = row['iso_code']
        if row['year'] == year and iso_code not in iso_code_dict:
            iso_code_dict[iso_code] = row

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
            #tooltip=tooltip,
            html = '<canvas id="myChart" style="width:100%;max-width:700px"></canvas>',
            parse_html=True
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

    return m

if __name__ == '__main__':
    m = create_map()
    m.save("index.html")
    webbrowser.open("index.html")