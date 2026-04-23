
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


def validate_data(df):
    
    results = {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_total': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum(),
        'countries': df['country'].nunique() if 'country' in df.columns else 0,
        'years': (df['year'].max() - df['year'].min() + 1) if 'year' in df.columns else 0,
    }
    
    print("\n Validation")
    print(f"Rows: {results['rows']:,}")
    print(f"Columns: {results['columns']}")
    print(f"Countries: {results['countries']}")
    print(f"Year range: {df['year'].min()} to {df['year'].max()}")
    print(f"Total missing values: {results['missing_total']:,}")
    print(f"Duplicate rows: {results['duplicates']}")
    
