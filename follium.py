

import folium
import webbrowser

m = folium.Map(
    location=(45.5236, -122.6750),
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
    min_zoom = 3
)

m.save("index.html")
webbrowser.open("index.html")

