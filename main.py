import asyncio
import scrap
import clean
import sentiment

def run_all_tasks():
    # Run Twitter scraping
    print("Starting Twitter scraping...")
    asyncio.run(scrap.main())

    # Run data cleaning
    print("Starting data cleaning...")
    clean.clean_data()

    # Run sentiment analysis
    print("Starting sentiment analysis...")
    sentiment.analyze_data()

if __name__ == "__main__":
    run_all_tasks()
