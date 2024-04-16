import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

file_path = './cleaned_df.xlsx'

df = pd.read_excel(file_path)

df['Last Sale Year'] = df['Last Sale Date'].dt.year
df['Last Sale Year'] = df['Last Sale Year'].astype('Int64')

def plot_top_10_owners(df, selected_year):
    df_selected_year = df[df['Last Sale Year'] == selected_year]
    owner_freq = df_selected_year['Owner 1'].value_counts().head(10)

    fig, ax = plt.subplots()
    owner_freq.plot(kind='bar', ax=ax)
    ax.set_ylabel('Frequency')
    ax.set_xlabel('Owner')
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Top 10 Owners for Year {selected_year}')
    plt.tight_layout()
    st.pyplot(fig)

st.title('Top 10 Owners by Year')

df = df.dropna(subset=['Last Sale Year'])

unique_years = sorted(df['Last Sale Year'].unique(), reverse=True)
selected_year = st.selectbox('Select Year', unique_years)
plot_top_10_owners(df, selected_year)

