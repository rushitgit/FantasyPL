import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

player_data = pd.read_csv('datasets\PlayerSetCleaned.csv')
player_data = player_data[(player_data['STATUS'] != 'Injured') & (player_data['STATUS'] != 'Suspended')]


team_data = pd.read_csv('datasets\TeamDataSetCSV.csv')


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


predicted_player_points = player_model.predict(X_player)


player_data['PREDICTED_POINTS'] = predicted_player_points / 11

top_players = player_data.sort_values('PREDICTED_POINTS', ascending=False)


selected_players = top_players.groupby('TEAM').head(6)

for team in selected_players['TEAM'].unique():
    top_players_team = selected_players[selected_players['TEAM'] == team].sort_values('PREDICTED_POINTS', ascending=False)
    print(f'\nTop 5 players for {team}:')
    print(top_players_team[['PLAYER', 'POSITION', 'PREDICTED_POINTS']])
