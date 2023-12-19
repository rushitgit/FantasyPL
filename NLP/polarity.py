import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
player_data = pd.read_csv('datasets\TopPlayers.csv')


articles_data = pd.read_csv(r'datasets\articles_set.csv', encoding='latin1')


players_list = player_data['PLAYER'].unique()

# Function to preprocess text
def preprocess_text(text):
    # Tokenize the text
    words = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and word not in stop_words]
    
    return words

def nltk_sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    return sentiment_score

# Function to perform sentiment analysis using TextBlob
def textblob_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# Perform sentiment analysis for each player in the player dataset
for player in players_list:
    # Get articles mentioning the player
    player_articles = articles_data[articles_data['text'].str.contains(player, case=False, na=False)]
    
    if not player_articles.empty:
        
        player_text = ' '.join(player_articles['text'])
        
        
        preprocessed_text = preprocess_text(player_text)
        
        
        nltk_score = nltk_sentiment_analysis(' '.join(preprocessed_text))
        
       
        textblob_score = textblob_sentiment_analysis(' '.join(preprocessed_text))
        
        print(f"\nSentiment Analysis for {player}:")
        print(f"NLTK Sentiment Score: {nltk_score}")
        print(f"TextBlob Sentiment Score: {textblob_score}")
