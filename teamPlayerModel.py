import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline

# Load the player dataset from the Excel sheet
player_data = pd.read_csv('datasets\PlayerSetCleaned.csv')
player_data = player_data[(player_data['STATUS'] != 'Injured') & (player_data['STATUS'] != 'Suspended')]

# Load the team dataset
team_data = pd.read_csv('datasets\TeamDataSetCSV.csv')

# Select the relevant features for player prediction
player_features = ['MINUTES', 'FORM', 'BONUS', 'POINTS/GAME', 'OWNERSHIP %', 'xG', 'xGI']

# Select the relevant features for team rating
team_features = ['RATING', 'WIN SCORE']

# Assuming 'POINTS' is the target variable for players
player_target_variable = 'POINTS'

# Split the player data into training and testing sets
player_train_data, player_test_data = train_test_split(player_data, test_size=0.2, random_state=42)

# Define a preprocessor for player data
player_preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='mean'), player_features)
    ])

# Define a pipeline for player model
player_model = Pipeline([
    ('preprocessor', player_preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

# Prepare the player training data
X_player_train = player_train_data[player_features]
y_player_train = player_train_data[player_target_variable]

# Train the player model
player_model.fit(X_player_train, y_player_train)

# Prepare the player testing data
X_player_test = player_test_data[player_features]
y_player_test = player_test_data[player_target_variable]

# Predict the points for the player test data
predicted_player_points = player_model.predict(X_player_test)

# Add the predicted points to the player test data
player_test_data['PREDICTED_POINTS'] = predicted_player_points / 11

# Sort the player test data by predicted points in descending order
top_players = player_test_data.sort_values('PREDICTED_POINTS', ascending=False)

# Select the top 3 players from each team
selected_players = top_players.groupby('TEAM').head(5)

# Print the selected players
for team in player_test_data['TEAM'].unique():
    top_players_team = player_test_data[player_test_data['TEAM'] == team].sort_values('PREDICTED_POINTS', ascending=False)
    print(f'\nBest players for {team}:')
    print(top_players_team[['PLAYER', 'POSITION', 'PREDICTED_POINTS']])
