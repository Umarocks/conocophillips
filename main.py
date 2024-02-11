import streamlit as st
from streamlit_folium import st_folium
import follium
import pandas as pd
import parse_schemas

filename = 'owid-energy-data'
schema = parse_schemas.get_schema()
columns = schema[filename][0]

df = pd.read_csv(f'Backend/CSV/{filename}.csv')
m = follium.create_map(columns, df, 2020)

st_folium(
    m,
    zoom=5,
    key="new",
    height=400,
    width=700,
)