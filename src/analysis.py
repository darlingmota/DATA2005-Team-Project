import numpy as np
import pandas as pd

def get_real_countries_only(df):

    countries_only = df[df["iso_code"].notna()].copy()
    return countries_only

def aggregate_by_year(df, value_column="electricity_generation"):

    # Group by year and calculate a few summary stats in one go
    yearly = df.groupby("year")[value_column].agg(
        total="sum",
        mean="mean",
        median="median",
        std="std",
    ).reset_index()
    return yearly
