########################### can be viewed as comstraint satisfaction problem #########################################
import pandas as pd

player_data = pd.read_csv('datasets\TopPlayersWithSentiments.csv') 
positions_to_select = {'GKP': 1, 'FWD': 3, 'MID': 4, 'DEF': 4}
player_data = player_data.sort_values(by='PREDICTED_POINTS', ascending=False)

selected_players = []

for position, num_players in positions_to_select.items():
    
    position_players = player_data[player_data['POSITION'] == position]
    
    
    selected_players.extend(position_players.head(num_players).to_dict(orient='records'))


selected_players_df = pd.DataFrame(selected_players)

total_cost = selected_players_df['COST'].sum()


print(selected_players_df[['PLAYER', 'TEAM', 'POSITION', 'COST', 'PREDICTED_POINTS']]) 
selected_players_df.to_csv('datasets\TeamSelection.csv', index=False)
print(f"Total Cost: {total_cost}")

if total_cost <= 90:
    print("Budget constraint satisfied.")
else:
    print("Budget constraint exceeded.")
