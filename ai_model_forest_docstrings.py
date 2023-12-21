import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

def load_and_preprocess_data():
    """
    Load player and team data from CSV files, and filter out players with status 'Injured' or 'Suspended'.

    Returns:
        pd.DataFrame: Player data after preprocessing.
        pd.DataFrame: Team data.
    """
    player_data = pd.read_csv('datasets\PlayerSetCleaned.csv')
    player_data = player_data[(player_data['STATUS'] != 'Injured') & (player_data['STATUS'] != 'Suspended')]

    team_data = pd.read_csv('datasets\TeamDataSetCSV.csv')

    return player_data, team_data

def train_player_model(player_data):
    """
    Train a RandomForestRegressor model on player data.

    Args:
        player_data (pd.DataFrame): Player data.

    Returns:
        Pipeline: Trained player model pipeline.
    """
    player_features = ['MINUTES', 'FORM', 'BONUS', 'POINTS/GAME', 'OWNERSHIP %', 'xG', 'xGI']
    player_target_variable = 'POINTS'

    player_preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), player_features)
        ])

    player_model = Pipeline([
        ('preprocessor', player_preprocessor),
        ('regressor', RandomForestRegressor(random_state=42, max_features='sqrt', max_depth=10, n_estimators=100))
    ])

    X_player = player_data[player_features]
    y_player = player_data[player_target_variable]

    player_model.fit(X_player, y_player)

    return player_model

def predict_and_select_top_players(player_model, player_data):
    """
    Predict player points, calculate predicted points per game, and select top players for each team.

    Args:
        player_model (Pipeline): Trained player model pipeline.
        player_data (pd.DataFrame): Player data.

    Returns:
        pd.DataFrame: Player data with predicted points.
        pd.DataFrame: Selected top players for each team.
    """
    predicted_player_points = player_model.predict(player_data[['MINUTES', 'FORM', 'BONUS', 'POINTS/GAME', 'OWNERSHIP %', 'xG', 'xGI']])


    """changed the formula to predicted_player_points / (player_data['MINUTES'] / 90) from predicted_player_points / 11, 11 was taken as average gameweeks played by a player in the game up until gw 17."""
    player_data['PREDICTED_POINTS'] = predicted_player_points / (player_data['MINUTES'] / 90)

    top_players = player_data.sort_values('PREDICTED_POINTS', ascending=False)

    selected_players = top_players.groupby('TEAM').head(6)

    return player_data, selected_players

def main():
    """
    Main function to execute the entire process.
    """
    player_data, team_data = load_and_preprocess_data()
    player_model = train_player_model(player_data)
    player_data, selected_players = predict_and_select_top_players(player_model, player_data)

    for team in selected_players['TEAM'].unique():
        top_players_team = selected_players[selected_players['TEAM'] == team].sort_values('PREDICTED_POINTS', ascending=False)
        print(f'\nTop 5 players for {team}:')
        print(top_players_team[['PLAYER', 'POSITION', 'PREDICTED_POINTS']])

if __name__ == "__main__":
    main()
