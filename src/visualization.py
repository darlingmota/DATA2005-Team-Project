import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load spreadsheet
df = pd.read_excel("World Energy Consumption.xlsx")

sns.set_theme(style="whitegrid")

# -----------------------------
# GRAPH 1: Global Energy Transition
# -----------------------------
world = df[df["country"] == "World"].copy()
world = world.dropna(subset=["fossil_fuel_consumption", "renewables_consumption"])

plt.figure(figsize=(10, 5))
plt.stackplot(
    world["year"],
    world["fossil_fuel_consumption"],
    world["renewables_consumption"],
    labels=["Fossil", "Renewables"],
    colors=["dimgray", "mediumseagreen"]
)
plt.title("Global Energy Transition")
plt.xlabel("")
plt.ylabel("")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("1_global_energy_transition.png")
plt.show()


# -----------------------------
# GRAPH 2: Renewables Share by Continent
# -----------------------------
continents = ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]

continent_df = df[
    (df["country"].isin(continents)) &
    (df["year"] >= 2000) &
    (df["renewables_share_elec"].notna())
].copy()

plt.figure(figsize=(10, 5))
sns.violinplot(
    data=continent_df,
    x="country",
    y="renewables_share_elec"
)
plt.xlabel("country")
plt.ylabel("renewables_share_elec")
plt.tight_layout()
plt.savefig("2_renewables_share_violin.png")
plt.show()


# -----------------------------
# GRAPH 3: Top 5 Countries Energy Source Comparison
# -----------------------------
latest_year = df["year"].max()

top_countries = ["China", "United States", "India", "Russia", "Japan"]

top_df = df[
    (df["country"].isin(top_countries)) &
    (df["year"] == latest_year)
].copy()

melted = top_df.melt(
    id_vars=["country"],
    value_vars=["coal_consumption", "gas_consumption", "renewables_consumption"],
    var_name="variable",
    value_name="value"
)

plt.figure(figsize=(10, 5))
sns.barplot(
    data=melted,
    x="country",
    y="value",
    hue="variable"
)
plt.xlabel("country")
plt.ylabel("value")
plt.tight_layout()
plt.savefig("3_top5_energy_sources.png")
plt.show()


# -----------------------------
# GRAPH 4: Statistical Shift in Carbon Intensity
# -----------------------------
carbon_df = df[
    (df["country"].notna()) &
    (df["iso_code"].notna()) &
    (df["year"].isin([2000, 2021])) &
    (df["carbon_intensity_elec"].notna())
].copy()

plt.figure(figsize=(10, 5))

sns.kdeplot(
    data=carbon_df[carbon_df["year"] == 2000],
    x="carbon_intensity_elec",
    fill=True,
    label="Year 2000"
)

sns.kdeplot(
    data=carbon_df[carbon_df["year"] == 2021],
    x="carbon_intensity_elec",
    fill=True,
    label="Year 2021"
)

plt.title("Statistical Shift in Carbon Intensity")
plt.xlabel("carbon_intensity_elec")
plt.ylabel("Density")
plt.legend()
plt.tight_layout()
plt.savefig("4_carbon_intensity_shift.png")
plt.show()


# -----------------------------
# GRAPH 5: Energy Per Capita by Continent
# -----------------------------
facet_df = df[
    (df["country"].isin(continents)) &
    (df["year"] >= 2000) &
    (df["energy_per_capita"].notna())
].copy()

g = sns.FacetGrid(
    facet_df,
    col="country",
    col_wrap=3,
    height=3,
    sharey=True
)

g.map_dataframe(
    sns.lineplot,
    x="year",
    y="energy_per_capita",
    marker="o",
    color="purple"
)

g.set_axis_labels("year", "energy_per_capita")
g.set_titles("country = {col_name}")
plt.tight_layout()
plt.savefig("5_energy_per_capita_facets.png")
plt.show()

print("All 5 graphs saved successfully.")
