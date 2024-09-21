import asyncio
import logging
from scrap import main as scrap_main
from clean import clean_data
from sentiment import analyze_data
from ingest_curr_vals import fetch_coin_data
from correlation_analysis import analyze_data
from charts import chart

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

async def run_all_tasks():
    logging.info("Starting Twitter scraping...")
    await scrap_main()

    logging.info("Starting data cleaning...")
    clean_data()

    logging.info("Starting sentiment analysis...")
    analyze_data()

    logging.info("Starting currency data ingestion...")
    fetch_coin_data()

    logging.info("Starting correlation analysis...")
    analyze_data()

    logging.info("Starting creating charts...")
    chart()

if __name__ == "__main__":
    asyncio.run(run_all_tasks())
