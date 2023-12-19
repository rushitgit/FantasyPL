import csv
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
top_players_data = pd.read_csv(r'datasets\TopPlayers.csv')


articles_data = pd.read_csv(r'datasets\articles_set.csv', encoding='latin1')

unique_players = top_players_data['PLAYER'].unique()


sentiment_scores = []


for player_name in unique_players:
   
    player_articles = articles_data[articles_data['text'].str.contains(player_name, case=False, na=False)]
    if not player_articles.empty:
        # Combine all articles for the player
        combined_text = ' '.join(player_articles['text'])

        # Use TextBlob for sentiment analysis
        blob = TextBlob(combined_text)
        sentiment_score = blob.sentiment.polarity

        sentiment_scores.append({'PLAYER': player_name, 'Sentiment_Score': sentiment_score})
    else:
        sentiment_scores.append({'PLAYER': player_name, 'Sentiment_Score': None})


sentiment_df = pd.DataFrame(sentiment_scores)
top_players_with_sentiment = pd.merge(top_players_data, sentiment_df, on='PLAYER', how='left')
print(top_players_with_sentiment)







# Select relevant columns
top_players_sentiments_df = top_players_with_sentiment[['PLAYER', 'TEAM', 'POSITION','COST','OWNERSHIP %', 'PREDICTED_POINTS','Sentiment_Score']]

conditions = [
    (top_players_sentiments_df['Sentiment_Score'] > 0),
    (top_players_sentiments_df['Sentiment_Score'] == 0) | (top_players_sentiments_df['Sentiment_Score'].isna()),
    (top_players_sentiments_df['Sentiment_Score'] < 0)
]

choices = ['positive', 'neutral', 'negative']

top_players_sentiments_df['POSITIVITY'] = np.select(conditions, choices, default='neutral')


print(top_players_sentiments_df)

top_players_sentiments_df.to_csv('datasets\TopPlayersWithSentiments.csv')



