import folium
from folium import *
import webbrowser
from folium.plugins import *
import json
import pandas as pd

def create_map_2(columns, df, year, primary_key):
    value_dict = {}

    min = 999999999999999
    max = -999999999999999
    for index, row in df.iterrows():
        if 'Entity' in row and (row['Entity'] in ['Low-income countries', 'High-income countries', 'Lower-middle-income countries', 'Upper-middle-income countries', 'World', 'Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'] or '(FAO)' in row['Entity']):
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
                    'fillColor': 'red',
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.25,
                },
                tooltip=f'No data available for this country in {year}.'
            ).add_to(country_layer)
            continue
        
        value = ((data[primary_key] - min) / (max - min)) if primary_key in data else 0.25
        value = value ** 0.7
        value_dict[iso_code] = value

        folium.GeoJson(
            feature,
            style_function=lambda feature: {
                'fillColor': 'green',
                'color': 'black',
                'weight': 2,
                'fillOpacity': value_dict[feature['id']],
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

    # Parse IconLocationsPercent.txt
    icon_data = []

    with open('IconLocationsPercent.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line: #new item "country name" added to list, be sure to account for this
                name, variant, lat, lon = line.split(', ')
                lat = -(float(lat) * 180 / 100 - 90) #why is there an outer negative sign?
                lon = float(lon) * 360 / 100 - 180
                color = conoconColor.get(variant, 'red')
                icon_data.append([lat, lon, f'<b>{name}</b>', color])

    # Create IconMarkers and add them to the map
    for data in icon_data:
        folium.Marker(
            location=(data[0], data[1]),
            icon=folium.Icon(color=data[3]),
            popup=data[2]
        ).add_to(m)

    return m

def create_map(filename, year):
    schema = parse_schemas.get_schema()
    columns = schema[filename][0]
    df = pd.read_csv(f'Backend/CSV/{filename}.csv')
    primary_key = schema[filename][1]
    return create_map_2(columns, df, year, primary_key)

if __name__ == '__main__':
    import parse_schemas
    m = create_map('agricultural-land', 2020)
    m.save('index.html')
    webbrowser.open('index.html')