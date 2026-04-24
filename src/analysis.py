import numpy as np
import pandas as pd

def get_real_countries_only(df):

    countries_only = df[df["iso_code"].notna()].copy()
    return countries_only

# Task 1: Resampling 
def aggregate_by_year(df, value_column="electricity_generation"):
    
    # Group by year and calculate a few summary stats in one go
    yearly = df.groupby("year")[value_column].agg(
        total="sum",
        mean="mean",
        median="median",
        std="std",
    ).reset_index()
    return yearly

def aggregate_by_decade(df, value_column="electricity_generation"):
    
    # Create a decade column using integer division 
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10

    decade_stats = df.groupby("decade")[value_column].agg(
        total="sum",
        mean="mean",
        std="std",
    ).reset_index()
    return decade_stats

def aggregate_by_country(df, value_column="electricity_generation"):

    country_stats = df.groupby("country")[value_column].agg(
        total="sum",
        mean="mean",
        min="min",
        max="max",
        std="std",
    ).reset_index()
    # Sort biggest first 
    country_stats = country_stats.sort_values("total", ascending=False)
    return country_stats

# Task 2: Detect peak consumption periods
def find_peak_year_per_country(df, value_column="electricity_generation"):

    # idxmax gives the index of the max row inside each group
    peak_idx = df.groupby("country")[value_column].idxmax()
    # Drop groups where countrys had missing values
    peak_idx = peak_idx.dropna()

    peaks = df.loc[peak_idx, ["country", "year", value_column]].copy()
    peaks = peaks.rename(columns={"year": "peak_year",
                                value_column: "peak_value"})
    peaks = peaks.sort_values("peak_value", ascending=False).reset_index(drop=True)
    return peaks

def top_n_consumers(df, n=10, value_column="electricity_generation",
                    year=None):

    if year is not None:
        # Filter to one year
        one_year = df[df["year"] == year].copy()
        top = one_year.nlargest(n, value_column)
        top = top[["country", "year", value_column]]
    else:
        # Sum across all years then take the biggest
        totals = df.groupby("country")[value_column].sum().reset_index()
        top = totals.nlargest(n, value_column)

    return top.reset_index(drop=True)
                        
def detect_consumption_anomalies(df, value_column="electricity_generation",
                                z_threshold=3.0):
    
    df = df.copy()

   # Country mean and std
    country_mean = df.groupby("country")[value_column].transform("mean")
    country_std = df.groupby("country")[value_column].transform("std")

    # Calculate z-score: (value - mean) / std
    # Used np.where because some countries have zero std and that breaks division
    df["z_score"] = np.where(
        country_std > 0,
        (df[value_column] - country_mean) / country_std,
        0.0,
    )
                                    
  # Keep only the anomalies
    anomalies = df[np.abs(df["z_score"]) > z_threshold].copy()
    anomalies = anomalies[["country", "year", value_column, "z_score"]]
    anomalies = anomalies.sort_values("z_score", key=np.abs, ascending=False)
    return anomalies.reset_index(drop=True)

# Task 3: Normalise and transform metrics
def per_capita_normalisation(df, value_column="electricity_generation"):

    df = df.copy()

 # NumPy divide with 'where' argument avoids division by zero or by NaN
    values = df[value_column].to_numpy()
    population = df["population"].to_numpy()

    # Make an output array full of NaN, then fill where population is valid
    result = np.full_like(values, np.nan, dtype=float)
    valid = (population > 0) & ~np.isnan(population)
    result[valid] = values[valid] / population[valid]

    new_col = value_column + "_per_capita"
    df[new_col] = result
    return df


def zscore_across_countries(df, value_column="electricity_generation"):

    df = df.copy()

    # Mean and std across all countries each year
    year_mean = df.groupby("year")[value_column].transform("mean")
    year_std = df.groupby("year")[value_column].transform("std")

    # z-score calculation
    df[value_column + "_zscore"] = np.where(
        year_std > 0,
        (df[value_column] - year_mean) / year_std,
        0.0,
    )
    return df

def energy_mix_shares(df):

    df = df.copy()

    # Stack the five source columns into one 2D array 
    sources = ["coal_electricity", "gas_electricity", "nuclear_electricity",
            "hydro_electricity", "renewables_electricity"]
    source_matrix = df[sources].to_numpy()

    # Total generation per row 
    # use np.nansum so missing values are treated as zero in the total
    row_totals = np.nansum(source_matrix, axis=1)

    safe_totals = np.where(row_totals > 0, row_totals, np.nan)
    shares = source_matrix / safe_totals[:, None]

    # Put the results back as new columns
    for i, source in enumerate(sources):
        share_name = "share_" + source.replace("_electricity", "")
        df[share_name] = shares[:, i]

    return df
    

# Task 4: Summary statistics using NumPy
def summary_statistics(df, value_column="electricity_generation"):
    
    values = df[value_column].to_numpy()

    # np.nanpercentile computes multiple percentiles in one vectorised call
    percentiles = np.nanpercentile(values, [25, 50, 75, 95])

    stats = {
        "mean": np.nanmean(values),
        "median": np.nanmedian(values),
        "std": np.nanstd(values),
        "variance": np.nanvar(values),
        "min": np.nanmin(values),
        "max": np.nanmax(values),
        "percentile_25": percentiles[0],
        "percentile_50": percentiles[1],
        "percentile_75": percentiles[2],
        "percentile_95": percentiles[3],
        "n_observations": int(np.sum(~np.isnan(values))),
    }
    return stats


def correlation_matrix(df, columns=None):

    if columns is None:
        columns = ["electricity_generation", "gdp", "population",
                "per_capita_electricity", "fossil_share_elec",
                "renewable_elec_share", "nuclear_share_elec"]

    # Keep only columns that actually exist 
    columns = [c for c in columns if c in df.columns]

    return df[columns].corr()

# Runs the whole analysis in one call
def run_full_analysis(df, value_column="electricity_generation"):
    
    # Only look at real countries 
    countries = get_real_countries_only(df)

    results = {
        "yearly": aggregate_by_year(countries, value_column),
        "by_decade": aggregate_by_decade(countries, value_column),
        "by_country": aggregate_by_country(countries, value_column),
        "peak_year_per_country": find_peak_year_per_country(countries,
                                                            value_column),
        "top_10_all_time": top_n_consumers(countries, n=10,
                                        value_column=value_column),
        "top_10_latest_year": top_n_consumers(
            countries, n=10, value_column=value_column,
            year=int(countries["year"].max())
        ),
        "anomalies": detect_consumption_anomalies(countries, value_column),
        "per_capita": per_capita_normalisation(countries, value_column),
        "zscore_by_year": zscore_across_countries(countries, value_column),
        "energy_mix": energy_mix_shares(countries),
        "summary": summary_statistics(countries, value_column),
        "correlations": correlation_matrix(countries),
    }

    return results

if __name__ == "__main__":
    # preprocessing.py will pass the cleaned df in
    print("Running analysis.py self-test...")
    # Dataset
    test_df = pd.read_excel("owid-energy-clean.xlsx")
    print(f"Loaded {len(test_df)} rows.")

    results = run_full_analysis(test_df)

    print("\n--- Summary Statistics (electricity_generation) ---")
    for key, value in results["summary"].items():
        print(f"  {key:20s}: {value:,.2f}")

    print("\n--- Top 10 Consumers ---")
    print(results["top_10_all_time"].to_string(index=False))

    print("\n--- Top 5 Anomalies Found ---")
    print(results["anomalies"].head().to_string(index=False))

    print("\nAnalysis complete.")
