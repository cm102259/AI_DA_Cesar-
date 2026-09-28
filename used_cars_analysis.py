import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------
# 1) Load data
# -----------------------------------------------------------
DATA_PATH = os.path.join('Data', 'used_cars_data.csv')
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# -----------------------------------------------------------
# 2) Basic cleaning
# -----------------------------------------------------------
# Keep a copy of the original
clean_df = df.copy()

# Remove duplicates if any
clean_df = clean_df.drop_duplicates().copy()

# Clean numeric columns that include units

def extract_numeric(text):
    if pd.isna(text):
        return None
    text = str(text).strip()
    match = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', text)
    if match:
        return float(match.group(0))
    return None

clean_df['Kilometers_Driven'] = pd.to_numeric(clean_df['Kilometers_Driven'], errors='coerce')
clean_df['Year'] = pd.to_numeric(clean_df['Year'], errors='coerce')
clean_df['Price'] = pd.to_numeric(clean_df['Price'], errors='coerce')
clean_df['Mileage'] = clean_df['Mileage'].apply(extract_numeric)
clean_df['Engine'] = clean_df['Engine'].apply(extract_numeric)
clean_df['Power'] = clean_df['Power'].apply(extract_numeric)
clean_df['Seats'] = pd.to_numeric(clean_df['Seats'], errors='coerce')

# Parse New_Price to numeric if it contains lakhs
clean_df['New_Price'] = clean_df['New_Price'].apply(lambda x: extract_numeric(x))

# Remove rows with missing target
clean_df = clean_df.dropna(subset=['Price']).copy()

# -----------------------------------------------------------
# 3) Plot 1: Price vs Year
# -----------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=clean_df, x='Year', y='Price', alpha=0.7, color='royalblue')
plt.title('Insight 1: Relación entre año del auto y precio de venta')
plt.xlabel('Año del vehículo')
plt.ylabel('Precio (Lakh)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'insight_1_price_vs_year.png'), dpi=200)
plt.close()

# -----------------------------------------------------------
# 4) Plot 2: Price by Fuel Type
# -----------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.boxplot(data=clean_df, x='Fuel_Type', y='Price', palette='Set2')
plt.title('Insight 2: Precio por tipo de combustible')
plt.xlabel('Tipo de combustible')
plt.ylabel('Precio (Lakh)')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'insight_2_price_by_fuel.png'), dpi=200)
plt.close()

# -----------------------------------------------------------
# 5) Plot 3: Average price by city
# -----------------------------------------------------------
city_avg = clean_df.groupby('Location', as_index=False)['Price'].mean().sort_values('Price', ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(data=city_avg, x='Price', y='Location', palette='viridis')
plt.title('Insight 3: Precio promedio por ciudad')
plt.xlabel('Precio promedio (Lakh)')
plt.ylabel('Ciudad')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'insight_3_price_by_city.png'), dpi=200)
plt.close()

# -----------------------------------------------------------
# 6) Print summary insights
# -----------------------------------------------------------
print('Dataset limpio y cargado correctamente.')
print('Filas finales:', len(clean_df))
print('Columnas:', list(clean_df.columns))
print('\nInsight 1: Precio promedio por año del auto')
print(clean_df.groupby('Year')['Price'].mean().sort_values(ascending=False).head())
print('\nInsight 2: Precio promedio por tipo de combustible')
print(clean_df.groupby('Fuel_Type')['Price'].mean().sort_values(ascending=False))
print('\nInsight 3: Precio promedio por ciudad')
print(city_avg.head(10))

print('\nGráficos guardados en la carpeta output/')
