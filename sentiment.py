from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
from decimal import Decimal
import logging
from typing import Dict, Any
from config import CLEAN_DIR, SENTIMENT_DIR

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> Decimal:
    sentiment: Dict[str, float] = analyzer.polarity_scores(text)
    return Decimal(sentiment["compound"])


def convert_sentiment(sentiment: Decimal) -> int:
    if -0.5 <= sentiment < -0.1:
        return 0
    elif -1 <= sentiment < -0.5:
        return -1
    elif 0 <= sentiment < 0.49:
        return 0
    elif 0.5 <= sentiment <= 1:
        return 1
    return 0


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
            df["sentiment"] = df["sentiment"].apply(convert_sentiment)
            df["Created_At"] = df["Created_At"].apply(convert_date)

            daily_sentiment = df.groupby("Created_At")["sentiment"].mean().reset_index()

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

            output_path = SENTIMENT_DIR / f"sentiment_{file_path.name}"
            df.to_csv(output_path, index=False)

            daily_output_path = SENTIMENT_DIR / f"daily_sentiment_{file_path.name}"
            daily_sentiment.to_csv(daily_output_path, index=False)

            logging.info(f"Sentiment analysis saved to: {output_path}")
            logging.info(f"Daily sentiment saved to: {daily_output_path}")

        except Exception as e:
            logging.error(f"Failed to process {file_path.name}: {str(e)}")

    logging.info("Sentiment analysis completed.")


if __name__ == "__main__":
    analyze_data()
