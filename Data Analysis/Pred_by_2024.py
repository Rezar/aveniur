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


results = []
owner_names = filtered_df['Owner 1'].str.strip().str.lower().unique()

def predict_next_digit(owner_name_input, df):
    owner_name = owner_name_input.strip().lower()
    
    owner_data = df[df['Owner 1'].str.strip().str.lower() == owner_name]
    
    if owner_data.empty:
        return None
    
    min_year = owner_data['Last Sale Year'].min()
    max_year = owner_data['Last Sale Year'].max() 
    
    sequence = [(year in owner_data['Last Sale Year'].values) for year in range(min_year, max_year + 1)]
    
    if len(set(sequence)) <= 1:
        return None
    
    X = pd.DataFrame({'Year': range(min_year, max_year + 1)})
    y = sequence
    
    model = CatBoostRegressor(iterations=100, learning_rate=0.01, random_seed=42)
    model.fit(X, y)
    
    next_year = 2024
    next_digit = model.predict([[next_year]])
    
    return next_digit    


for owner_name in owner_names:
    prediction = predict_next_digit(owner_name, filtered_df)
    
    if prediction is not None and len(prediction) > 0:
        probability = np.round(prediction[0] * 100, 2)
    
        if probability > 80:
            results.append({
                'Owner Name': owner_name,
                'Probability': probability
            })


results_df = pd.DataFrame(results)

results_df = results_df.sort_values(by = 'Probability', ascending = False)

st.title('Property Buyer Prediction with Probabilities')

try:
    st.write(results_df)

except Exception as e:
    st.error(f"Error: {e}")