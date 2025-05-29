"""
This script trains a machine learning model to predict Fantasy Premier League player points
and identifies the top players based on these predictions.
It uses player statistics and team data for model training and selection.
"""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline

# Load the player dataset from the CSV file and filter out injured/suspended players
player_data = pd.read_csv('datasets\PlayerSetCleaned.csv') # Note: Backslash in path might cause issues on non-Windows systems
player_data = player_data[(player_data['STATUS'] != 'Injured') & (player_data['STATUS'] != 'Suspended')]

# Load the team dataset
team_data = pd.read_csv('datasets\TeamDataSetCSV.csv') # Note: Backslash in path

# Define features for player points prediction
player_features = ['MINUTES', 'FORM', 'BONUS', 'POINTS/GAME', 'OWNERSHIP %', 'xG', 'xGI']

# Define features for team rating (currently not used in this script for player prediction)
team_features = ['RATING', 'WIN SCORE']

# Define the target variable for player points prediction
player_target_variable = 'POINTS'

# Split player data into training and testing sets
player_train_data, player_test_data = train_test_split(player_data, test_size=0.2, random_state=42)

# Define a preprocessor for handling missing values in player data
player_preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='mean'), player_features) # Impute missing numerical values with the mean
    ])

# Define a machine learning pipeline for the player model
# It includes preprocessing and a Random Forest Regressor
player_model = Pipeline([
    ('preprocessor', player_preprocessor),
    ('regressor', RandomForestRegressor(random_state=42)) # Use RandomForestRegressor for prediction
])

# Prepare the training data for the player model
X_player_train = player_train_data[player_features]
y_player_train = player_train_data[player_target_variable]

# Train the player model using the training data
player_model.fit(X_player_train, y_player_train)

# Prepare the data for all active players for prediction
X_all_players = player_data[player_features]

# Predict points for all active players
predicted_points_all_players = player_model.predict(X_all_players)

# Add the predicted points to the player_data DataFrame
# The division by 11 has been removed as per refactoring instructions.
# The original comment was:
# TODO: Clarify why predicted points are divided by 11. Is this to normalize per game week or some other domain-specific reason?
player_data['PREDICTED_POINTS'] = predicted_points_all_players

# Sort the full player data by predicted points in descending order
all_players_sorted = player_data.sort_values('PREDICTED_POINTS', ascending=False)

# Save the sorted list of all players with their predicted points to a CSV file
# The index is not written to the CSV file.
# Note: Backslash in path might cause issues on non-Windows systems.
all_players_sorted.to_csv('datasets/PredictedPlayerPoints_All.csv', index=False)

print("Predicted points for all active players saved to datasets/PredictedPlayerPoints_All.csv")

# The following sections for test data prediction and printing top players by team are now removed
# as per the refactoring to predict for all players and save to CSV.
# X_player_test = player_test_data[player_features]
# y_player_test = player_test_data[player_target_variable]
# predicted_player_points_test = player_model.predict(X_player_test)
# player_test_data['PREDICTED_POINTS'] = predicted_player_points_test
# top_players = player_test_data.sort_values('PREDICTED_POINTS', ascending=False)
# selected_players = top_players.groupby('TEAM').head(5)
# for team in player_test_data['TEAM'].unique():
#     top_players_team = player_test_data[player_test_data['TEAM'] == team].sort_values('PREDICTED_POINTS', ascending=False)
#     print(f'\nBest players for {team}:')
#     print(top_players_team[['PLAYER', 'POSITION', 'PREDICTED_POINTS']])
