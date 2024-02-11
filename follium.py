

import folium
import webbrowser

m = folium.Map(location=(45.5236, -122.6750))

m.save("index.html")
webbrowser.open("index.html")

