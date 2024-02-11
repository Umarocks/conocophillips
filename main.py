import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import *
from folium.plugins import *
import pandas as pd
parse_schemas = __import__('Backend/parse_schemas.py')

filename = 'owid-energy-data'
columns = parse_schemas.get_columns(filename)

import follium
df = pd.read_csv(f'Backend/CSV/{filename}.csv')
m = follium.create_map(columns, df)

st_folium(
    m,
    zoom=5,
    key="new",
    height=400,
    width=700,
)