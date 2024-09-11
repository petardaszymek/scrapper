from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
import csv
import os

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# List of coin IDs you want to pull data for
coins = [
    'bitcoin', 'ethereum', 'tether', 'binancecoin', 'ripple', 'cardano', 'dogecoin', 'solana', 'toncoin',
    'tron', 'polkadot', 'matic-network', 'litecoin', 'avalanche-2', 'chainlink', 'shiba-inu', 'bitcoin-cash',
    'wrapped-bitcoin', 'dai', 'stellar', 'uniswap', 'monero', 'aptos', 'near', 'vechain', 'hedera', 'internet-computer',
    'filecoin', 'aave', 'bittensor', 'qubic', 'synapse-2', 'nomad', 'media-licensing-token', 'woo-network'
]

# Directory to save the CSV files
output_dir = r'C:\Users\User\PycharmProjects\twitter_scrap\currency_vals'
os.makedirs(output_dir, exist_ok=True)

# Convert date to timestamp (UNIX time)
start_date = int(datetime.strptime('01-07-2024', '%d-%m-%Y').timestamp())
end_date = int(datetime.strptime('03-08-2024', '%d-%m-%Y').timestamp())

# Convert timestamp to 'day month year' (e.g., '2 sierpnia 2024')
def format_date(timestamp):
    try:
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        return dt.strftime('%d %B %Y')  # Convert to day month year
    except ValueError:
        return 'unknown'  # Handle any date formatting errors

# Function to save data to CSV
def save_to_csv(coin, merged_data):
    filename = os.path.join(output_dir, f"{coin}.csv")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Price (USD)", "Market Cap", "Volume"])
        for point in merged_data:
            try:
                timestamp, price, market_cap, volume = point
                date = format_date(timestamp)

                # Cast price to integer
                price = int(price)

                writer.writerow([date, price, market_cap, volume])
            except Exception as e:
                print(f"Error processing data point {point}: {e}")


# Merge price, market cap, and volume data by timestamp
def merge_data(prices, market_caps, volumes):
    merged = []
    for price, market_cap, volume in zip(prices, market_caps, volumes):
        if price[0] == market_cap[0] == volume[0]:  # Ensure the timestamps match
            merged.append([price[0], price[1], market_cap[1], volume[1]])
        else:
            print(f"Timestamp mismatch: {price[0]}, {market_cap[0]}, {volume[0]}")
    return merged

# Fetch and save data for each coin
for coin in coins:
    print(f"Fetching data for {coin}...")
    try:
        data = cg.get_coin_market_chart_range_by_id(id=coin, vs_currency='usd', from_timestamp=start_date,
                                                    to_timestamp=end_date)
        if not all(key in data for key in ['prices', 'market_caps', 'total_volumes']):
            print(f"Missing data for {coin}: {data}")
            continue
        # Merge the data based on matching timestamps
        merged_data = merge_data(data['prices'], data['market_caps'], data['total_volumes'])
        save_to_csv(coin, merged_data)
    except Exception as e:
        print(f"Failed to fetch data for {coin}: {e}")
