import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import base64

# Convert background image to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image
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

st.title("L'Avenir Holdings Inc Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["HOME", "PREDICTION", "SETTINGS", "ABOUT"])

@st.cache_data
def load_data(file):
    return pd.read_excel(file)

@st.cache_data
def filter_data(dataa, year_range, price, buyer, owner_column, neighborhood_column):
    if isinstance(buyer, str):
        buyer = [buyer]
    filtered_data = dataa[(dataa['Prior Sale Year'].isin(range(year_range[0], year_range[1] + 1))) & 
                          (dataa[neighborhood_column].isin(range(price[0], price[1] + 1))) & 
                          (dataa[owner_column].isin(buyer))]
    return filtered_data

@st.cache_data
def filter_data_based_on_price(dataa, price, neighborhood_column):
    filtered_data = dataa[(dataa[neighborhood_column].isin(range(price[0], price[1] + 1)))]
    return filtered_data

@st.cache_data
def filter_data_based_on_year(dataa, year_range):
    filtered_data = dataa[(dataa['Prior Sale Year'].isin(range(year_range[0], year_range[1] + 1)))]
    return filtered_data

@st.cache_data
def get_slider_ranges(data, column_name):
    return (int(data[column_name].min()), int(data[column_name].max()))

# Initialize session state for data file selection
if 'data_file' not in st.session_state:
    st.session_state['data_file'] = 'merged_df.xlsx'

# Initial data load
data = load_data(st.session_state['data_file'])

# Determine the column names based on the data file
if st.session_state['data_file'] == 'merged_df.xlsx':
    owner_column = 'Owner 1'
    neighborhood_column = 'Neighborhood'
else:
    owner_column = 'Owner'
    neighborhood_column = 'Situs City'

# Function to clean and convert numeric columns
def clean_numeric_column(series):
    series = series.apply(lambda x: str(x).split(',')[0].strip())
    series = pd.to_numeric(series, errors='coerce')
    return series

# Function to clean and convert coordinate columns
def clean_coordinate_column(series):
    series = series.apply(lambda x: str(x).split(',')[0].strip())
    series = pd.to_numeric(series, errors='coerce')
    return series

with tab1:
    data = data.dropna(subset=['lat', 'lng', 'Situs Zip Code', 'Last Sale Date', 'Prior Sale Date', 'Year Built'])
    
    # Clean date strings before converting to datetime
    data['Last Sale Date'] = data['Last Sale Date'].apply(lambda x: str(x).split(',')[0].strip())
    data['Prior Sale Date'] = data['Prior Sale Date'].apply(lambda x: str(x).split(',')[0].strip())
    
    data['Last Sale Date'] = pd.to_datetime(data['Last Sale Date'], format='%m/%d/%Y', errors='coerce')
    data['Prior Sale Date'] = pd.to_datetime(data['Prior Sale Date'], format='%m/%d/%Y', errors='coerce')
    
    data['Last Sale Year'] = data['Last Sale Date'].dt.year
    data['Prior Sale Year'] = data['Prior Sale Date'].dt.year

    # Clean and convert numeric columns
    data['Year Built'] = clean_numeric_column(data['Year Built'])

    # Clean and convert coordinate columns
    data['lat'] = clean_coordinate_column(data['lat'])
    data['lng'] = clean_coordinate_column(data['lng'])
    
    data = data.sample(frac=0.1, random_state=10)

    geometry = [Point(xy) for xy in zip(data['lng'], data['lat'])]
    gdf = gpd.GeoDataFrame(data, geometry=geometry, crs="EPSG:4326")

    st.subheader("Original map:")
    st.map(gdf, longitude='lng', latitude='lat', zoom=8)

    year_min = min(data['Last Sale Year'].min(), data['Prior Sale Year'].min(), data['Year Built'].min())
    year_max = max(data['Last Sale Year'].max(), data['Prior Sale Year'].max(), data['Year Built'].max())

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.slider('Year', 2000, 2024, (2000, 2024))
        buyers = data[owner_column].unique().tolist()
        selected_buyer = st.selectbox('Buyer', ['All'] + buyers)

    with col2:
        min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
        selected_price = st.slider('Price', 1000, 10000, (1000, 10000))
        neighborhoods = data[neighborhood_column].unique().tolist()
        selected_neighborhood = st.selectbox(neighborhood_column, ['All'] + neighborhoods)

    filtered_data = filter_data(data, selected_year, selected_price, selected_buyer, owner_column, neighborhood_column)
    geometry_filtered = [Point(xy) for xy in zip(filtered_data['lng'], filtered_data['lat'])]
    gdf_filtered = gpd.GeoDataFrame(filtered_data, geometry=geometry_filtered, crs="EPSG:4326")

    st.subheader("Filtered map:")
    st.map(gdf_filtered, longitude='lng', latitude='lat', zoom=8)

    if selected_buyer != 'All':
        filtered_data = filtered_data[filtered_data[owner_column] == selected_buyer]

    st.title('Selected Price Range')
    st.write(f'Min Price: {selected_price[0]:,} - Max Price: {selected_price[1]:,}')

    st.title('Filtered Data')
    st.write(filtered_data.T)

with tab2:
    st.subheader("What do you want to search today?")
    filter_options = ["Buyers", "Years", "Price", neighborhood_column]
    selected_filter = st.radio("Select a filter option:", filter_options, horizontal=True)
    display_data = False

    if selected_filter == "Buyers":
        buyers_predict = data[owner_column].unique().tolist()
        selected_buyer_predict = st.selectbox('Buyers', ['All'] + buyers_predict)
        if selected_buyer_predict != 'All':
            filtered_data = filtered_data[filtered_data[owner_column] == selected_buyer_predict]
            display_data = True

    elif selected_filter == "Years":
        year_min, year_max = get_slider_ranges(data, 'Last Sale Year')
        selected_year_predict = st.slider('Years', 2000, 2024, (2000, 2024))
        filtered_data = filter_data_based_on_year(data, selected_year_predict)
        display_data = True

    elif selected_filter == "Price":
        min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
        selected_price_predict = st.slider('Prices', 1000, 10000, (1000, 10000))
        filtered_data = filter_data_based_on_price(data, selected_price_predict, neighborhood_column)
        display_data = True

    elif selected_filter == neighborhood_column:
        neighborhoods = data[neighborhood_column].unique().tolist()
        selected_neighborhood_predict = st.selectbox('Neighborhoods', ['All'] + neighborhoods)
        if selected_neighborhood_predict != 'All':
            filtered_data = filtered_data[filtered_data[neighborhood_column] == selected_neighborhood_predict]
            display_data = True

    if display_data:
        st.title('Filtered Data')
        st.write(filtered_data.T)

with tab3:
    st.header("Settings")
    st.subheader('What type of data do you want to use to filter?')
    
    col1, col2 = st.columns(2)
    data_selected = None
    
    with col1:
        if st.button('Select Large Data'):
            st.session_state['data_file'] = 'merged_df.xlsx'
            st.session_state['data_selected'] = 'Large Data Selected'
            st.experimental_rerun()
    
    with col2:
        if st.button('Select Reduced Data'):
            st.session_state['data_file'] = 'all_predicted_buyers_2024_details.xlsx'
            st.session_state['data_selected'] = 'Reduced Data Selected'
            st.experimental_rerun()
    
    if 'data_selected' in st.session_state:
        st.success(st.session_state['data_selected'])

with tab4:
    st.header("About us")
    st.write("L'Avenir Holdings Inc. is a Real estate company which deals with building, buying and selling of properties such as lands, detached, semi-detached, town houses, apartments, condos, and waterfront/beach houses. We are located in Sarasota, Florida, USA.")

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

# # Step 4: Add 'Last Sale Year' column
# data['Last Sale Year'] = data['Last Sale Date'].dt.year
# data['Prior Sale Year'] = data['Prior Sale Date'].dt.year
# data['Year Built'] = data['Year Built'].astype('int64')

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
