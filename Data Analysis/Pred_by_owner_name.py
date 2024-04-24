import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split


file_path = './cleaned_df.xlsx'
df = pd.read_excel(file_path)

df['Gross Bldg Area'] = df['Gross Bldg Area'].fillna(df['Gross Bldg Area'].mean())
df['Living Area'] = df['Living Area'].fillna(df['Living Area'].mean())
df = df.infer_objects()

df['Year Built'] = pd.to_datetime(df['Year Built'], errors='coerce')
df['Last Sale Date'] = pd.to_datetime(df['Last Sale Date'], errors='coerce')
df['Prior Sale Date'] = pd.to_datetime(df['Prior Sale Date'], errors='coerce')

df['Year Built'] = df['Year Built'].fillna(pd.Timestamp.max)
df['Last Sale Date'] = df['Last Sale Date'].fillna(pd.Timestamp.max)
df['Prior Sale Date'] = df['Prior Sale Date'].fillna(pd.Timestamp.max)

df['Last Sale Year'] = df['Last Sale Date'].dt.year
df['Last Sale Year'] = df['Last Sale Year'].astype('Int64')

df['Year Built'] = df['Year Built'].dt.year.astype('Int64')

df['Last Sale Month'] = df['Last Sale Date'].dt.month.astype('Int64')
df['Prior Sale Year'] = df['Prior Sale Date'].dt.year.astype('Int64')
df['Prior Sale Month'] = df['Prior Sale Date'].dt.month.astype('Int64')

df['Prop_Count'] = df['Owner 1'].map(df['Owner 1'].value_counts())

filtered_df = df[df['Prop_Count'] > 1]

filtered_df = filtered_df[filtered_df['Last Sale Year'] != 2262]


def predict_next_digit(owner_name_input, year_input, df):
    owner_name = owner_name_input.strip().lower()
    #print(owner_name)

    
    owner_data = df[df['Owner 1'].str.strip().str.lower() == owner_name]
    #print(owner_data)
    
    if owner_data.empty:
        st.error(f"No data found for owner: {owner_name_input}")
        return None
    
    min_year = owner_data['Last Sale Year'].min()
    max_year = int(year_input)   

    if max_year < 2024:
        st.warning(f"Please ensure year is 2024 or after.")
        return
        
    
    sequence = [(year in owner_data['Last Sale Year'].values) for year in range(min_year, max_year + 1)]
    
    X = pd.DataFrame({'Year': range(min_year, max_year + 1)})
    y = sequence
    
    model = CatBoostRegressor(iterations=100, learning_rate=0.1, random_seed=42)
    model.fit(X, y)
    
    
    next_year = max_year
    next_digit = model.predict([[next_year]])
    
    return next_year, next_digit


def main():
        
    st.title('Property Buyer Prediction')
    
    
    owner_name_input = st.text_input("Enter owner's name here:", value = "", 
    help = "Please ensure the requested owner owns more than 1 property")

    year_input = st.text_input("Enter desired year here:", value = "", 
    help = "Please ensure the requested year is 2024 or after for optimum results")
    
    if owner_name_input:
        try:
            next_year, next_digit = predict_next_digit(owner_name_input, year_input, filtered_df)
            probability = np.round(next_digit * 100, 2)
            
            if next_digit[0] > 0.7:
                will_buy = f'Yes, good chances with {str(probability[0])}% probability'
            else:
                will_buy = f'No, poor chances with {str(probability[0])}% probability'
            
            st.write(f"Will owner '{owner_name_input}' buy in year {next_year}: {will_buy}")
        
        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == '__main__':
    main()
