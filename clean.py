import os
import re
import pandas as pd

csv_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\raw'
output_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\clean'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

STOPWORDS = set([
    'the', 'is', 'in', 'it', 'and', 'to', 'a', 'of', 'that', 'i', 'for', 'on', 'with', 'you', 'this', 'at', 'by', 'not'
])

def clean_tweet(text):
    if isinstance(text, str):
        text = re.sub(r"http\S+|www\S+|https\S+", '', text)
        text = re.sub(r'\@\w+|\#', '', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower()
        tokens = text.split()
        tokens = [word for word in tokens if word not in STOPWORDS]
        return " ".join(tokens)
    return ""

def clean_data():
    for file_name in os.listdir(csv_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(csv_dir, file_name)
            print(f"Processing file: {file_name}")
            df = pd.read_csv(file_path)
            if 'Text' in df.columns:
                df['cleaned_tweet'] = df['Text'].apply(clean_tweet)
                output_path = os.path.join(output_dir, f"cleaned_{file_name}")
                df.to_csv(output_path, index=False)
                print(f"Cleaned file saved as: cleaned_{file_name}")
            else:
                print(f"Skipped {file_name}, no 'Text' column found")
    print("Data cleaning completed.")
