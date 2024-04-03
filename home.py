import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import base64
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

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
    return pd.read_excel('SCPA Public.xlsx')

# Geocode situs address
@st.cache_data
def geocode_situs_address(data):
    geometries = []
    for _, row in data.iterrows():
        location = gpd.tools.geocode('{}, {}, {}, {}'.format(row['Situs Address (Property Address)'], row['Situs City'], row['Situs State'], row['Situs Zip Code']))
        if not location.empty:
            point = Point(location.iloc[0].geometry.x, location.iloc[0].geometry.y)
            geometries.append(point)
    return gpd.GeoDataFrame(geometry=geometries, crs='EPSG:4326')

# Filter data based on selected year and neighborhood
@st.cache_data
def filter_data(data, year_range, neighborhood):
    filtered_data = data[(data['Value Data Source'].isin(range(year_range[0], year_range[1] + 1))) & (data['Neighborhood'] == neighborhood)]
    return filtered_data

# Get unique values for sliders
@st.cache_data
def get_slider_ranges(data, column_name):
    return (int(data[column_name].min()), int(data[column_name].max()))

# Set the location to Florida
florida_location = [27.994402, -81.760254]  # Center of Florida

# Load data
data = load_data()

# Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
year_min = min(data['Value Data Source'].min(), data['Parcel Characteristics Data'].min())
year_max = max(data['Value Data Source'].max(), data['Parcel Characteristics Data'].max())

# Create folium map
map = folium.Map(location=florida_location, zoom_start=8)

# Create marker cluster
marker_cluster = MarkerCluster().add_to(map)

# Set up sidebar
# st.sidebar.title('Filters')


# Display the map
# st.title('Property Map')
folium_static(map)

# Year slider
selected_year = st.slider('Year', year_min, year_max, (year_min, year_max))

# Neighborhood dropdown
neighborhoods = data['Neighborhood'].unique().tolist()
selected_neighborhood = st.selectbox('Neighborhood', ['All'] + neighborhoods)

# Buyer dropdown
buyers = data['Owner 1'].unique().tolist()
selected_buyer = st.selectbox('Buyer', ['All'] + buyers)

# Price slider
min_price, max_price = get_slider_ranges(data, 'Neighborhood')
selected_price = st.slider('Price', min_price, max_price, (min_price, max_price))

# Filter data based on selected filters
filtered_data = filter_data(data, selected_year, selected_neighborhood)

# Filter data based on selected buyer
if selected_buyer != 'All':
    filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# Geocode situs addresses
if 'situs_coordinates' not in st.session_state:
    situs_coordinates = geocode_situs_address(filtered_data[['Situs Address (Property Address)', 'Situs City', 'Situs State', 'Situs Zip Code']])
    st.session_state.situs_coordinates = situs_coordinates
else:
    situs_coordinates = st.session_state.situs_coordinates

# Add markers to the marker cluster
for index, row in situs_coordinates.iterrows():
    popup_text = f"{row['Situs Address (Property Address)']}, {row['Situs City']}, {row['Situs State']}, {row['Situs Zip Code']}"
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup=popup_text).add_to(marker_cluster)

# Display filtered data
st.title('Filtered Data')
st.write(filtered_data)

# Display selected price range
st.title('Selected Price Range')
st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')

# Initialize clicked_cluster in session state
if 'clicked_cluster' not in st.session_state:
    st.session_state.clicked_cluster = None
    
# Show row when a cluster is clicked
if st.session_state.clicked_cluster is not None:
    cluster_data = filtered_data.iloc[st.session_state.clicked_cluster]
    st.write('Clicked Cluster Data:')
    st.write(cluster_data)

# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Point
# import numpy as np
# import base64
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import folium_static

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('./images/background.png')

# '# L\'Avenir Holdings Inc updates Dashboard'
# # streamlit run practice.py 
# st.tabs(["HOME", "VIEW BUYERS", "HISTORY", "ABOUT"])

# # Load data
# @st.cache_data
# def load_data():
#     return pd.read_excel('SCPA Public.xlsx')

# # Geocode situs address
# @st.cache_data
# def geocode_situs_address(data):
#     geometries = []
#     for _, row in data.iterrows():
#         location = gpd.tools.geocode('{}, {}, {}, {}'.format(row['Situs Address (Property Address)'], row['Situs City'], row['Situs State'], row['Situs Zip Code']))
#         if not location.empty:
#             point = Point(location.iloc[0].geometry.x, location.iloc[0].geometry.y)
#             geometries.append(point)
#     return gpd.GeoDataFrame(geometry=geometries, crs='EPSG:4326')

# # Filter data based on selected year and neighborhood
# @st.cache_data

# def filter_data(data, year_range, price_range):
#     filtered_data = data[(data['Value Data Source'].isin(range(year_range[0], year_range[1] + 1))) & 
#                          (data['Just Value'] >= price_range[0]) & 
#                          (data['Just Value'] <= price_range[1])]
#     return filtered_data

# # Get unique values for sliders
# @st.cache_data
# def get_slider_ranges(data, column_name):
#     return (int(data[column_name].min()), int(data[column_name].max()))

# # Set the location to Florida
# florida_location = [27.994402, -81.760254]  # Center of Florida

# # Load data
# data = load_data()

# # Create folium map
# map = folium.Map(location=florida_location, zoom_start=8)

# # Create marker cluster
# marker_cluster = MarkerCluster().add_to(map)

# # Display the map
# folium_static(map)

# # Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
# year_min = min(data['Value Data Source'].min(), data['Parcel Characteristics Data'].min())
# year_max = max(data['Value Data Source'].max(), data['Parcel Characteristics Data'].max())

# col1, col2 = st.columns(2)

# with col1:
#     # Year slider
#     selected_year = st.slider('Year', year_min, year_max, (year_min, year_max))

# with col2:
#     # Price slider using Just Value, Assessed Value, and Taxable Value
#     price_min = data[['Just Value', 'Assessed Value', 'Taxable Value']].min().min()
#     price_max = data[['Just Value', 'Assessed Value', 'Taxable Value']].max().max()
#     selected_price = st.slider('Price', price_min, price_max, (price_min, price_max))


# # Buyer dropdown
# buyers = data['Owner 1'].unique().tolist()
# selected_buyer = st.selectbox('Buyer', ['All'] + buyers)

# # Filter data based on selected filters
# filtered_data = filter_data(data, selected_year, selected_price)

# # Filter data based on selected buyer
# if selected_buyer != 'All':
#     filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# # Geocode situs addresses
# if 'situs_coordinates' not in st.session_state:
#     situs_coordinates = geocode_situs_address(filtered_data[['Situs Address (Property Address)', 'Situs City', 'Situs State', 'Situs Zip Code']])
#     st.session_state.situs_coordinates = situs_coordinates
# else:
#     situs_coordinates = st.session_state.situs_coordinates

# # Add markers to the marker cluster
# for index, row in situs_coordinates.iterrows():
#     popup_text = f"{row.geometry.x}, {row.geometry.y}, {row['Situs City']}, {row['Situs State']}, {row['Situs Zip Code']}"
#     folium.Marker(location=[row.geometry.y, row.geometry.x], popup=popup_text).add_to(marker_cluster)

# # Display filtered data
# st.title('Filtered Data')
# st.write(filtered_data)

# # Display selected price range
# st.title('Selected Price Range')
# st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')

# # # Initialize clicked_cluster in session state
# # if 'clicked_cluster' not in st.session_state:
# #     st.session_state.clicked_cluster = None
    
# # # Show row when a cluster is clicked
# # if st.session_state.clicked_cluster is not None:
# #     cluster_data = filtered_data.iloc[st.session_state.clicked_cluster]
# #     st.write('Clicked Cluster Data:')
# #     st.write(cluster_data)