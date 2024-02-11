# Data Source: https://public.tableau.com/app/profile/federal.trade.commission/viz/FraudandIDTheftMaps/AllReportsbycountry
# US country Boundaries: https://public.opendatasoft.com/explore/dataset/us-country-boundaries/export/

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Fraud and Identity Theft Report'
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
st.title("CSV File Selector")

# Dropdown menu to select a dataset
selected_dataset = st.selectbox("Select a dataset", simplified_names)

# Find the corresponding file name and directory path
selected_file_info = next(info for info in file_info if info[0] == selected_dataset)




def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
    st.header(f'{year}' )
    return year

def display_country_filter(df, country_name):
    country_list = [''] + list(df['country Name'].unique())
    country_list.sort()
    country_index = country_list.index(country_name) if country_name and country_name in country_list else 0
    return st.sidebar.selectbox('country', country_list, country_index)

def display_report_type_filter():
    return st.sidebar.radio('Report Type', ['Fraud', 'Other'])

def display_map(df, year, quarter):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]

    map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
    choropleth = folium.Choropleth(
        geo_data='data/us-country-boundaries.geojson',
        data=df,
        columns=('country Name', 'country Total Reports Quarter'),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('country Name')
    for feature in choropleth.geojson.data['features']:
        country_name = feature['properties']['name']
        feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[country_name, 'country Pop'][0]) if country_name in list(df_indexed.index) else ''
        feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[country_name, 'Reports per 100K-F&O together'][0])) if country_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'population', 'per_100k'], labels=False)
    )
    
    st_map = st_folium(map, width=700, height=450)

    country_name = ''
    if st_map['last_active_drawing']:
        country_name = st_map['last_active_drawing']['properties']['name']
    return country_name

# def display_fraud_facts(df, year, quarter, report_type, country_name, field, title, string_format='${:,}', is_median=False):
#     df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
#     df = df[df['Report Type'] == report_type]
#     if country_name:
#         df = df[df['country Name'] == country_name]
#     df.drop_duplicates(inplace=True)
#     if is_median:
#         total = df[field].sum() / len(df[field]) if len(df) else 0
#     else:
#         total = df[field].sum()
#     st.metric(title, string_format.format(round(total)))

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
    df_fraud = pd.read_csv('data/AxS-Fraud Box_Full Data_data.csv')
    df_median = pd.read_csv('data/AxS-Median Box_Full Data_data.csv')
    df_loss = pd.read_csv('data/AxS-Losses Box_Full Data_data.csv')

    #Display Filters and Map
    year, quarter = display_time_filters(df_continental)
    country_name = display_map(df_continental, year, quarter)
    country_name = display_country_filter(df_continental, country_name)
    report_type = display_report_type_filter()

    #Display Metrics
    st.subheader(f'{country_name} {report_type} Facts')

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     display_fraud_facts(df_fraud, year, quarter, report_type, country_name, 'country Fraud/Other Count', f'# of {report_type} Reports', string_format='{:,}')
    # with col2:
    #     display_fraud_facts(df_median, year, quarter, report_type, country_name, 'Overall Median Losses Qtr', 'Median $ Loss', is_median=True)
    # with col3:
    #     display_fraud_facts(df_loss, year, quarter, report_type, country_name, 'Total Losses', 'Total $ Loss')        


if __name__ == "__main__":
    main()