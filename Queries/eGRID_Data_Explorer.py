import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv('egrid2016.csv')
    
    # Create fuel group mapping
    fuel_map = {
        'BIT': 'COAL', 'LIG': 'COAL', 'RC': 'COAL', 'SUB': 'COAL', 'WC': 'COAL',
        'DFO': 'OIL', 'JF': 'OIL', 'KER': 'OIL', 'RFO': 'OIL', 'WO': 'OIL',
        'BFG': 'GAS', 'COG': 'GAS', 'LFG': 'GAS', 'NG': 'GAS', 'OG': 'GAS', 'PG': 'GAS', 'PRG': 'GAS',
        'GEO': 'RENEW', 'SUN': 'RENEW', 'WAT': 'RENEW', 'WDL': 'RENEW', 'WDS': 'RENEW', 'WND': 'RENEW'
    }
    df['FUEL_GROUP'] = df['PLPRMFL'].map(fuel_map)
    
    return df

def most_energy_generation(df):
    """Plant with most energy generation (MWh)"""
    most_energy = df.loc[df['PLNGENAN'].idxmax()]
    return most_energy['PNAME']

def most_co2_emissions(df):
    """Plant with most CO2 emissions (tons)"""
    most_emissions = df.loc[df['PLCO2EQA'].idxmax()]
    return most_emissions['PNAME']

def state_most_co2_emissions(df):
    """State of the plant with the most CO2 emissions"""
    most_emissions = df.loc[df['PLCO2EQA'].idxmax()]
    return most_emissions['PSTATABB']

def fuel_most_co2_emissions(df):
    """Primary fuel of the plant with most CO2 emissions"""
    most_emissions = df.loc[df['PLCO2EQA'].idxmax()]
    return most_emissions['PLPRMFL']

def northernmost_plant(df):
    """Northernmost power plant (max latitude)"""
    northernmost = df.loc[df['LAT'].idxmax()]
    return northernmost['PNAME']

def state_northernmost_plant(df):
    """State of the northernmost power plant"""
    northernmost = df.loc[df['LAT'].idxmax()]
    return northernmost['PSTATABB']

def state_most_hydro_plants(df):
    """State with the largest number of hydroelectric plants"""
    hydro_df = df[df['PLPRMFL'] == 'WAT']
    hydro_count = hydro_df['PSTATABB'].value_counts()
    return hydro_count.idxmax()

def count_hydro_state(df):
    """Number of hydro plants in the state with most hydro plants"""
    hydro_df = df[df['PLPRMFL'] == 'WAT']
    hydro_count = hydro_df['PSTATABB'].value_counts()
    return hydro_count.max()

def states_most_coal_energy(df):
    """State(s) that generated the most energy using coal"""
    coal_types = ['BIT', 'LIG', 'RC', 'SUB', 'WC']
    coal_df = df[df['PLPRMFL'].isin(coal_types)]
    coal_energy_by_state = coal_df.groupby('PSTATABB')['PLNGENAN'].sum()
    max_energy = coal_energy_by_state.max()
    top_states = coal_energy_by_state[coal_energy_by_state == max_energy].index
    return sorted(top_states)

def total_coal_energy(df):
    """Total coal energy (MWh) produced in top states"""
    coal_types = ['BIT', 'LIG', 'RC', 'SUB', 'WC']
    coal_df = df[df['PLPRMFL'].isin(coal_types)]
    coal_energy_by_state = coal_df.groupby('PSTATABB')['PLNGENAN'].sum()
    max_energy = coal_energy_by_state.max()
    top_states = coal_energy_by_state[coal_energy_by_state == max_energy].index
    return round(coal_energy_by_state[top_states].sum())

def states_one_coal_plant(df):
    """States with exactly 1 coal plant"""
    coal_types = ['BIT', 'LIG', 'RC', 'SUB', 'WC']
    coal_df = df[df['PLPRMFL'].isin(coal_types)]
    coal_plant_counts = coal_df['PSTATABB'].value_counts()
    one_plant_states = coal_plant_counts[coal_plant_counts == 1].index
    return sorted(one_plant_states)

def primary_fuel_emissions(df):
    """Primary fuel category with the most CO2 emissions"""
    fuel_emissions = df.groupby('FUEL_GROUP')['PLCO2EQA'].sum()
    return fuel_emissions.idxmax()

def interactive_cli(df):
    """Interactive command line interface for exploring the data"""
    questions = {
        '1': "Plant with most energy generation (MWh)",
        '2': "Plant with most CO2 emissions (tons)",
        '3': "State of the plant with the most CO2 emissions",
        '4': "Primary fuel of the plant with most CO2 emissions",
        '5': "Northernmost power plant (max latitude)",
        '6': "State of the northernmost power plant",
        '7': "State with the largest number of hydroelectric plants",
        '8': "Number of hydro plants in that state",
        '9': "State(s) that generated the most energy using coal",
        '10': "Total coal energy (MWh) produced in those states",
        '11': "States with exactly 1 coal plant",
        '12': "Primary fuel category with the most CO2 emissions",
        'exit': "Exit the program"
    }
    
    while True:
        print("\nAvailable questions:")
        for key, value in questions.items():
            print(f"{key}. {value}")
        
        choice = input("\nEnter your choice (1-12, plot, or exit): ").lower()
        
        if choice == 'exit':
            print("Goodbye!")
            break
        elif choice in questions:
            try:
                if choice == '1':
                    answer = most_energy_generation(df)
                elif choice == '2':
                    answer = most_co2_emissions(df)
                elif choice == '3':
                    answer = state_most_co2_emissions(df)
                elif choice == '4':
                    answer = fuel_most_co2_emissions(df)
                elif choice == '5':
                    answer = northernmost_plant(df)
                elif choice == '6':
                    answer = state_northernmost_plant(df)
                elif choice == '7':
                    answer = state_most_hydro_plants(df)
                elif choice == '8':
                    answer = count_hydro_state(df)
                elif choice == '9':
                    answer = ', '.join(states_most_coal_energy(df))
                elif choice == '10':
                    answer = total_coal_energy(df)
                elif choice == '11':
                    answer = ', '.join(states_one_coal_plant(df))
                elif choice == '12':
                    answer = primary_fuel_emissions(df)
                
                print(f"\nAnswer to question {choice}: {answer}")
            except Exception as e:
                print(f"Error processing question {choice}: {str(e)}")
        else:
            print("Invalid choice. Please try again.")

def main():
    df = load_data()
    interactive_cli(df)

if __name__ == "__main__":
    main()

