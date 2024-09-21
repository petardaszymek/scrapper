import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from config import SENTIMENT_DIR, CURRENCY_VALS_DIR, CHARTS_DIR
from matplotlib.ticker import FuncFormatter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CRYPTO_FILE_MAPPING = {
    'hbar': 'hedera.csv',
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
    'tao': 'bittensor.csv'
}


def parse_date(date_str):
    if date_str == "unknown":
        return pd.NaT
    for fmt in ("%d %B %Y", "%Y-%m-%d", "%a %b %d %H:%M:%S %z %Y"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    logging.warning(f"Unable to parse date: {date_str}")
    return pd.NaT


def load_and_prepare_sentiment_data(file_path):
    df = pd.read_csv(file_path)
    df['Created_At'] = df['Created_At'].apply(parse_date)
    df['sentiment'] = df['sentiment'].str.replace(',', '.').astype(float)
    df = df.dropna(subset=['Created_At'])  
    return df.groupby(df['Created_At'].dt.date)['sentiment'].sum().reset_index()


def load_and_prepare_price_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Price (USD)'] = df['Price (USD)'].str.replace(',', '.').astype(float)
    return df.groupby(df['Date'].dt.date)['Price (USD)'].mean().reset_index()


def create_combined_chart(sentiment_data, price_data, cryptocurrency):
    sns.set_style("darkgrid")
    sns.set_palette("muted")

    fig, ax1 = plt.subplots(figsize=(16, 9))

    sns.lineplot(x='Date', y='Price (USD)', data=price_data, ax=ax1, color='skyblue', linewidth=2, label='Price (USD)')
    ax1.fill_between(price_data['Date'], price_data['Price (USD)'], alpha=0.3, color='skyblue')

    ax1.set_ylabel('Price (USD)', color='skyblue', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='skyblue')

    min_price = price_data['Price (USD)'].min()
    ax1.set_ylim(bottom=min_price)
    max_price = price_data['Price (USD)'].max()
    ax1.set_ylim(top=max_price)

    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2 = ax1.twinx()

    sns.lineplot(x='Created_At', y='sentiment', data=sentiment_data, ax=ax2, color='coral', linewidth=2,
                 label='Sentiment')

    ax2.set_ylabel('Sentiment', color='coral', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='coral')

    plt.title(f'{cryptocurrency.upper()} - Price and Sentiment Over Time', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Date', fontsize=12)

    plt.xticks(rotation=45)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, ['Price (USD)', 'Sentiment'], loc='upper left', fontsize=10)

    if ax1.get_legend():
        ax1.get_legend().remove()
    if ax2.get_legend():
        ax2.get_legend().remove()

    ax1.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    output_path = CHARTS_DIR / f"{cryptocurrency}_price_sentiment_chart.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Chart saved to: {output_path}")


def chart():
    for crypto, price_file in CRYPTO_FILE_MAPPING.items():
        sentiment_file = SENTIMENT_DIR / f"sentiment_cleaned_{crypto}.csv"
        price_file_path = CURRENCY_VALS_DIR / price_file

        if not sentiment_file.exists() or not price_file_path.exists():
            logging.warning(f"Skipping {crypto}: Missing sentiment or price data file")
            continue

        sentiment_data = load_and_prepare_sentiment_data(sentiment_file)
        price_data = load_and_prepare_price_data(price_file_path)

        logging.info(f"Processing {crypto}")
        logging.info(f"Sentiment data shape: {sentiment_data.shape}")
        logging.info(f"Price data shape: {price_data.shape}")

        create_combined_chart(sentiment_data, price_data, crypto)


if __name__ == "__main__":
    chart()
    
