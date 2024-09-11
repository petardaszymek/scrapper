from textblob import TextBlob
import pandas as pd
import os

# Path where cleaned CSV files are located
clean_csv_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\clean'
# Path where you want to save the sentiment-analyzed CSVs
output_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\sentiment'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    # TextBlob returns polarity as a float where:
    # > 0 is positive, = 0 is neutral, < 0 is negative
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"

# Loop through all cleaned CSV files in the directory
for file_name in os.listdir(clean_csv_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(clean_csv_dir, file_name)

        # Load the CSV into a DataFrame
        print(f"Processing file: {file_name}")
        df = pd.read_csv(file_path)

        if 'cleaned_tweet' in df.columns:
            # Apply sentiment analysis
            df['sentiment'] = df['cleaned_tweet'].apply(analyze_sentiment)
            df = df[['Username', 'Created_At', 'Retweets', 'Likes', 'cleaned_tweet', 'sentiment']]
            df = df.rename(columns={
                'cleaned_tweet': 'tweet'})
            # Save the sentiment-analyzed data to a new CSV
            output_path = os.path.join(output_dir, f"sentiment_{file_name}")
            df.to_csv(output_path, index=False)
            print(f"Sentiment analysis saved to: sentiment_{file_name}")
        else:
            print(f"Skipped {file_name}, no 'cleaned_tweet' column found")

print("Sentiment analysis completed.")
