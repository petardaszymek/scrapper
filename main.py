import asyncio
from twikit import Client, TooManyRequests
import csv
from datetime import datetime
from configparser import ConfigParser
from random import randint
import time

MINIMUM_TWEETS = 5000

# List of queries and corresponding filenames for each hashtag4
QUERIES = [
    ('min_faves:50 (#BTC) lang:en until:2024-08-03 since:2024-07-01', 'btc.csv'),
    ('min_faves:50 (#ETH) lang:en until:2024-08-03 since:2024-07-01', 'eth.csv'),
    ('min_faves:50 (#USDT) lang:en until:2024-08-03 since:2024-07-01', 'usdt.csv'),
    ('min_faves:50 (#BNB) lang:en until:2024-08-03 since:2024-07-01', 'bnb.csv'),
    ('min_faves:50 (#XRP) lang:en until:2024-08-03 since:2024-07-01', 'xrp.csv'),
    ('min_faves:50 (#ADA) lang:en until:2024-08-03 since:2024-07-01', 'ada.csv'),
    ('min_faves:50 (#DOGE) lang:en until:2024-08-03 since:2024-07-01', 'doge.csv'),
    ('min_faves:50 (#SOL) lang:en until:2024-08-03 since:2024-07-01', 'sol.csv'),
    ('min_faves:50 (#TON) lang:en until:2024-08-03 since:2024-07-01', 'ton.csv'),
    ('min_faves:50 (#TRX) lang:en until:2024-08-03 since:2024-07-01', 'trx.csv'),
    ('min_faves:50 (#DOT) lang:en until:2024-08-03 since:2024-07-01', 'dot.csv'),
    ('min_faves:50 (#MATIC) lang:en until:2024-08-03 since:2024-07-01', 'matic.csv'),
    ('min_faves:50 (#LTC) lang:en until:2024-08-03 since:2024-07-01', 'ltc.csv'),
    ('min_faves:50 (#AVAX) lang:en until:2024-08-03 since:2024-07-01', 'avax.csv'),
    ('min_faves:50 (#LINK) lang:en until:2024-08-03 since:2024-07-01', 'link.csv'),
    ('min_faves:50 (#SHIB) lang:en until:2024-08-03 since:2024-07-01', 'shib.csv'),
    ('min_faves:50 (#BCH) lang:en until:2024-08-03 since:2024-07-01', 'bch.csv'),
    ('min_faves:50 (#WBTC) lang:en until:2024-08-03 since:2024-07-01', 'wbtc.csv'),
    ('min_faves:50 (#DAI) lang:en until:2024-08-03 since:2024-07-01', 'dai.csv'),
    ('min_faves:50 (#XLM) lang:en until:2024-08-03 since:2024-07-01', 'xlm.csv'),
    ('min_faves:50 (#UNI) lang:en until:2024-08-03 since:2024-07-01', 'uni.csv'),
    ('min_faves:50 (#XMR) lang:en until:2024-08-03 since:2024-07-01', 'xmr.csv'),
    ('min_faves:50 (#APT) lang:en until:2024-08-03 since:2024-07-01', 'apt.csv'),
    ('min_faves:50 (#NEAR) lang:en until:2024-08-03 since:2024-07-01', 'near.csv'),
    ('min_faves:50 (#VET) lang:en until:2024-08-03 since:2024-07-01', 'vet.csv'),
    ('min_faves:50 (#HBAR) lang:en until:2024-08-03 since:2024-07-01', 'hbar.csv'),
    ('min_faves:50 (#ICP) lang:en until:2024-08-03 since:2024-07-01', 'icp.csv'),
    ('min_faves:50 (#FIL) lang:en until:2024-08-03 since:2024-07-01', 'fil.csv'),
    ('min_faves:50 (#AAVE) lang:en until:2024-08-03 since:2024-07-01', 'aave.csv'),
    ('min_faves:50 (#TAO) lang:en until:2024-08-03 since:2024-07-01', 'tao.csv'),
    ('min_faves:50 (#QUBIC) lang:en until:2024-08-03 since:2024-07-01', 'qubic.csv'),
    ('min_faves:50 (#SYN) lang:en until:2024-08-03 since:2024-07-01', 'syn.csv'),
    ('min_faves:50 (#NMT) lang:en until:2024-08-03 since:2024-07-01', 'nmt.csv'),
    ('min_faves:50 (#MLT) lang:en until:2024-08-03 since:2024-07-01', 'mlt.csv'),
    ('min_faves:50 (#WOO) lang:en until:2024-08-03 since:2024-07-01', 'woo.csv')

]

# Load login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']


async def get_tweets(client, query, tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets for query: {query}')
        tweets = await client.search_tweet(query, product='Latest')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets for query: {query} after {wait_time} seconds')
        time.sleep(wait_time)
        tweets = await tweets.next()

    return tweets


async def scrape_tweets(query, filename):
    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies('cookies.json')

    # Load cookies for authentication
    client.load_cookies('cookies.json')

    tweet_count = 0
    tweets = None

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_Count', 'Username', 'Text', 'Created_At', 'Retweets', 'Likes'])

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(client, query, tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found for query: {query}')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count,
                          tweet.favorite_count]
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets for query: {query}')

    print(f'{datetime.now()} - Done for query: {query}. {tweet_count} tweets found')

    # Wait for 15 seconds before the next query
    await asyncio.sleep(15)


async def main():
    for query, filename in QUERIES:
        await scrape_tweets(query, filename)


# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
