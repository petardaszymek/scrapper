import re
import pandas as pd
import logging
from typing import List, Set
from config import RAW_DIR, CLEAN_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

STOPWORDS: Set[str] = {
    "the",
    "is",
    "in",
    "it",
    "and",
    "to",
    "a",
    "of",
    "that",
    "i",
    "for",
    "on",
    "with",
    "you",
    "this",
    "at",
    "by",
    "not",
    "are",
    "be",
    "will",
    "can",
    "has",
    "have",
    "was",
    "were",
    "would",
    "could",
    "should",
    "did",
    "do",
    "does",
    "done",
}

CRYPTO_TERMS: Set[str] = {
    "btc",
    "eth",
    "usdt",
    "bnb",
    "xrp",
    "ada",
    "doge",
    "sol",
    "ton",
    "trx",
    "dot",
    "matic",
    "ltc",
}


def clean_tweet(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\@\w+|\#", "", text)
    text = re.sub(r"\$\w+", "", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)

    tokens: List[str] = text.split()
    tokens = [
        word for word in tokens if word not in STOPWORDS and word not in CRYPTO_TERMS
    ]
    return " ".join(tokens)


def clean_data() -> None:
    for file_path in RAW_DIR.glob("*.csv"):
        logging.info(f"Processing file: {file_path.name}")

        try:
            df = pd.read_csv(file_path)
            if "Text" not in df.columns:
                logging.warning(f"Skipped {file_path.name}, no 'Text' column found")
                continue

            df["cleaned_tweet"] = df["Text"].apply(clean_tweet)
            output_path = CLEAN_DIR / f"cleaned_{file_path.name}"
            df.to_csv(output_path, index=False)
            logging.info(f"Cleaned file saved as: {output_path}")

        except Exception as e:
            logging.error(f"Error processing {file_path.name}: {str(e)}")

    logging.info("Data cleaning completed.")


if __name__ == "__main__":
    clean_data()
