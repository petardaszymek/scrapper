import pandas as pd
import numpy as np
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, Any, List
from config import SENTIMENT_DIR, CURRENCY_VALS_DIR, RESULTS_DIR
from scipy import stats
import matplotlib.pyplot as plt

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

analyzer = SentimentIntensityAnalyzer()

CRYPTO_FILE_MAPPING = {
    'aave': 'aave.csv',
    'ada': 'cardano.csv',
    'apt': 'aptos.csv',
    'avax': 'avalanche-2.csv',
    'bnb': 'binancecoin.csv',
    'btc': 'bitcoin.csv',
    'bch': 'bitcoin-cash.csv',
    'link': 'chainlink.csv',
    'dai': 'dai.csv',
    'doge': 'dogecoin.csv',
    'eth': 'ethereum.csv',
    'fil': 'filecoin.csv',
    'icp': 'internet-computer.csv',
    'ltc': 'litecoin.csv',
    'matic': 'matic-network.csv',
    'near': 'near.csv',
    'dot': 'polkadot.csv',
    'xrp': 'ripple.csv',
    'shib': 'shiba-inu.csv',
    'sol': 'solana.csv',
    'xlm': 'stellar.csv',
    'usdt': 'tether.csv',
    'ton': 'toncoin.csv',
    'trx': 'tron.csv',
    'uni': 'uniswap.csv',
    'vet': 'vechain.csv',
    'wbtc': 'wrapped-bitcoin.csv',
    'xmr': 'monero.csv',
    'tao': 'bittensor.csv',
    'hbar': 'hedera'
}


def create_correlation_chart(cryptocurrency: str, sentiment: pd.Series, price: pd.Series, correlation: float,
                             p_value: float):
    plt.figure(figsize=(10, 6))
    plt.scatter(sentiment, price)
    plt.xlabel('Sentiment')
    plt.ylabel('Price (USD)')
    plt.title(f'{cryptocurrency} Sentiment vs Price\nCorrelation: {correlation:.4f}, p-value: {p_value:.4f}')

    chart_path = RESULTS_DIR / f"{cryptocurrency}_correlation_chart.png"
    plt.savefig(chart_path)
    plt.close()
    logging.info(f"Correlation chart saved for {cryptocurrency}: {chart_path}")


def analyze_data() -> None:
    results: List[Dict[str, Any]] = []

    for sentiment_file in SENTIMENT_DIR.glob("daily_sentiment_cleaned_*.csv"):
        cryptocurrency = sentiment_file.stem.split('_')[3] 
        logging.info(f"Processing file: {sentiment_file.name}")

        try:
            daily_sentiment = pd.read_csv(sentiment_file)

            daily_sentiment["Created_At"] = pd.to_datetime(daily_sentiment["Created_At"], format="%d %B %Y",
                                                           errors='coerce')
            daily_sentiment = daily_sentiment.dropna(subset=["Created_At"])

            daily_sentiment = daily_sentiment.sort_values("Created_At")

            daily_sentiment["sentiment"] = daily_sentiment["sentiment"].str.replace(',', '.').astype(float)

            price_file_name = CRYPTO_FILE_MAPPING.get(cryptocurrency)
            if not price_file_name:
                logging.warning(f"No matching price file found for {cryptocurrency}")
                continue

            price_file = CURRENCY_VALS_DIR / price_file_name
            if not price_file.exists():
                logging.warning(f"Price data file not found: {price_file}")
                continue

            price_data = pd.read_csv(price_file)
            price_data["Date"] = pd.to_datetime(price_data["Date"])
            price_column = next((col for col in price_data.columns if 'price' in col.lower()), None)
            if not price_column:
                logging.warning(f"No price column found for {cryptocurrency}")
                continue

            price_data[price_column] = price_data[price_column].str.replace(',', '.').astype(float)
            price_data = price_data.sort_values("Date")

            merged_data = pd.merge_asof(daily_sentiment, price_data, left_on="Created_At",
                                        right_on="Date", direction="nearest")

            if len(merged_data) > 1:
                correlation, p_value = stats.pearsonr(merged_data["sentiment"], merged_data[price_column])
                create_correlation_chart(cryptocurrency, merged_data["sentiment"], merged_data[price_column],
                                         correlation, p_value)
            else:
                logging.warning(f"Not enough data to calculate correlation for {cryptocurrency}")
                correlation, p_value = np.nan, np.nan

            results.append({
                "Cryptocurrency": cryptocurrency,
                "Correlation": correlation,
                "P-value": p_value,
                "Days": len(merged_data)
            })

            logging.info(
                f"Successfully processed {cryptocurrency}: Correlation={correlation:.4f},"
                f" P-value={p_value:.4f}, Days={len(merged_data)}")

        except Exception as e:
            logging.error(f"Failed to process {sentiment_file.name}: {str(e)}", exc_info=True)

    if not results:
        logging.warning("No data was processed successfully. Results list is empty.")
        return

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / "crypto_sentiment_analysis.csv"
    results_df.to_csv(output_path, index=False, sep=';')

    logging.info(f"Crypto sentiment analysis saved to: {output_path}")
    logging.info("Correlation analysis completed.")


if __name__ == "__main__":
    analyze_data()
    
