import pandas as pd

# Load the dataset
df = pd.read_csv('egrid2016.csv')

# --- Question 1: Power plant with most energy generation (MWh)
most_energy = df.loc[df['PLNGENAN'].idxmax()]
print("1. Plant with most energy generation:", most_energy['PNAME'])

# --- Question 2: Power plant with most CO2 emissions (tons)
most_emissions = df.loc[df['PLCO2EQA'].idxmax()]
print("2. Plant with most CO2 emissions:", most_emissions['PNAME'])

# --- Question 3: State of the plant with the most CO2 emissions
print("3. Located in state:", most_emissions['PSTATABB'])

# --- Question 4: Primary fuel of the plant with most CO2 emissions
print("4. Primary fuel:", most_emissions['PLPRMFL'])

# --- Question 5: Name of the northernmost power plant (max latitude)
northernmost = df.loc[df['LAT'].idxmax()]
print("5. Northernmost plant:", northernmost['PNAME'])

# --- Question 6: State of the northernmost power plant
print("6. State:", northernmost['PSTATABB'])

# --- Question 7: State with the largest number of hydroelectric plants
hydro_df = df[df['PLPRMFL'] == 'WAT']
hydro_count = hydro_df['PSTATABB'].value_counts()
most_hydro_state = hydro_count.idxmax()
print("7. State with most hydro plants:", most_hydro_state)

# --- Question 8: How many hydro plants in that state?
print("8. Number of hydro plants in that state:", hydro_count[most_hydro_state])

# --- Question 9: State(s) that generated the most energy using coal
coal_types = ['BIT', 'LIG', 'RC', 'SUB', 'WC']
coal_df = df[df['PLPRMFL'].isin(coal_types)]
coal_energy_by_state = coal_df.groupby('PSTATABB')['PLNGENAN'].sum()
max_energy = coal_energy_by_state.max()
top_states = coal_energy_by_state[coal_energy_by_state == max_energy].index
print("9. State(s) with most coal energy generation:", ",".join(sorted(top_states)))

# --- Question 10: Total coal energy (MWh) produced in those states
total_energy = coal_energy_by_state[top_states].sum()
print("10. Total MWh (rounded):", round(total_energy))

# --- Question 11: States with exactly 1 coal plant
coal_plant_counts = coal_df['PSTATABB'].value_counts()
one_plant_states = coal_plant_counts[coal_plant_counts == 1].index
print("11. States with exactly one coal plant:", ",".join(sorted(one_plant_states)))

# --- Question 12: Primary fuel category with the most CO2 emissions
fuel_map = {
    'BIT': 'COAL', 'LIG': 'COAL', 'RC': 'COAL', 'SUB': 'COAL', 'WC': 'COAL',
    'DFO': 'OIL', 'JF': 'OIL', 'KER': 'OIL', 'RFO': 'OIL', 'WO': 'OIL',
    'BFG': 'GAS', 'COG': 'GAS', 'LFG': 'GAS', 'NG': 'GAS', 'OG': 'GAS', 'PG': 'GAS', 'PRG': 'GAS',
    'GEO': 'RENEW', 'SUN': 'RENEW', 'WAT': 'RENEW', 'WDL': 'RENEW', 'WDS': 'RENEW', 'WND': 'RENEW'
}
df['FUEL_GROUP'] = df['PLPRMFL'].map(fuel_map)
fuel_emissions = df.groupby('FUEL_GROUP')['PLCO2EQA'].sum()
max_fuel = fuel_emissions.idxmax()
print("12. Fuel group with most CO2 emissions:", max_fuel)
