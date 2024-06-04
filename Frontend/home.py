# def main():
#     st.write("# Home Page")
    
#     # Get the query parameters
#     query_params = st.query_params()
    
#     # Check if the 'authenticated' parameter is present and set to 'true'
#     if 'authenticated' in query_params and query_params['authenticated'][0] == 'true':
#         st.success("Login Successful")
#     else:
#         st.warning("Login failed")

# if _name_ == "_main_":
#     main()

import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import base64

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

st.title("L'Avenir Holdings inc Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["HOME", "VIEW", "HISTORY", "2024 PREDICTED BUYERS", "SETTINGS", "ABOUT"])

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
    numeric_data = pd.to_numeric(data[column_name], errors='coerce').dropna()
    if numeric_data.empty:
        return (0, 0)
    min_value = numeric_data.min()
    max_value = numeric_data.max()
    return (int(min_value), int(max_value))

st.logo("images/lavenir.PNG")
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
    # data = data.dropna(subset=['lat', 'lng', 'Situs Zip Code', 'Last Sale Date', 'Prior Sale Date', 'Year Built'])
    
    col1, col2 = st.columns(2)

    with col1:
        state = ["FL","MA"]
        selected_buyer = st.selectbox('State', ['All'] + state)

    with col2:
        county = ["Sarasota","Sulffolk", "Nor"]
        selected_neighborhood = st.selectbox('County/Township', ['All'] + county)
        agree = st.checkbox("I agree")

if agree:
    st.write("Great!")

    # st.checkbox(label, value=False, key=None, help=None, on_change=None, args=None, kwargs=None, *, disabled=False, label_visibility="visible")


with tab2:
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
    st.map(gdf.rename(columns={'lng': 'longitude', 'lat': 'latitude'}), zoom=8)

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
    st.map(gdf_filtered.rename(columns={'lng': 'longitude', 'lat': 'latitude'}), zoom=8)

    if selected_buyer != 'All':
        filtered_data = filtered_data[filtered_data[owner_column] == selected_buyer]

    st.title('Selected Price Range')
    st.write(f'Min Price: {selected_price[0]:,} - Max Price: {selected_price[1]:,}')

    st.title('Filtered Data')
    st.dataframe(filtered_data.T, width=1000, height=600)

with tab3:
    st.subheader("What do you want to search today?")
    filter_options = ["Buyers", "Years", "Price", neighborhood_column]
    selected_filter = st.radio("Select a filter option:", filter_options, horizontal=True)
    display_data = False
    filtered_data = data  # Initializing `filtered_data` with the entire dataset

    if selected_filter == "Buyers":
        buyers_predict = data[owner_column].unique().tolist()
        selected_buyer_predict = st.selectbox('Buyers', ['All'] + buyers_predict)
        if selected_buyer_predict != 'All':
            filtered_data = filtered_data[filtered_data[owner_column] == selected_buyer_predict]
        display_data = True

    elif selected_filter == "Years":
        year_min, year_max = get_slider_ranges(data, 'Last Sale Year')
        selected_year_predict = st.slider('Years', year_min, year_max, (year_min, year_max))
        filtered_data = filter_data_based_on_year(data, selected_year_predict)
        display_data = True

    elif selected_filter == "Price":
        min_price, max_price = get_slider_ranges(data, 'Last Sale Amount')
        selected_price_predict = st.slider('Prices', min_price, max_price, (min_price, max_price))
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
        st.dataframe(filtered_data.T, width=1000, height=600)

with tab4:
    st.subheader("Predicted Buyers for 2024")

    # if st.session_state['data_file'] != 'all_2024_details.xlsx':
    #     st.warning("Please switch to the reduced data file in the Settings tab to use this feature.")
    # else:
    reduced_data = load_data('all_2024_details.xlsx')

    owners = reduced_data['Owner'].unique().tolist() if 'Owner' in reduced_data.columns else []
    types = reduced_data['Type'].dropna().unique().tolist() if 'Type' in reduced_data.columns else []

    selected_owner = st.selectbox('Owner', ['All'] + owners)
    selected_type = st.selectbox('Type', ['All'] + types)

    if 'Owner' in reduced_data.columns and 'Type' in reduced_data.columns:
        if selected_owner != 'All':
            reduced_data = reduced_data[reduced_data['Owner'] == selected_owner]
        if selected_type != 'All':
            reduced_data = reduced_data[reduced_data['Type'] == selected_type]

        st.title('Filtered Data')

        # Check if both owner and type are "All"
        if selected_owner == 'All' and selected_type == 'All':
            st.warning("Please select to see predicted buyers")  # Display all data
        else:
            if reduced_data.shape[0] == 1:
                # Display the map and data vertically
                row = reduced_data.iloc[0]
                latitude = float(row['lat'].split(',')[0].strip())  # Extract latitude and convert to float
                longitude = float(row['lng'].split(',')[0].strip())  # Extract longitude and convert to float
                map_data = pd.DataFrame([[latitude, longitude]], columns=['latitude', 'longitude'])
                st.map(map_data, zoom=8)
                st.dataframe(row, width=1000, height=600)
            else:
                # Display the data horizontally
                for index, row in reduced_data.iterrows():
                    pcol1, pcol2 = st.columns(2)
                    with pcol1:
                        # Display the map
                        latitude = float(row['lat'].split(',')[0].strip())  # Extract latitude and convert to float
                        longitude = float(row['lng'].split(',')[0].strip())  # Extract longitude and convert to float
                        map_data = pd.DataFrame([[latitude, longitude]], columns=['latitude', 'longitude'])
                        st.map(map_data, zoom=8)
                        
                    with pcol2:
                        st.dataframe(row, width=600, height=400)

with tab5:
    st.header("Settings")
    st.subheader('What type of data do you want to use to filter?')
    
    col1, col2 = st.columns(2)
    data_selected = None
    
    with col1:
        if st.button('Select Large Data'):
            st.session_state['data_file'] = 'merged_df.xlsx'
            st.session_state['data_selected'] = 'Large Data Selected'
            st.rerun()
    
    with col2:
        if st.button('Select Reduced Data'):
            st.session_state['data_file'] = 'all_2024_details.xlsx'
            st.session_state['data_selected'] = 'Reduced Data Selected'
            st.rerun()
    
    if 'data_selected' in st.session_state:
        st.success(st.session_state['data_selected'])

with tab6:
    # st.header("About us")
    st.image("images/lavenir.PNG")
    st.write("L'Avenir Holdings Inc. stands as a beacon in the real estate landscape of Sarasota, Florida, USA. Specializing in the art of property transactions, our expertise spans the spectrum from sprawling lands to cozy apartments, from charming townhouses to luxurious waterfront retreats. \n\nOur dedication lies in crafting seamless experiences for both buyers and sellers, ensuring every transaction is not just a deal, but a journey towards realizing dreams and aspirations. With an unwavering commitment to excellence, we navigate the complexities of the real estate market with finesse, guided by a vision of shaping tomorrow's landscapes today. \n\nAt L'Avenir Holdings Inc., every property is not just a structure; it's a canvas waiting to be adorned with memories and possibilities. Whether it's finding the perfect home to settle into or unlocking the potential of a lucrative investment opportunity, we are the trusted partner guiding you every step of the way. With integrity, innovation, and a passion for the extraordinary, we redefine what it means to turn dreams into reality in the realm of real estate.")