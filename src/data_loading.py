 
import pandas as pd
 
 
def load_raw_data(filepath):
    
    try:
        df = pd.read_csv(filepath)
        print(f"loaded {len(df)} rows and {len(df.columns)} columns from {filepath}")
        return df
    
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
