import pandas as pd


def load_raw_data(filepath):
    
    try:
        df = pd.read_csv(filepath)
        print(f" loaaded {len(df):,} rows and {len(df.columns)} columns")
        return df
        
