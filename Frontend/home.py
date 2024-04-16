# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Point
# import numpy as np
# import base64
# from streamlit_modal import Modal

# # convert background image to base64
# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# # set background image
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

# '# L\'Avenir Holdings Inc Dashboard'
# # streamlit run home.py 
# st.tabs(["HOME", "PREDICTION", "SETTINGS", "ABOUT"])

# # Load data
# @st.cache_data
# def load_data():
#     return pd.read_excel('merged_df.xlsx')

# # Filter data based on selected year and neighborhood
# @st.cache_data
# def filter_data(data, year_range, price):
#     filtered_data = data[(data['Prior Sale Date', 'Year Built', 'Last Sale Date'].isin(range(year_range[0], year_range[1] + 1)) & data['Neighborhood'].isin(range(price[0], price[1] + 1)))]
#     return filtered_data

# # Get unique values for sliders
# @st.cache_data
# def get_slider_ranges(data, column_name):
#     return (int(data[column_name].min()), int(data[column_name].max()))

# # @st.cache_data
# # def refresh_map(filtered_gdf):
#     # st.map(filtered_gdf, longitude='lng', latitude='lat', zoom=8)

# # Set the location to Florida
# florida_location = [27.994402, -81.760254]  # Center of Florida

# # Load data
# data = load_data()

# # Step 2: Drop rows with missing values
# data = data.dropna(subset=['lat', 'lng', 'Situs Zip Code', 'Last Sale Date','Prior Sale Date', 'Year Built'])

# # Step 3: Convert 'Last Sale Date' column to datetime
# data['Last Sale Date'] = pd.to_datetime(data['Last Sale Date'], format='%m/%d/%Y')
# data['Prior Sale Date'] = pd.to_datetime(data['Prior Sale Date'], format='%m/%d/%Y')

# # Step 4: Add 'Last Sale Year' column
# data['Last Sale Year'] = data['Last Sale Date'].dt.year
# data['Prior Sale Year'] = data['Prior Sale Date'].dt.year

# # Create a GeoDataFrame around the Florida location
# geometry = [Point(xy) for xy in zip(data['lng'], data['lat'])]
# gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

# # Plot the GeoDataFrame on Streamlit map
# st.map(gdf, longitude='lng', latitude='lat', zoom=8)
# #  size=20, color='#0044ff',

# # Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
# year_min = min(data['Value Data Source'].min(), data['Parcel Characteristics Data'].min())
# year_values = min(data['Year Built'].min(), data['Year Built'].min())
# year_max = max(data['Value Data Source'].max(), data['Parcel Characteristics Data'].max())

# col1, col2 = st.columns(2)

# with col1:
#     # Convert all values to floats
#     values = [float(value) for value in year_values]

# # Pass the converted values to the slider
# # st.slider('Slider', min_value=min_value, max_value=max_value, value=values)

#     # Year slider
#     selected_year = st.slider('Year', year_min, year_max, (year_min, year_max), value=year_values)

#     # Buyer dropdown
#     buyers = data['Owner 1'].unique().tolist()
#     selected_buyer = st.selectbox('Buyer', ['All'] + buyers)
    

# with col2:
#     # Price slider
#     min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
#     selected_price = st.slider('Price', min_price, max_price, (min_price, max_price))
    
#     # Neighborhood dropdown
#     neighborhoods = data['Neighborhood'].unique().tolist()
#     selected_neighborhood = st.selectbox('Neighborhood', ['All'] + neighborhoods)

# # Filter data based on selected filters
# filtered_data = filter_data(data, selected_year, selected_price)
# # selected_buyer


# # Filter data based on selected buyer
# if selected_buyer != 'All':
#     filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# # Filter data based on selected price range
# filtered_data = filtered_data[(filtered_data['Last Sale Amount'] >= selected_price[0]) & (filtered_data['Last Sale Amount'] <= selected_price[1])]

# # Update geometry column
# filtered_geometry = [Point(xy) for xy in zip(filtered_data['lng'], filtered_data['lat'])]
# filtered_gdf = gpd.GeoDataFrame(filtered_data, geometry=filtered_geometry, crs="EPSG:4326")

# # refresh_map(filtered_gdf)
# # Plot the GeoDataFrame on Streamlit map after filtering
# # st.map(filtered_gdf, longitude='lng', latitude='lat', zoom=8)

# col3 = st.columns(1)

# with col3:
#     # Display filtered data
#     st.title('Filtered Data')
#     st.write(filtered_data.T)

# # modal = Modal(key="Demo Key",title="test")
# # for col in st.columns(8):
# #     with col:
# #         open_modal = st.button(label='clicck')
# #         if open_modal:
# #             with modal.container():
# #                 # st.markdown('testtesttesttesttesttesttesttest')
# #                 for index, row in filtered_data.iterrows():
# #                     for col in filtered_data.columns:
# #                         st.markdown(f"{col}: {row[col]}")

# # Display selected price range
# st.title('Selected Price Range')
# st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import base64

# convert background image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# set background image
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

'# L\'Avenir Holdings Inc Dashboard'
# streamlit run home.py 
st.tabs(["HOME", "PREDICTION", "SETTINGS", "ABOUT"])

# Load data
@st.cache_data
def load_data():
    return pd.read_excel('merged_df.xlsx')

# Filter data based on selected year and neighborhood
@st.cache_data
def filter_data(data, year_range, price):
    filtered_data = data[(data['Prior Sale Year'].isin(range(year_range[0], year_range[1] + 1))) & 
                         (data['Neighborhood'].isin(range(price[0], price[1] + 1)))]
    return filtered_data

# Get unique values for sliders
@st.cache_data
def get_slider_ranges(data, column_name):
    return (int(data[column_name].min()), int(data[column_name].max()))

# Set the location to Florida
florida_location = [27.994402, -81.760254]  # Center of Florida

# Load data
data = load_data()

# Step 2: Drop rows with missing values
data = data.dropna(subset=['lat', 'lng', 'Situs Zip Code', 'Last Sale Date','Prior Sale Date', 'Year Built'])

# Step 3: Convert 'Last Sale Date' column to datetime
data['Last Sale Date'] = pd.to_datetime(data['Last Sale Date'], format='%m/%d/%Y')
data['Prior Sale Date'] = pd.to_datetime(data['Prior Sale Date'], format='%m/%d/%Y')

# Step 4: Add 'Last Sale Year' column
data['Last Sale Year'] = data['Last Sale Date'].dt.year
data['Prior Sale Year'] = data['Prior Sale Date'].dt.year
data['Year Built'] = data['Year Built'].astype('int64')

# Create a GeoDataFrame around the Florida location
geometry = [Point(xy) for xy in zip(data['lng'], data['lat'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

# Plot the GeoDataFrame on Streamlit map
st.map(gdf, longitude='lng', latitude='lat', zoom=8)

# Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
year_min = min(data['Last Sale Year'].min(), data['Prior Sale Year'].min(), data['Year Built'].min())
year_max = max(data['Last Sale Year'].max(), data['Prior Sale Year'].max(), data['Year Built'].max())

col1, col2 = st.columns(2)

with col1:
    # Year slider
    selected_year = st.slider('Year', year_min, year_max, (year_min, year_max))

    # Buyer dropdown
    buyers = data['Owner 1'].unique().tolist()
    selected_buyer = st.selectbox('Buyer', ['All'] + buyers)

with col2:
    # Price slider
    min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
    selected_price = st.slider('Price', min_price, max_price, (min_price, max_price))
    
    # Neighborhood dropdown
    neighborhoods = data['Neighborhood'].unique().tolist()
    selected_neighborhood = st.selectbox('Neighborhood', ['All'] + neighborhoods)

# Filter data based on selected filters
filtered_data = filter_data(data, selected_year, selected_price)

# Filter data based on selected buyer
if selected_buyer != 'All':
    filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# Display selected price range
st.title('Selected Price Range')
st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')

# Display filtered data
st.title('Filtered Data')
st.write(filtered_data.T)


# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# from shapely.geometry import Point
# import numpy as np
# import base64

# # convert background image to base64
# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# # set background image
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

# '# L\'Avenir Holdings Inc Dashboard'
# # streamlit run home.py 
# st.tabs(["HOME", "PREDICTION", "SETTINGS", "ABOUT"])

# # Load data
# @st.cache_data
# def load_data():
#     return pd.read_excel('merged_df.xlsx')

# # Filter data based on selected year and neighborhood
# @st.cache_data
# def filter_data(data, year_range, price):
#     filtered_data = data[(data['Prior Sale Year'].isin(range(year_range[0], year_range[1] + 1))) & 
#                          (data['Neighborhood'].isin(range(price[0], price[1] + 1)))]
#     return filtered_data

# # Get unique values for sliders
# @st.cache_data
# def get_slider_ranges(data, column_name):
#     return (int(data[column_name].min()), int(data[column_name].max()))

# # Set the location to Florida
# florida_location = [27.994402, -81.760254]  # Center of Florida

# # Load data
# data = load_data()

# # Step 2: Drop rows with missing values
# data = data.dropna(subset=['lat', 'lng', 'Situs Zip Code', 'Last Sale Date','Prior Sale Date', 'Year Built'])

# # Step 3: Convert 'Last Sale Date' column to datetime
# data['Last Sale Date'] = pd.to_datetime(data['Last Sale Date'], format='%m/%d/%Y')
# data['Prior Sale Date'] = pd.to_datetime(data['Prior Sale Date'], format='%m/%d/%Y')
# data['Year Built'] = data['Year Built'].astype('int64')

# # Step 4: Add 'Last Sale Year' column
# data['Last Sale Year'] = data['Last Sale Date'].dt.year
# data['Prior Sale Year'] = data['Prior Sale Date'].dt.year

# # Create a GeoDataFrame around the Florida location
# geometry = [Point(xy) for xy in zip(data['lng'], data['lat'])]
# gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

# # Plot the GeoDataFrame on Streamlit map
# st.map(gdf, longitude='lng', latitude='lat', zoom=8)

# # Concatenate 'Value Data Source' and 'Parcel Characteristics Data' for year range
# year_min = min(data['Last Sale Year'].min(), data['Prior Sale Year'].min(), data['Year Built'].min())
# year_max = max(data['Last Sale Year'].max(), data['Prior Sale Year'].max(), data['Year Built'].max())

# col1, col2 = st.columns(2)

# with col1:
#     # Year slider
#     selected_year = st.slider('Year', year_min, year_max, (year_min, year_max))

#     # Buyer dropdown
#     buyers = data['Owner 1'].unique().tolist()
#     selected_buyer = st.selectbox('Buyer', ['All'] + buyers)

# with col2:
#     # Price slider
#     min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
#     selected_price = st.slider('Price', min_price, max_price, (min_price, max_price))
    
#     # Neighborhood dropdown
#     neighborhoods = data['Neighborhood'].unique().tolist()
#     selected_neighborhood = st.selectbox('Neighborhood', ['All'] + neighborhoods)

# # Filter data based on selected filters
# filtered_data = filter_data(data, selected_year, selected_price)

# # Filter data based on selected buyer
# if selected_buyer != 'All':
#     filtered_data = filtered_data[filtered_data['Owner 1'] == selected_buyer]

# # Display selected price range
# st.title('Selected Price Range')
# st.write(f'Min Price: {selected_price[0]} - Max Price: {selected_price[1]}')

# # Display filtered data
# st.title('Filtered Data')
# st.write(filtered_data.T)
