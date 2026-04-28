# World Energy Consumption Analysis - DATA 2005 Team Project

**Course:** DATA 2005 - Data-Centric Programming  
**Assessment:** Team Data Processing Project (20%)

## Team Members

| Name | Role | GitHub |
|------|------|--------|
| [Darling Mota] | Data Engineer | [@darlingmota] (https://github.com/darlingmota) |
| [Titas Utrya] | Data Analyst | [@titas3012] (https://github.com/Titas3012) |
| [Prosper Umeh] | Visualization Lead | [@pruber] (https://github.com/Pruber) |
| [Nischal Rana] | Documentation Lead | [@NischalRana29] (https://github.com/NischalRana29) |

## Project Description

This project analyses how the global energy mix has changed between fossil fuels and low-carbon sources by processing the Our World in Data (OWID) World Energy Consumption dataset. The pipeline creates a cleaned dataset that is ready for statistical analysis and visualisation after loading the raw country-level annual data, removing sparse indicators, filtering to the most recent years (2000+), and engineering four energy mix share features. The final results are exported in JSON and CSV formats. 

## Dataset

- **Name:** [World Energy Consumption]
- **Source:** [Kaggle] [\[[Source URL](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)\]](https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption)
- **Size:** [~20,000+]
- **Format:** CSV

The raw dataset contains a wide range of energy indicators including total consumption, source-specific consumption (coal, gas, oil, renewables, nuclear, etc.), electricity generation by source, per-capita measures, and economic context (GDP, population). Many indicators are sparsely populated for earlier years, which motivates the cleaning steps in our pipeline.

## Pipeline Overview

The project is organised as four cooperating modules in `src/`:

**1. Data Loading (`data_loading.py`)** — Reads the raw CSV, runs structural validation (row/column counts, missing-value summary, duplicate detection, country and year coverage), and reports a high-level overview of the dataset.

**2. Preprocessing (`preprocessing.py`)** — Drops columns with more than 70% missing values, filters to the modern era (year ≥ 2000), removes exact duplicates, removes rows missing the key energy columns, engineers four derived features (`renewable_elec_share`, `coal_elec_share`, `nuclear_elec_share`, `fossil_renewable_ratio`), selects a focused subset of relevant columns, and forward/backward fills remaining gaps within each country.

**3. Analysis (`analysis.py`)** — Computes summary statistics, yearly/decadal/country aggregations, per-capita normalisation, z-score standardisation, energy-mix shares, peak-year detection, top-N consumers, anomaly detection (z-score > 3), and a correlation matrix across the main indicators. Most aggregations use pandas `groupby` with vectorised NumPy operations underneath.

**4. Visualization (`visualization.py`)** — Creates a well chosen collection of five figures, each employing a different chart format and presenting a different analytical aspect from the dataset: the global fossil-vs-renewables transition (stackplot), the energy mix of the top-five consumer countries (grouped bar), the regional distribution of renewables share in electricity (violin), the statistical shift in carbon intensity between 2000 and 2021 (KDE), and The varied energy-per-capita patterns of the world's regions (faceted line). Built with matplotlib and seaborn, reading from the raw OWID CSV so that pre-2000 data remains available for historical context.


## Repository Structure 

```
DATA2005-TEAM-PROJECT/
├── data/
│   ├── raw/
│   │   ├── .gitkeep
│   │   └── owid-energy-data.csv                    
│   └── processed/
│       ├── .gitkeep
│       └── owid-energy-clean.csv                   
├── outputs/
│   ├── figures/                                    
│   │   ├── .gitkeep
│   │   ├── 1_transition.png
│   │   ├── 4_top5.png
│   │   ├── 6_violin.png
│   │   ├── 7_carbon_kde.png
│   │   └── 9_facetgrid.png
│   └── reports/                                   
│       └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_loading.py                           
│   ├── preprocessing.py                           
│   ├── analysis.py                                 
│   ├── visualization.py                            
│   └── main.py                                     
├── LICENSE
└── README.md
``` 

## Setup
### Requirements

- Python >= 3.12
- pandas
- numpy
- matplotlib
- seaborn
- openpyxl

### Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/darlingmota/DATA2005-Team-Project.git
cd DATA2005-TEAM-PROJECT
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows
pip install pandas numpy matplotlib seaborn openpyxl
```


### Data Acquisition

Kaggle
1. Go to https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption
2. Download World Energy Consumption.csv
3. Place it in data/raw/ and rename to owid-energy-data.csv 

## Usage
### Run the full data pipeline

From the project root, run the main pipeline to load, validate, clean, and export the dataset:

```bash
python src/main.py
```

This reads `data/raw/owid-energy-data.csv` and writes `data/processed/owid-energy-clean.csv`.

### Run the analysis module

```bash
python src/analysis.py
```

Computes summary statistics, anomaly detection, top-N consumers, and aggregations on the cleaned dataset, printing key results to the console.

### Generate the visualization

```bash
python src/visualization.py
```

Produces a set of figures saved to `outputs/figures/` as PNG files, including the global energy transition, the energy mix of the top-five consumers, the regional distribution of renewables, the carbon-intensity distribution shift, and energy per capita by region.


## Output files 
| File | Description |
|------|-------------|
| `data/processed/owid-energy-clean.csv` | Cleaned dataset, post-2000, with engineered features |
| `outputs/figures/1_transition.png` | Global fossil vs renewables consumption over time |
| `outputs/figures/4_top5.png` | Energy mix of the top-5 consumer countries |
| `outputs/figures/6_violin.png` | Regional distribution of renewables share in electricity |
| `outputs/figures/7_carbon_kde.png` | Carbon-intensity density: 2000 vs 2021 |
| `outputs/figures/9_facetgrid.png` | Energy per capita by region, faceted over time |


## Sample Outputs

A selection of figures produced by `visualization.py`. The full set lives in `outputs/figures/`.

### Global Energy Transition

The headline finding: global fossil-fuel consumption has continued to grow alongside renewables. Renewables are catching up but absolute fossil consumption has not yet declined.

<p align="center">
    <img src="outputs/figures/1_transition.png" alt="Global Energy Transition stackplot" width="700"/>
</p>

### Renewables Share of Electricity by Region

Distributions of renewables share across the post-2015 period. South America stands out at roughly 70% renewables, while most other regions cluster between 20% and 35%.

<p align="center">
    <img src="outputs/figures/6_violin.png" alt="Regional renewables share violin plot" width="700"/>
</p>

### Energy Mix of Top-5 Consumers

The five largest energy consumers and how their mix differs. China is heavily coal-dependent, the US leans on gas, and renewables remain a small share for all five.

<p align="center">
    <img src="outputs/figures/4_top5.png" alt="Top 5 consumer countries energy mix" width="700"/>
</p>


## Engineered Features

| Feature | Definition |
|---------|------------|
| `renewable_elec_share` | Renewables as % of total electricity generation |
| `coal_elec_share` | Coal as % of total electricity generation |
| `nuclear_elec_share` | Nuclear as % of total electricity generation |
| `fossil_renewable_ratio` | Fossil-fuel consumption ÷ renewables consumption |

These features make it easier to compare countries on energy-mix composition rather than absolute consumption, which is dominated by population and GDP.

## License
This project is released under the terms of the `LICENSE` file in the project root.