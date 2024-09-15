# Cryptocurrency Sentiment Analysis

## Overview

This project analyzes sentiment in cryptocurrency-related tweets and correlates it with cryptocurrency price movements. It scrapes tweets, performs sentiment analysis, and compares the results with real-time cryptocurrency price data.

## Features

- Tweet scraping for multiple cryptocurrencies
- Data cleaning and preprocessing
- Sentiment analysis using VADER
- Cryptocurrency price data fetching
- Correlation of sentiment with price movements

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-sentiment-analysis.git
   cd crypto-sentiment-analysis

2. Create and activate a virtual environment (optional but recommended):
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install required packages:
   ```bash
    pip install -r requirements.txt
4. Set up Twitter API credentials in config.py.



## Usage

1. Run the main script:
   ```bash
    python main.py
   
This executes the following pipeline:

Tweet scraping
Data cleaning
Sentiment analysis
Cryptocurrency price data fetching

Results are saved in these directories:

./raw/: Raw tweet data
./clean/: Cleaned tweet data
./sentiment/: Sentiment analysis results
./currency_vals/: Cryptocurrency price data

Project Structure

main.py: Orchestrates the data pipeline
scrap.py: Handles tweet scraping
clean.py: Preprocesses scraped data
sentiment.py: Performs sentiment analysis
ingest_curr_vals.py: Fetches cryptocurrency prices
config.py: Project configuration and settings

Dependencies
Main libraries used:

twikit: Tweet scraping
pandas: Data manipulation
vaderSentiment: Sentiment analysis
pycoingecko: Cryptocurrency data fetching

For a full list, see requirements.txt.
Configuration
Edit config.py to set:

API credentials
File paths
Cryptocurrency list
Date ranges for data collection

Data Flow

scrap.py collects tweets and saves raw data.
clean.py processes raw data, removing noise and irrelevant information.
sentiment.py analyzes cleaned data for sentiment.
ingest_curr_vals.py fetches corresponding cryptocurrency prices.
Results are saved for further analysis or visualization.

Output

CSV files containing processed tweets with sentiment scores
CSV files with daily aggregated sentiment
CSV files of cryptocurrency price data



