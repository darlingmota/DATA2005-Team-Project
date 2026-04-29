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

def aggregate_by_country(df, 
