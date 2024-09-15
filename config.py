from pathlib import Path

ROOT_DIR = Path(__file__).parent

# Directory configurations
RAW_DIR = ROOT_DIR / "raw"
CLEAN_DIR = ROOT_DIR / "clean"
SENTIMENT_DIR = ROOT_DIR / "sentiment"
CURRENCY_VALS_DIR = ROOT_DIR / "currency_vals"

# File configurations
COOKIES_FILE = ROOT_DIR / "cookies.json"
RESUME_FILE = ROOT_DIR / "resume_state.json"

# Ensure all directories exist
for directory in [RAW_DIR, CLEAN_DIR, SENTIMENT_DIR, CURRENCY_VALS_DIR]:
    directory.mkdir(exist_ok=True)

# Twitter API credentials
TWITTER_USERNAME = "login"
TWITTER_EMAIL = "e-mail"
TWITTER_PASSWORD = "password"

# CoinGecko API settings
COINGECKO_COINS = [
    "bitcoin",
    "ethereum",
    "tether",
    "binancecoin",
    "ripple",
    "cardano",
    "dogecoin",
    "solana",
    "toncoin",
    "tron",
    "polkadot",
    "matic-network",
    "litecoin",
    "avalanche-2",
    "chainlink",
    "shiba-inu",
    "bitcoin-cash",
    "wrapped-bitcoin",
    "dai",
    "stellar",
    "uniswap",
    "monero",
    "aptos",
    "near",
    "vechain",
    "hedera",
    "internet-computer",
    "filecoin",
    "aave",
    "bittensor",
    "qubic",
    "synapse-2",
    "nomad",
    "media-licensing-token",
    "woo-network",
]
