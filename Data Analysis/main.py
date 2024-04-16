# importing libraries
import pandas as pd
import re
import matplotlib.pyplot as plt
from data_cleaning import clean_data

# define function to return clean df
def process_data(file_path, subset=False):
    df = pd.read_excel(file_path)
    if subset:
        df = df.sample(frac = 0.1, random_state = 24)
    
    cleaned_df = clean_data(df)
    return cleaned_df

# define file path
file_path = './SCPA Public.xlsx'

# use function to create clean dataset called processed df
processed_df = process_data(file_path, subset=True)

#print(processed_df.head(20))
