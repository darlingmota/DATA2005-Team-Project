import pandas as pd
import numpy as np


def drop_sparse_columns(df, threshold=70):
    
    
    keep_always = ['country', 'year', 'iso_code']
    
    missing_pct = (df.isnull().sum() / len(df) * 100)
    cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
    
    
    cols_to_drop = [col for col in cols_to_drop if col not in keep_always]
    
    before_cols = len(df.columns)
    df = df.drop(columns=cols_to_drop)
    after_cols = len(df.columns)
    
    print(f"dropped {before_cols - after_cols} sparse columns (>{threshold}% missing)")
    return df


def filter_modern_data(df, min_year=2000):
    
    before = len(df)
    df = df[df['year'] >= min_year]
    removed = before - len(df)
    
    print(f"filtered to {min_year}+: removed {removed:,} rows")
    return df


def remove_duplicates(df):
    dupes = df.duplicated().sum()
    if dupes > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"removed {dupes} duplicate rows")
    return df


def handle_missing(df):
    
    key_cols = ['electricity_generation', 'fossil_fuel_consumption', 'renewables_electricity']
    key_cols = [col for col in key_cols if col in df.columns]
    
    if not key_cols:
        print("warning: No key energy columns found, skipping missing value filter")
        return df
    
    before = len(df)
    df = df.dropna(subset=key_cols, how='any')
    removed = before - len(df)
    
    if removed > 0:
        print(f"removed {removed:,} rows missing key energy columns")
    return df


def engineer_features(df):
    if 'renewables_electricity' in df.columns and 'electricity_generation' in df.columns:
        df['renewable_elec_share'] = (df['renewables_electricity'] / df['electricity_generation'] * 100).round(2)
    if 'fossil_fuel_consumption' in df.columns and 'renewables_consumption' in df.columns:
        df['fossil_renewable_ratio'] = (df['fossil_fuel_consumption'] / (df['renewables_consumption'] + 1)).round(2)
    
    if 'coal_electricity' in df.columns and 'electricity_generation' in df.columns:
        df['coal_elec_share'] = (df['coal_electricity'] / df['electricity_generation'] * 100).round(2)
    
    if 'nuclear_electricity' in df.columns and 'electricity_generation' in df.columns:
        df['nuclear_elec_share'] = (df['nuclear_electricity'] / df['electricity_generation'] * 100).round(2)
    
    print("created features: renewable_elec_share, fossil_renewable_ratio, coal_elec_share, nuclear_elec_share")
    return df


def select_key_columns(df):
    keep = ['country', 'year', 'iso_code', 'population', 'gdp']
    
    primary = ['electricity_generation', 'primary_energy_consumption']
    sources = [
        'fossil_fuel_consumption', 'coal_consumption', 'gas_consumption', 'oil_consumption',
        'renewables_consumption', 'solar_consumption', 'wind_consumption', 'hydro_consumption',
        'nuclear_consumption', 'biofuel_consumption'
    ]
    electricity = [
        'fossil_electricity', 'coal_electricity', 'gas_electricity', 'oil_electricity',
        'renewables_electricity', 'solar_electricity', 'wind_electricity', 'hydro_electricity',
        'nuclear_electricity', 'biofuel_electricity'
    ]
    
