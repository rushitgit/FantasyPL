"""
This script performs sentiment analysis on news articles related to top Fantasy Premier League players.
It calculates sentiment scores for each player based on relevant news articles and
merges these scores with player data, then categorizes the sentiment as positive, neutral, or negative.
The final dataset with sentiment information is saved to a CSV file.
"""
import csv
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from textblob import TextBlob
# SentimentIntensityAnalyzer was imported but not used. TextBlob is used for sentiment analysis.
import numpy as np

# Load datasets:
# Player data is now read from PredictedPlayerPoints_All.csv (output of teamPlayerModel.py)
# News articles data is loaded with latin1 encoding.
# Using forward slashes for path consistency.
top_players_data = pd.read_csv(r'datasets/PredictedPlayerPoints_All.csv')
articles_data = pd.read_csv(r'datasets/articles_set.csv', encoding='latin1')

# Get unique player names from the player dataset
unique_players = top_players_data['PLAYER'].unique()

# Initialize a list to store sentiment scores for each player
sentiment_scores = []

# Iterate through each unique player to calculate sentiment from related articles
for player_name in unique_players:
    # Filter articles that contain the player's name (case-insensitive)
    player_articles = articles_data[articles_data['text'].str.contains(player_name, case=False, na=False)]
    
    if not player_articles.empty:
        # Combine all text from articles related to the player
        combined_text = ' '.join(player_articles['text'])

        # Perform sentiment analysis using TextBlob
        blob = TextBlob(combined_text)
        sentiment_score = blob.sentiment.polarity # Polarity score ranges from -1 (negative) to 1 (positive)

        sentiment_scores.append({'PLAYER': player_name, 'Sentiment_Score': sentiment_score})
    else:
        # If no articles are found for a player, assign a None sentiment score
        sentiment_scores.append({'PLAYER': player_name, 'Sentiment_Score': None})

# Convert the list of sentiment scores to a pandas DataFrame
sentiment_df = pd.DataFrame(sentiment_scores)

# Merge the sentiment scores with the original top players data
top_players_with_sentiment = pd.merge(top_players_data, sentiment_df, on='PLAYER', how='left')

# Print the merged DataFrame (optional, for verification)
print(top_players_with_sentiment)

# Select relevant columns for the final dataset
top_players_sentiments_df = top_players_with_sentiment[['PLAYER', 'TEAM', 'POSITION','COST','OWNERSHIP %', 'PREDICTED_POINTS','Sentiment_Score']]

# Define conditions to categorize sentiment scores into 'positive', 'neutral', or 'negative'
conditions = [
    (top_players_sentiments_df['Sentiment_Score'] > 0),  # Positive sentiment
    (top_players_sentiments_df['Sentiment_Score'] == 0) | (top_players_sentiments_df['Sentiment_Score'].isna()), # Neutral or no sentiment
    (top_players_sentiments_df['Sentiment_Score'] < 0)  # Negative sentiment
]

# Define corresponding choices for each condition
choices = ['positive', 'neutral', 'negative']

# Apply the conditions to create a 'POSITIVITY' column
top_players_sentiments_df['POSITIVITY'] = np.select(conditions, choices, default='neutral')

# Print the DataFrame with the 'POSITIVITY' column (optional, for verification)
print(top_players_sentiments_df)

# Save the final DataFrame with player sentiments to a CSV file
# Note: The filename 'TopPlayersWithSentiments.csv' is retained for now,
# but it might be reviewed as the input now contains all players, not just 'top' players.
# Using forward slashes for path consistency.
top_players_sentiments_df.to_csv('datasets/TopPlayersWithSentiments.csv', index=False)


################################ end #########################################
# This comment indicates the end of the main script logic.
