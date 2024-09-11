import os
import re
import pandas as pd

# Path where your CSV files are located
csv_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\raw'
# Path where you want to save the cleaned CSVs
output_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\clean'

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Simple stop words list (can be expanded)
STOPWORDS = set([
    'the', 'is', 'in', 'it', 'and', 'to', 'a', 'of', 'that', 'i', 'for', 'on', 'with', 'you', 'this', 'at', 'by', 'not'
])

def clean_tweet(text):
    if isinstance(text, str):
        # Remove URLs
        text = re.sub(r"http\S+|www\S+|https\S+", '', text)
        # Remove mentions and hashtags, keep text after #
        text = re.sub(r'\@\w+|\#', '', text)
        # Remove special characters, numbers, and punctuations
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Tokenize and remove stop words
        tokens = text.split()
        tokens = [word for word in tokens if word not in STOPWORDS]
        # Join tokens back to a string
        return " ".join(tokens)
    else:
        return ""

# Loop through all CSV files in the directory
for file_name in os.listdir(csv_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_dir, file_name)

        # Load the CSV into a DataFrame
        print(f"Processing file: {file_name}")
        df = pd.read_csv(file_path)

        if 'Text' in df.columns:
            # Clean the tweets
            df['cleaned_tweet'] = df['Text'].apply(clean_tweet)

            # Save the cleaned data to a new CSV
            output_path = os.path.join(output_dir, f"cleaned_{file_name}")
            df.to_csv(output_path, index=False)
            print(f"Cleaned file saved as: cleaned_{file_name}")
        else:
            print(f"Skipped {file_name}, no 'Text' column found")

print("Data cleaning completed.")


