
import pandas as pd


def load_raw_data(filepath):
    
    try:
        df = pd.read_csv(filepath)
        print(f" loaaded {len(df):,} rows and {len(df.columns)} columns")
        return df
        
    except FileNotFoundError:
        print(f"error no file found")
        return None
    except Exception as e:
        print(f"error loading file pls try again: {e}")
        return None


