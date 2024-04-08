import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./images/background.png')

'# L\'Avenir Holdings Inc updates Dashboard'
# streamlit run practice.py 
st.tabs(["HOME", "VIEW BUYERS", "HISTORY", "ABOUT"])

# Load data
@st.cache_data
def load_data():
    return pd.read_excel('merged_df.xlsx')

# Filter data based on selected year and neighborhood
@st.cache_data
def filter_data(data, year_range, neighborhood):
    filtered_data = data[(data['Value Data Source'].isin(range(year_range[0], year_range[1] + 1))) & (data['Neighborhood'] == neighborhood)]
    return filtered_data

# Get unique values for sliders
@st.cache_data
def get_slider_ranges(data, column_name):
    return (int(data[column_name].min()), int(data[column_name].max()))

# @st.cache_data
def refresh_map(filtered_gdf):
    st.map(filtered_gdf, longitude='lng', latitude='lat', zoom=8)

# Set the location to Florida
florida_location = [27.994402, -81.760254]  # Center of Florida

# Load data
data = load_data()

# Drop rows with missing latitude or longitude values
data = data.dropna(subset=['lat', 'lng'])

# Create a GeoDataFrame around the Florida location
geometry = [Point(xy) for xy in zip(data['lng'], data['lat'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

# Plot the GeoDataFrame on Streamlit map
st.map(gdf, longitude='lng', latitude='lat', zoom=8)

# Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
year_min = min(data['Value Data Source'].min(), data['Parcel Characteristics Data'].min())
year_max = max(data['Value Data Source'].max(), data['Parcel Characteristics Data'].max())

col1, col2 = st.columns(2)

with col1:
    # Year slider
    selected_year = st.slider('Year', year_min, year_max, (year_min, year_max))

    # Buyer dropdown
    buyers = data['Owner 1'].unique().tolist()
    selected_buyer = st.selectbox('Buyer', ['All'] + buyers)
    

with col2:
    # Price slider
    min_price, max_price = get_slider_ranges(data, 'Neighborhood')
    selected_price = st.slider('Price', min_price, max_price, (min_price, max_price))
    
    # Neighborhood dropdown
    neighborhoods = data['Neighborhood'].unique().tolist()
    selected_neighborhood = st.selectbox('Neighborhood', ['All'] + neighborhoods)

# Filter data based on selected filters
filtered_data = filter_data(data, selected_year, selected_neighborhood)

# Filter data based on selected buyer
if selected_buyer != 'All':
    filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# Filter data based on selected filters 
# filtered_data = filter_data(data, selected_year, selected_neighborhood)

# Filter data based on selected buyer
if selected_buyer != 'All':
    filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]
    
# Filter data based on selected price range
filtered_data = filtered_data[(filtered_data['Neighborhood'] >= selected_price[0]) & (filtered_data['Neighborhood'] <= selected_price[1])]

# Update geometry column
filtered_geometry = [Point(xy) for xy in zip(filtered_data['lng'], filtered_data['lat'])]
filtered_gdf = gpd.GeoDataFrame(filtered_data, geometry=filtered_geometry, crs="EPSG:4326")

# refresh_map(filtered_gdf)
# Plot the GeoDataFrame on Streamlit map after filtering
# st.map(filtered_gdf, longitude='lng', latitude='lat', zoom=8)

# Display filtered data
st.title('Filtered Data')
st.write(filtered_data)

# Display selected price range
st.title('Selected Price Range')
st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')
