import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Fraud and IdCountry Theft Report'
APP_SUB_TITLE = 'Source: Federal Trade Commission'

csv_files = [
    "agricultural-land.csv",
    "change-forest-area-share-total.csv",
    "climate-change.csv",
    "consumption-of-ozone-depleting-substances.csv",
    "fossil-fuel-primary-energy.csv",
    "fossil-fuels-per-capita.csv",
    "owid-energy-data.csv",
    "global-living-planet-index.csv",
    "share-deaths-air-pollution.csv",
    "water-and-sanitation.csv"
]

# Directory path where the CSV files are located
dir_path = "./Backend/CSV/"

# Corresponding simplified names
simplified_names = [
    "Agricultural Land",
    "Change in Forest Area Share Total",
    "Climate Change",
    "Consumption of Ozone-Depleting Substances",
    "Fossil Fuel Primary Energy",
    "Fossil Fuels Per Capita",
    "OWID Energy Data",
    "Global Living Planet Index",
    "Share of Deaths from Air Pollution",
    "Water and Sanitation"
]

# Create a list of tuples with simplified names, file names, and directory path
file_info = list(zip(simplified_names, csv_files, [dir_path] * len(csv_files)))

# Streamlit UI
st.title("Data Sector Selector")

# Dropdown menu to select a dataset
selected_dataset = st.selectbox("Select a dataset", simplified_names)

# Find the corresponding file name and directory path
selected_file_info = next(info for info in file_info if info[0] == selected_dataset)

full_path = os.path.join(selected_file_info[2], selected_file_info[1])

# Read the CSV file using Pandas
try:
    df = pd.read_csv(full_path)
    st.write(f"Showing contents of {selected_file_info[0]}")
    st.dataframe(df)
    attributes = [col for col in df.columns if col not in ['Country', 'Year','Code']]
    countries = df['Country'].unique().tolist()

    # Streamlit UI
    st.title("CSV Data Viewer")
    # Multiselect for selecting attributes
    selected_attributes = st.multiselect("Select Attributes", attributes)

    # Dropdown for selecting all countries
    selected_countries = st.multiselect("Select Countries", countries)

    # Dropdown for selecting the year
    selected_year = st.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))

    # Filter the dataframe based on user selections
    filtered_df = df[(df['Country'].isin(selected_countries)) & (df['Year'] == selected_year)]
    selected_attributes.append('Country')        
    # filtered_df = filtered_df.rename(columns={'Country': 'Country'})
    selected_attributes.reverse()
    # Display the filtered dataframe
    if not selected_attributes:
        st.warning("Please select at least one attribute.")
    else:

        st.dataframe(filtered_df[selected_attributes], hide_index=True)
    st.title(filtered_df)        
except FileNotFoundError:
    st.error(f"File not found: {full_path}")
except pd.errors.EmptyDataError:
    st.error(f"The selected CSV file is empty: {full_path}")    


