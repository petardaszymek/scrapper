import asyncio
import csv
import logging
import random
import json
from twikit import Client, TooManyRequests
from datetime import datetime
from typing import List, Tuple, Optional
from config import (
    RAW_DIR,
    COOKIES_FILE,
    RESUME_FILE,
    TWITTER_USERNAME,
    TWITTER_EMAIL,
    TWITTER_PASSWORD,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

MINIMUM_TWEETS = # Set minimum value of tweets you want to get

QUERIES: List[Tuple[str, str]] = [
    ("min_faves:50 (#BTC) lang:en until:2024-07-14 since:2024-07-01", "btc.csv"),
    ("min_faves:20 (#ETH) lang:en until:2024-07-08 since:2024-07-01", "eth.csv")
    ("min_faves:20 (#USDT) lang:en until:2024-08-03 since:2024-07-01", "usdt.csv"),
    ("min_faves:20 (#BNB) lang:en until:2024-08-03 since:2024-07-01", "bnb.csv"),
    ("min_faves:50 (#XRP) lang:en until:2024-07-06 since:2024-07-01", "xrp.csv"),
    ("min_faves:20 (#ADA) lang:en until:2024-08-03 since:2024-07-01", "ada.csv"),
    ("min_faves:20 (#DOGE) lang:en until:2024-08-03 since:2024-07-01", "doge.csv"),
    ("min_faves:20 (#TAO) lang:en until:2024-08-03 since:2024-07-01", "tao.csv"),
    ("min_faves:20 (#TON) lang:en until:2024-08-03 since:2024-07-01", "ton.csv"),
    ("min_faves:20 (#TRX) lang:en until:2024-08-03 since:2024-07-01", "trx.csv"),
    ("min_faves:20 (#DOT) lang:en until:2024-08-03 since:2024-07-01", "dot.csv"),
    ("min_faves:20 (#MATIC) lang:en until:2024-08-03 since:2024-07-01", "matic.csv"),
    ("min_faves:20 (#LTC) lang:en until:2024-08-03 since:2024-07-01", "ltc.csv"),
    ("min_faves:20 (#AVAX) lang:en until:2024-08-03 since:2024-07-01", "avax.csv"),
    ("min_faves:20 (#LINK) lang:en until:2024-08-03 since:2024-07-01", "link.csv"),
    ("min_faves:20 (#SHIB) lang:en until:2024-08-03 since:2024-07-01", "shib.csv"),
    ("min_faves:20 (#BCH) lang:en until:2024-08-03 since:2024-07-01", "bch.csv"),
    ("min_faves:20 (#WBTC) lang:en until:2024-08-03 since:2024-07-01", "wbtc.csv"),
    ("min_faves:20 (#DAI) lang:en until:2024-08-03 since:2024-07-01", "dai.csv"),
    ("min_faves:20 (#XLM) lang:en until:2024-08-03 since:2024-07-01", "xlm.csv"),
    ("min_faves:20 (#UNI) lang:en until:2024-08-03 since:2024-07-01", "uni.csv"),
    ("min_faves:20 (#XMR) lang:en until:2024-08-03 since:2024-07-01", "xmr.csv"),
    ("min_faves:20 (#APT) lang:en until:2024-08-03 since:2024-07-01", "apt.csv"),
    ("min_faves:20 (#NEAR) lang:en until:2024-08-03 since:2024-07-01", "near.csv"),
    ("min_faves:20 (#VET) lang:en until:2024-08-03 since:2024-07-01", "vet.csv"),
    ("min_faves:20 (#HBAR) lang:en until:2024-08-03 since:2024-07-01", "hbar.csv"),
    ("min_faves:20 (#ICP) lang:en until:2024-08-03 since:2024-07-01", "icp.csv"),
    ("min_faves:20 (#FIL) lang:en until:2024-08-03 since:2024-07-01", "fil.csv"),
    ("min_faves:20 (#AAVE) lang:en until:2024-08-03 since:2024-07-01", "aave.csv"),
    ("min_faves:20 (#QUBIC) lang:en until:2024-08-03 since:2024-07-01", "qubic.csv"),
    ("min_faves:20 (#SYN) lang:en until:2024-08-03 since:2024-07-01", "syn.csv"),
    ("min_faves:20 (#MLT) lang:en until:2024-08-03 since:2024-07-01", "mlt.csv"),
    ("min_faves:20 (#WOO) lang:en until:2024-08-03 since:2024-07-01", "woo.csv"),
    ("min_faves:20 (#SOL) lang:en until:2024-07-06 since:2024-07-01", "sol.csv"),

]


async def get_tweets(client: Client, query: str, tweets: Optional[object]) -> object:
    if tweets is None:
        logging.info(f"Getting tweets for query: {query}")
        tweets = await client.search_tweet(query, product="Latest")
    else:
        wait_time = random.randint(5, 25)
        logging.info(
            f"Getting next tweets for query: {query} after {wait_time} seconds"
        )
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets


async def scrape_tweets(query: str, filename: str) -> None:
    client = Client(language="en-US")
    await client.login(
        auth_info_1=TWITTER_USERNAME,
        auth_info_2=TWITTER_EMAIL,
        password=TWITTER_PASSWORD,
    )
    client.save_cookies(str(COOKIES_FILE))

    tweet_count = 0
    tweets = None

    full_path = RAW_DIR / filename

    if RESUME_FILE.exists():
        with RESUME_FILE.open("r") as f:
            resume_state = json.load(f)
        if resume_state["query"] == query:
            tweet_count = resume_state["tweet_count"]
            logging.info(f"Resuming scraping for {query} from tweet {tweet_count}")

    with full_path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if tweet_count == 0:
            writer.writerow(
                ["Tweet_Count", "Username", "Text", "Created_At", "Retweets", "Likes"]
            )

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(client, query, tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                logging.warning(f"Rate limit reached. Waiting until {rate_limit_reset}")
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
                await asyncio.sleep(wait_time)
                continue
            except Exception as e:
                logging.error(f"Error fetching tweets: {str(e)}")
                await asyncio.sleep(60)
                continue

            if not tweets:
                logging.info(f"No more tweets found for query: {query}")
                break

            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count,
                    tweet.user.name,
                    tweet.text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count,
                ]
                writer.writerow(tweet_data)

            logging.info(f"Got {tweet_count} tweets for query: {query}")

            with RESUME_FILE.open("w") as f:
                json.dump({"query": query, "tweet_count": tweet_count}, f)

    logging.info(f"Done for query: {query}. {tweet_count} tweets found")
    RESUME_FILE.unlink(missing_ok=True)

    await asyncio.sleep(15)


async def main():
    for query, filename in QUERIES:
        await scrape_tweets(query, filename)


if __name__ == "__main__":
    asyncio.run(main())
