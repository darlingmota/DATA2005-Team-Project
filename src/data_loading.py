
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
    
    missing_cols = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    cols_90pct_missing = (missing_cols > 90).sum()
    cols_50pct_missing = (missing_cols > 50).sum()
    
    print(f"Columns >50% missing: {cols_50pct_missing}")
    print(f"Columns >90% missing: {cols_90pct_missing}")
    
    return results


def show_info(df):
    
    
    print("\n Data Info")
    
    print(f"\nCountries/Regions: {df['country'].nunique()}")
    print(f"Sample countries: {', '.join(df['country'].unique()[:5])}")
    
    print(f"\nTime period: {df['year'].min()} to {df['year'].max()}")
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    print(f"\nNumeric columns: {len(numeric_cols)}")
    
    energy_cols = [col for col in df.columns if 'energy' in col or 'electricity' in col or 'consumption' in col]
    print(f"columns related to energy: {len(energy_cols)}")
    if energy_cols:
        print(f"  Examples: {', '.join(energy_cols[:5])}")


if __name__ == "__main__":
    df = load_raw_data("data/raw/owid-energy-data.csv")
    if df is not None:
        validate_data(df)
        show_info(df)