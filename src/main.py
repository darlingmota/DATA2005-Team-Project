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
