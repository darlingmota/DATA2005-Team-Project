import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

def run_master_pipeline():
    print("--- Starting Master Data Pipeline (10 Graphs) ---")
    

    try:
        df = pd.read_excel('World Energy Consumption.xlsx')
        print(f"Dataset Loaded: {df.shape[0]} rows found.")
    except Exception as e:
        print(f"Critical Error: Could not read file. {e}")
        return

   
    world_df = df[df['country'] == 'World'].copy()
    regions = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    region_df = df[df['country'].isin(regions)].copy()
    country_df = df[df['iso_code'].notna()].copy()

    
    valid_data = country_df.dropna(subset=['gdp', 'renewables_share_energy'])
    latest_valid_year = int(valid_data['year'].max())
    print(f"Using data from {latest_valid_year} for comparative plots.")


    print("Generating Graphs 1-6...")
    
    
    plt.figure(figsize=(10, 5))
    plt.stackplot(world_df['year'], world_df['fossil_fuel_consumption'], world_df['renewables_consumption'], 
                  labels=['Fossil', 'Renewables'], colors=['#333333', '#27ae60'], alpha=0.8)
    plt.title('Global Energy Transition'); plt.legend(); plt.savefig('1_transition.png'); plt.close()

    
    plt.figure(figsize=(8, 6))
    sns.heatmap(world_df[['gdp', 'population', 'fossil_fuel_consumption', 'renewables_consumption']].corr(), annot=True, cmap='mako')
    plt.savefig('2_heatmap.png'); plt.close()

   
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=world_df[world_df['year'] >= 2000], x='year', y='solar_consumption', label='Solar')
    sns.lineplot(data=world_df[world_df['year'] >= 2000], x='year', y='wind_consumption', label='Wind')
    plt.savefig('3_solar_wind.png'); plt.close()

  
    top_5 = country_df[country_df['year'] == latest_valid_year].nlargest(5, 'primary_energy_consumption')
    mix = top_5.melt(id_vars='country', value_vars=['coal_consumption', 'gas_consumption', 'renewables_consumption'])
    plt.figure(figsize=(10, 5))
    sns.barplot(data=mix, x='country', y='value', hue='variable'); plt.savefig('4_top5.png'); plt.close()

    
    scat = country_df[(country_df['year'] == latest_valid_year) & (country_df['gdp'] > 0) & (country_df['low_carbon_electricity'] > 0)]
    plt.figure(figsize=(8, 5))
    sns.regplot(data=scat, x='gdp', y='low_carbon_electricity', scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
