import pandas as pd
import logging
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict
from config import CLEAN_DIR, SENTIMENT_DIR

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    sentiment: Dict[str, float] = analyzer.polarity_scores(text)
    return f"{sentiment['compound']:.4f}".replace('.', ',')


def convert_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
        return dt.strftime("%d %B %Y")
    except ValueError:
        logging.warning(f"Unable to parse date: {date_str}")
        return "unknown"


def analyze_data() -> None:
    for file_path in CLEAN_DIR.glob("*.csv"):
        logging.info(f"Processing file: {file_path.name}")

        try:
            df = pd.read_csv(file_path)
            if "cleaned_tweet" not in df.columns:
                logging.warning(
                    f"Skipped {file_path.name}, no 'cleaned_tweet' column found"
                )
                continue

            df["sentiment"] = df["cleaned_tweet"].apply(analyze_sentiment)
            df["Created_At"] = df["Created_At"].apply(convert_date)

            df["sentiment_float"] = df["sentiment"].str.replace(',', '.').astype(float)
            daily_sentiment = df.groupby("Created_At")["sentiment_float"].mean().reset_index()
            daily_sentiment["sentiment_float"] = (daily_sentiment["sentiment_float"]
                                                  .apply(lambda x: f"{x:.4f}"
                                                         .replace('.', ',')))
            daily_sentiment = daily_sentiment.rename(columns={"sentiment_float": "sentiment"})

            df = df[
                [
                    "Username",
                    "Created_At",
                    "Retweets",
                    "Likes",
                    "cleaned_tweet",
                    "sentiment",
                ]
            ]
            df = df.rename(columns={"cleaned_tweet": "tweet"})

            output_path = SENTIMENT_DIR / f"sentiment_{file_path.stem}.csv"
            df.to_csv(output_path, index=False)

            daily_output_path = SENTIMENT_DIR / f"daily_sentiment_{file_path.stem}.csv"
            daily_sentiment.to_csv(daily_output_path, index=False)

            logging.info(f"Sentiment analysis saved to: {output_path}")
            logging.info(f"Daily sentiment saved to: {daily_output_path}")

        except Exception as e:
            logging.error(f"Failed to process {file_path.name}: {str(e)}")

    logging.info("Sentiment analysis completed.")


if __name__ == "__main__":
    analyze_data()
    
