import pandas as pd
from pathlib import Path
from data_loading import load_raw_data, validate_data, show_info
from preprocessing import preprocess


def summarise(df_raw, df_clean):
    
    print("\nSummary")
    
    
    print(f"\before: {len(df_raw):,} rows × {len(df_raw.columns)} columns")
    print(f"after:  {len(df_clean):,} rows × {len(df_clean.columns)} columns")
    print(f"\rows removed: {len(df_raw) - len(df_clean):,}")
    print(f"Columns reduced: {len(df_raw.columns)} → {len(df_clean.columns)}")
    
    print("\key features:")
    print("  Core: country, year, population, gdp")
    print("  Energy sources: fossil, coal, gas, oil, renewables, nuclear")
    print("  Electricity: by source (coal, gas, solar, wind, nuclear, etc.)")
    print("  Engineered: renewable_elec_share, coal_elec_share, nuclear_elec_share")
    
    countries = df_clean['country'].nunique()
    years_min, years_max = df_clean['year'].min(), df_clean['year'].max()
    print(f"\nCOVERAGE:")
    print(f"  Countries: {countries}")
    print(f"  Years: {years_min}-{years_max}")
    



def export_data(df, output_file):
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    size_mb = Path(output_file).stat().st_size / (1024*1024)
    print(f"exported to: {output_file}")
    print(f"size: {size_mb:.1f} MB")


def main():
    
    
    print("\nour world in data energy pipeline")
    
    
    raw_file = "data/raw/owid-energy-data.csv"
    clean_file = "data/processed/owid-energy-clean.csv"
    print("\nload")
    
    df_raw = load_raw_data(raw_file)
    
    if df_raw is None:
        print("failed to load. Check file path.")
        return False
    
