import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_and_clean_data(file_path):
    print(f"--- Attempting to load: {file_path} ---")
    # Using read_csv because your file in 'ls' had a .csv style name
    # If it fails, we try read_excel
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
