import streamlit as st
from streamlit_folium import st_folium
import follium

m = follium.create_map('owid-energy-data', 2020)

st_folium(
    m,
    zoom=5,
    key="new",
    height=400,
    width=700,
)