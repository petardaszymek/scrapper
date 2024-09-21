import logging
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
from typing import List, Tuple
from config import CURRENCY_VALS_DIR, COINGECKO_COINS
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

cg = CoinGeckoAPI()

start_date = int(datetime.strptime("01-07-2024", "%d-%m-%Y").timestamp())
end_date = int(datetime.strptime("03-08-2024", "%d-%m-%Y").timestamp())


def format_date(timestamp: int) -> str:
    try:
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        return dt.strftime("%d %B %Y")
    except ValueError:
        return "unknown"


def save_to_csv(coin: str, merged_data: List[Tuple[int, float, float, float]]) -> None:
    filename = CURRENCY_VALS_DIR / f"{coin}.csv"
    df = pd.DataFrame(merged_data, columns=["Timestamp", "Price (USD)", "Market Cap", "Volume"])
    df["Date"] = df["Timestamp"].apply(format_date)
    df = df[["Date", "Price (USD)", "Market Cap", "Volume"]]

    # Format numbers with comma as decimal separator
    df["Price (USD)"] = df["Price (USD)"].apply(lambda x: f"{x:.8f}".replace(".", ","))
    df["Market Cap"] = df["Market Cap"].apply(lambda x: f"{x:.2f}".replace(".", ","))
    df["Volume"] = df["Volume"].apply(lambda x: f"{x:.2f}".replace(".", ","))

    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")


def merge_data(
        prices: List, market_caps: List, volumes: List
) -> List[Tuple[int, float, float, float]]:
    merged = []
    for price, market_cap, volume in zip(prices, market_caps, volumes):
        if price[0] == market_cap[0] == volume[0]:
            merged.append((price[0], price[1], market_cap[1], volume[1]))
        else:
            logging.warning(
                f"Timestamp mismatch: {price[0]}, {market_cap[0]}, {volume[0]}"
            )
    return merged


def fetch_coin_data() -> None:
    for coin in COINGECKO_COINS:
        logging.info(f"Fetching data for {coin}...")
        try:
            data = cg.get_coin_market_chart_range_by_id(
                id=coin,
                vs_currency="usd",
                from_timestamp=start_date,
                to_timestamp=end_date,
            )
            if not all(
                    key in data for key in ["prices", "market_caps", "total_volumes"]
            ):
                logging.warning(f"Missing data for {coin}: {data}")
                continue
            merged_data = merge_data(
                data["prices"], data["market_caps"], data["total_volumes"]
            )
            save_to_csv(coin, merged_data)
        except Exception as e:
            logging.error(f"Failed to fetch data for {coin}: {e}")


if __name__ == "__main__":
    fetch_coin_data()
