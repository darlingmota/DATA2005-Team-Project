import numpy as np
import pandas as pd

def get_real_countries_only(df):

    countries_only = df[df["iso_code"].notna()].copy()
    return countries_only
