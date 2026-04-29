import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_real_countries_only(df):
    countries_only = df[df["iso_code"].notna()].copy()
    return countries_only

def aggregate_by_year(df, value_column="electricity_generation"):
    yearly = df.groupby("year")[value_column].agg(
        total="sum",
        mean="mean",
        median="median",
        std="std",
    ).reset_index()
    return yearly

def aggregate_by_decade(df, value_column="electricity_generation"):
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

    country_stats = country_stats.sort_values("total", ascending=False)
    return country_stats

def find_peak_year_per_country(df, value_column="electricity_generation"):
    # FIXED: remove rows where electricity_generation is missing
    valid_df = df.dropna(subset=[value_column]).copy()

    peak_idx = valid_df.groupby("country")[value_column].idxmax()

    peaks = valid_df.loc[peak_idx, ["country", "year", value_column]].copy()
    peaks = peaks.rename(columns={
        "year": "peak_year",
        value_column: "peak_value"
    })

    peaks = peaks.sort_values("peak_value", ascending=False).reset_index(drop=True)
    return peaks

def top_n_consumers(df, n=10, value_column="electricity_generation", year=None):
    if year is not None:
        one_year = df[df["year"] == year].copy()
        top = one_year.nlargest(n, value_column)
        top = top[["country", "year", value_column]]
    else:
        totals = df.groupby("country")[value_column].sum().reset_index()
        top = totals.nlargest(n, value_column)

    return top.reset_index(drop=True)

def detect_consumption_anomalies(df, value_column="electricity_generation", z_threshold=3.0):
    df = df.copy()

    country_mean = df.groupby("country")[value_column].transform("mean")
    country_std = df.groupby("country")[value_column].transform("std")

    df["z_score"] = np.where(
        country_std > 0,
        (df[value_column] - country_mean) / country_std,
        0.0,
    )

    anomalies = df[np.abs(df["z_score"]) > z_threshold].copy()
    anomalies = anomalies[["country", "year", value_column, "z_score"]]
    anomalies = anomalies.sort_values("z_score", key=np.abs, ascending=False)
    return anomalies.reset_index(drop=True)

def per_capita_normalisation(df, value_column="electricity_generation"):
    df = df.copy()

    values = df[value_column].to_numpy()
    population = df["population"].to_numpy()

    result = np.full_like(values, np.nan, dtype=float)
    valid = (population > 0) & ~np.isnan(population)
    result[valid] = values[valid] / population[valid]

    new_col = value_column + "_per_capita"
    df[new_col] = result
    return df

def zscore_across_countries(df, value_column="electricity_generation"):
    df = df.copy()

    year_mean = df.groupby("year")[value_column].transform("mean")
    year_std = df.groupby("year")[value_column].transform("std")

    df[value_column + "_zscore"] = np.where(
        year_std > 0,
        (df[value_column] - year_mean) / year_std,
        0.0,
    )
    return df

def energy_mix_shares(df):
    df = df.copy()

    sources = [
        "coal_electricity",
        "gas_electricity",
        "nuclear_electricity",
        "hydro_electricity",
        "renewables_electricity"
    ]

    source_matrix = df[sources].to_numpy()
    row_totals = np.nansum(source_matrix, axis=1)

    safe_totals = np.where(row_totals > 0,
