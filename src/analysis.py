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

