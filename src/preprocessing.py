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


