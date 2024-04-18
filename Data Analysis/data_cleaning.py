# importing libraries
import pandas as pd
import re

# defining function to clean dataset
def clean_data(df):
    
    # trying to reduce Owner 1, Owner 2 and Owner 3 col values
    # checking if Owner 1, Owner 2, Owner 3 values in the same row are equal
    # if same, replace with ''
    same_values_mask = (df['Owner 1'] == df['Owner 2']) & (df['Owner 2'] == df['Owner 3'])
    df.loc[same_values_mask, ['Owner 2', 'Owner 3']] = ''

    # get rid of whitespace
    df['Owner 1'] = df['Owner 1'].str.strip()
    df['Owner 2'] = df['Owner 2'].str.strip()
    df['Owner 3'] = df['Owner 3'].str.strip()

    # dropping columns not needed for current analysis
    df = df.drop(columns=['Owner 2', 'Owner 3'])
    
    df = df.drop(columns=['Mailing Address 1', 'Mailing Address 2', 'Mailing City',	
                          'Mailing State', 'Mailing Zip Code', 'Mailing Country'])
    
    df = df.drop(columns=['Situs State', 'Property Use Code', 'Neighborhood', 'Subdivision', 
                          'Taxing District', 'Municipality', 'Waterfront Code'])
    
    df = df.drop(columns=['Homestead Exemption (YES or NO)', 'Homestead Exemption Grant Year', 'Zoning', 
                          'Parcel Desc 1', 'Parcel Desc 2', 'Parcel Desc 3', 'Parcel Desc 4'])
    
    df = df.drop(columns=['Pool (YES or NO)', 'Link to Property Detail Page', 'Value Data Source', 
                          'Parcel Characteristics Data', 'Status'])


    # converting float datatype columns to datetime
    df['Year Built'] = pd.to_datetime(df['Year Built'], format='%Y', errors='coerce')
    df['Last Sale Date'] = pd.to_datetime(df['Last Sale Date'], format='%m/%d/%Y', errors='coerce')
    df['Prior Sale Date'] = pd.to_datetime(df['Prior Sale Date'], format='%m/%d/%Y', errors='coerce')


    # done checking all columns
    # returning cleaned df
    return df

