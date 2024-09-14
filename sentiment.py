from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import os
from datetime import datetime
from decimal import Decimal

clean_csv_dir = r'.\clean'
output_dir = r'.\sentiment'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment = analyzer.polarity_scores(text)
    return Decimal(sentiment['compound'])

def convert_sentiment(sentiment):
    if -0.5 <= sentiment < -0.1:
        return 0
    elif -1 <= sentiment < -0.5:
        return -1
    elif 0 <= sentiment < 0.49:
        return 0
    elif 0.5 <= sentiment <= 1:
        return 1
    return 0

def convert_date(date_str):
    try:
        dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
        return dt.strftime('%d %B %Y')
    except ValueError:
        return 'unknown'

def analyze_data():
    for file_name in os.listdir(clean_csv_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(clean_csv_dir, file_name)
            try:
                print(f"Processing file: {file_name}")
                df = pd.read_csv(file_path)
                if 'cleaned_tweet' in df.columns:
                    df['sentiment'] = df['cleaned_tweet'].apply(analyze_sentiment)
                    df['sentiment'] = df['sentiment'].apply(convert_sentiment)
                    df['Created_At'] = df['Created_At'].apply(convert_date)
                    df = df[['Username', 'Created_At', 'Retweets', 'Likes', 'cleaned_tweet', 'sentiment']]
                    df = df.rename(columns={'cleaned_tweet': 'tweet'})
                    output_path = os.path.join(output_dir, f"sentiment_{file_name}")
                    df.to_csv(output_path, index=False)
                    print(f"Sentiment analysis saved to: sentiment_{file_name}")
                else:
                    print(f"Skipped {file_name}, no 'cleaned_tweet' column found")
            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
    print("Sentiment analysis completed.")
