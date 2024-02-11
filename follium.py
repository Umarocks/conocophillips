import parse_schemas
import folium
from folium import *
import webbrowser
from folium.plugins import *
import json
import pandas as pd
import re

continents = ['Low-income countries', 'High-income countries', 'Lower-middle-income countries', 'Upper-middle-income countries', 'World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

def create_map_2(columns, df, year, primary_key, gradient):
    value_dict = {}

    min = 999999999999999
    max = -999999999999999
    for index, row in df.iterrows():
        if 'Country' in row and (row['Country'] in continents or re.match('^.*\([A-Z]+\).*$', row['Country'])):
            continue
        if (row['year'] if 'year' in row else row['Year']) == year:
            if primary_key not in row:
                raise ValueError(f"Primary key '{primary_key}' not found in row {row}")
            if row[primary_key] < min:
                min = row[primary_key]
            if row[primary_key] > max:
                max = row[primary_key]
    print(min, max)

    tile_layer = folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
        min_zoom=3,
        name=primary_key
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

    # Load the CSV file into a DataFrame
    iso_code_dict = {}
    for index, row in df.iterrows():
        iso_code = row['iso_code'] if 'iso_code' in row else row['Code']
        if (row['year'] if 'year' in row else row['Year']) == year and iso_code not in iso_code_dict:
            iso_code_dict[iso_code] = row

    for feature in country_geo['features']:
        iso_code = feature['id']
        
        tooltip = ''
        if iso_code in iso_code_dict:
            data = iso_code_dict[iso_code]
            for column in columns:
                if column in data and not pd.isna(data[column]):
                    tooltip += f'{column}: {data[column]}<br>'
        else:
            folium.GeoJson(
                feature,
                style_function=lambda feature: {
                    'fillColor': 'white',
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 1,
                },
                tooltip=f'No data available for this country in {year}.'
            ).add_to(country_layer)
            continue
        
        value = ((data[primary_key] - min) / (max - min)) if primary_key in data else 0.25
        value_dict[iso_code] = [
            value,
            gradient.to_hex(gradient.get_blended_color(value)),
            gradient.to_hex(gradient.get_blended_color(1 - value))
        ]

        folium.GeoJson(
            feature,
            style_function=lambda feature: {
                'fillColor': value_dict[feature['id']][1],
                'color': value_dict[feature['id']][2],
                'weight': 2,
                'fillOpacity': value_dict[feature['id']][0],
            },
            tooltip=tooltip,
            zoom_on_click = True
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
        'Climate Change' : 'red',
        'Water' : 'blue',
        'Biodiversity' : 'lightgreen',
        'Stakeholder Engagement' : 'orange'
    }

    descriptions = []
    with open('IconDescriptions.txt', 'r', encoding='utf-8') as file:
        fulltext = ''.join(file.readlines())

        descriptions = re.split(';\n[0-9]+:', fulltext)
        descriptions = [x.strip() for x in descriptions]
        descriptions = [x for x in descriptions if x]

    # Parse IconLocationsPercent.txt
    icon_data = []

    with open('IconLocationsPercent.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line: #new item "country name" added to list, be sure to account for this
                name, variant, lat, lon, country_name = line.split(', ')
                lat = -(float(lat) * 180 / 100 - 90) #why is there an outer negative sign?
                lon = float(lon) * 360 / 100 - 180
                color = conoconColor.get(variant, 'red')
                icon_data.append([lat, lon, f'<b>{country_name}</b></br><b>{name}</b></br>{descriptions.pop()}', color])

    # Create IconMarkers and add them to the map
    for data in icon_data:
        folium.Marker(
            location=(data[0], data[1]),
            icon=folium.Icon(color=data[3]),
            popup=data[2]
        ).add_to(m)

    fullscreen_control = Fullscreen()
    fullscreen_control.add_to(m)

    return m

def create_map(filename, year, primary_key):
    schema = parse_schemas.get_schema()
    columns = schema[filename][0]
    gradient = schema[filename][2]
    df = pd.read_csv(f'Backend/CSV/{filename}.csv')
    return create_map_2(columns, df, year, primary_key, gradient)

if __name__ == '__main__':
    #m = create_map('agricultural-land', 2020, 'Agricultural land')
    m = create_map('fossil-fuels-per-capita', 2019, 'Fossil fuels per capita (kWh)')
    #m = create_map('fossil-fuel-primary-energy', 2019, 'Fossil fuels (TWh)')
    m.save('index.html')
    webbrowser.open('index.html')