import pandas
import json
import requests
import folium
import webbrowser
state_geo = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json"
).json()
# print(state_geo)
state_data = pandas.read_csv(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_unemployment_oct_2012.csv"
)
# print(state_data)
my_map= folium.Map(location=[48, -102], zoom_start=3)

folium.Choropleth(
    geo_data=state_geo,
    name="choropleth",
    data=state_data,
    columns=["State", "Unemployment"],
    key_on="feature.id",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Unemployment Rate (%)",
).add_to(my_map)

folium.LayerControl().add_to(my_map)

my_map.save('my_map.html')
chrome_path = 'google-chrome'
webbrowser.get(chrome_path).open('my_map.html')


