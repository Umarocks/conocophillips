

import folium
import webbrowser
from folium.plugins import *

m = folium.Map(
    location=(45.5236, -122.6750),
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    attr='Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, USGS, Intermap, iPC, NRCAN, Esri Japan, METI, Esri China (Hong Kong), Esri (Thailand), TomTom, 2012',
    min_zoom = 3,
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

m.save("index.html")
webbrowser.open("index.html")

