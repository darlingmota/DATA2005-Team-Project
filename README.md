# [Project Domain Name] - DATA 2005 Team Project

**Course:** DATA 2005 - Data-Centric Programming  
**Assessment:** Team Data Processing Project (20%)

## Team Members

| Name | Role | GitHub |
|------|------|--------|
| [Darling Mota] | Data Engineer | [@darlingmota] |
| [Titas Utrya] | Data Analyst | [@titas3012] |
| [Prosper Umeh] | Visualization Lead | [@pruber] |
| [Nischal Rana] | Documentation Lead | [@NischalRana29] |

## Project Description

This project processes the Our World in Data (OWID) World Energy Consumpiton dataset to analyse how the global energy mix has shifted between fossil fuels and low carbon sources. The pipeline loads the raw country level annual data, drops sparse indicators, filters to the modern year(2000+), engineers four energy mix share features, and produces a cleaned dataset ready for statistical analysis and visualization. Final outputs are exported in CSV and JSON formats. 

## Dataset

- **Name:** [World Energy Consumption]
- **Source:** [\[[Source URL](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)\]](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)
- **Size:** [~20,000+]
- **Format:** CSV/JSON

## Project Structure 2026

## Repository Structure 
DATA2005-TEAM-PROJECT/

|__ data/
| |__processed/
| | |-- .gitkeep
| | |__ owid-energy-clean.csv
| |__raw/
| | |-- .gitkeep
| | |__ oid-energy-data.csv

|__ outputs/
| |__ figures/
| | |__ .gitkeep
| |__ reports/
| | |__ .gitkeep

|__ src
| |-- __init__.py
| |-- analysis.py
| |-- data_loading.py
| |-- main.py
| |-- preprocessing.py
| |__ visualization.py

|__ LINCENSE

|__ README.md   <-- this file

## Setup

Requirements
- Python >= 3.12

Installation

## Data Acquisition
Kaggle
1. Go to https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption
2. Download World Energy Consumption.csv
3. Place it in data/raw/ and rename to owid-energy-data.csv 

## Usage

## Pipeline Overview

| Stage              | Module            | Function(s)            | What it does                           |  Rubric criterion     |
|--------------------|-------------------|------------------------|----------------------------------------|-----------------------|  
| 1. Load            | data_loading.py   | load_raw_data          | Reads raw CSV with error handling      |Data Loading           |
| 2. Validate        | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |   
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |
| "new customer ID"  | camelCase    | `newCustomerId`        | `newCustomerID`       |                       |


## Academic Integrity