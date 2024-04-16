import pandas as pd
import re
import streamlit as st
import plotly.express as px

file_path = './SCPA Public.xlsx'

data = pd.read_excel(file_path)
data1 = data.dropna(subset=['Situs Zip Code', 'Last Sale Date']).copy()
data1['Situs Zip Code'] = data1['Situs Zip Code'].str.replace('-', '')
data1['Situs Zip Code'] = data1['Situs Zip Code'].str.replace('_', '')
data1['Situs Zip Code'] = data1['Situs Zip Code'].astype('int64')

# Read the second Excel file with lat and long columns
df2 = pd.read_excel('uszips.xlsx', usecols=['zip', 'lat', 'lng'])

# Merge the two DataFrames based on situs zip code column
merged_df = pd.merge(data1, df2,  left_on = 'Situs Zip Code', right_on='zip', how='left')


df = merged_df.dropna(subset=['Situs Zip Code', 'Last Sale Date']).copy()
df['Last Sale Date'] = pd.to_datetime(df['Last Sale Date'])
df['Last Sale Year'] = df['Last Sale Date'].dt.year


# Streamlit App
st.title('Florida Property Visualization')



assessed_value_slider = st.sidebar.slider('Assessed Value', float(df['Assessed Value'].min()), 
                                          float(df['Assessed Value'].max()), (float(df['Assessed Value'].min()), 
                                                                              float(df['Assessed Value'].max())))
last_sale_amount_slider = st.sidebar.slider('Last Sale Amount', float(df['Last Sale Amount'].min()), 
                                            float(df['Last Sale Amount'].max()), (float(df['Last Sale Amount'].min()), 
                                                                                  float(df['Last Sale Amount'].max())))
last_sale_year_slider = st.sidebar.slider('Last Sale Year', int(df['Last Sale Year'].min()), 
                                          int(df['Last Sale Year'].max()), (int(df['Last Sale Year'].min()), 
                                                                            int(df['Last Sale Year'].max())))

# Create dropdown for categorical column
owner_options = df['Owner 1'].unique().tolist()
selected_owner = st.sidebar.selectbox('Owner 1', options=owner_options)

# Filter the data based on user selection
filtered_df = df[(df['Assessed Value'] >= assessed_value_slider[0]) & (df['Assessed Value'] <= assessed_value_slider[1]) &
                 (df['Last Sale Amount'] >= last_sale_amount_slider[0]) & (df['Last Sale Amount'] <= last_sale_amount_slider[1]) &
                 (df['Last Sale Year'] >= last_sale_year_slider[0]) & (df['Last Sale Year'] <= last_sale_year_slider[1]) &
                 (df['Owner 1'] == selected_owner)]

# Plot map with dots
fig = px.scatter_mapbox(filtered_df, lat='lat', lon='lng', hover_name='Situs Address (Property Address)',
                        hover_data=['Assessed Value', 'Last Sale Amount', 'Last Sale Year'],
                        #size=10, 
                        zoom=5)

fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig)
