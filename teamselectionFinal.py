########################### can be viewed as comstraint satisfaction problem #########################################



import pandas as pd

# Load the player data from the CSV file
player_data = pd.read_csv('datasets\TopPlayersWithSentiments.csv')  # Replace 'path_to_your_csv_file.csv' with the actual file path

# Define the positions and the number of players to select for each position
positions_to_select = {'GKP': 1, 'FWD': 3, 'MID': 4, 'DEF': 4}

# Sort players by predicted points in descending order
player_data = player_data.sort_values(by='PREDICTED_POINTS', ascending=False)

# Initialize selected players list
selected_players = []

# Iterate over positions and select players
for position, num_players in positions_to_select.items():
    # Filter players for the current position
    position_players = player_data[player_data['POSITION'] == position]
    
    # Select top N players for the current position
    selected_players.extend(position_players.head(num_players).to_dict(orient='records'))

# Create a DataFrame with the selected players
selected_players_df = pd.DataFrame(selected_players)

# Calculate the total cost of selected players
total_cost = selected_players_df['COST'].sum()

# Display the selected players and total cost
print(selected_players_df[['PLAYER', 'TEAM', 'POSITION', 'COST', 'PREDICTED_POINTS']]) 
selected_players_df.to_csv('datasets\TeamSelection.csv', index=False)
print(f"Total Cost: {total_cost}")

# Check if the total cost is within the budget limit (e.g., 90)
if total_cost <= 90:
    print("Budget constraint satisfied.")
else:
    print("Budget constraint exceeded.")
