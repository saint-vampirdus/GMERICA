# Modules
Collection of useful ELT modules for analyzing Gamestop

## 01_generate_ticker_data

This script retrieves historical stock data for specified tickers using Yahoo Finance's API through the yfinance library, processes it, and saves the aggregated data into a CSV file. It's designed to handle a list of tickers, ensuring the data is cleaned and formatted uniformly.

### Getting Started
#### Prerequisites
Python 3.6+: The script uses Python features that might not be compatible with older versions.
Libraries: 
yfinance for fetching stock data.
pandas for data manipulation.
datetime for handling date operations.
os and glob for file system interactions.

You can install these libraries via pip:

`sh`
`pip install yfinance pandas`

#### Configuration
Modify the ticker_list to include the stock symbols you're interested in.
Adjust start_date and end_date to define the time range for data collection. The script uses end_date as the day before the current date by default.

#### Running the Script
To run the script:

`sh`
`python 01_generate_ticker_data.py`

#### Data Processing
Data Retrieval: The script fetches daily historical data for each ticker.
Column Standardization: Ensures column names are consistent across all tickers by:
Converting to uppercase.
Removing spaces and replacing with underscores.
Truncating column names at the last underscore to handle potential duplicates.
Data Consolidation: All data is combined into one DataFrame with an additional 'TICKER' column to differentiate data sources.

#### Output
CSV File: The processed data is saved into a CSV file in the data/output directory. Old files with the same naming prefix are removed to ensure freshness of data.
Filename: The CSV file follows the naming convention gme-stock-data-START_DATE-to-END_DATE.csv. Adjust gme_ticker_file_prefix if you want a different prefix.

#### Troubleshooting
Yahoo Finance Limitations: Ensure the tickers are correctly formatted and recognized by Yahoo Finance. Some tickers might have issues with historical data availability.
Date Formats: Make sure start_date and end_date are in the correct format (YYYY-MM-DD).

## 02_generate_gme_financials.py

### Getting Started
#### Prerequisites
Python 3.6+: Ensure you have a compatible Python version.
Libraries: 
yfinance for fetching financial data.
pandas for data manipulation.
datetime for handling date operations.
os and glob for file system operations.

You can install these via pip:
`sh`
`pip install yfinance pandas`

#### Configuration
The script is configured with default date ranges and file naming conventions. Adjust start_date and end_date if you need data for a different period.

#### Running the Script
To execute:

`sh`
`python 02_generate_gme_financials.py`

#### Data Types Collected
Total Shares Outstanding: Daily data on GME's total shares.
SEC Filings: All SEC filings for GME, with their attributes flattened.
Quarterly Financials: Aggregated financial statements (balance sheet, income statement, cash flow) for each quarter.

#### Output
CSV Files: Data is saved in data/output directory:
gme-total-shares-{start_date}-to-{end_date}.csv
gme-sec-filings-{start_date}-{end_date}.csv
gme-quarterly-financials-{start_date}-to-{end_date}.csv

Old files with matching prefixes are removed before saving new data.

#### Key Functions
flatten_dict: Flattens nested dictionaries for easier DataFrame creation.
generate_csv: Handles CSV file creation and cleanup.
generate_ticker_total_shares: Retrieves and formats total shares data.
generate_ticker_sec_filings: Processes SEC filings into a DataFrame.
generate_quarterly_financials: Aggregates quarterly financial data.

#### Troubleshooting
Data Availability: Ensure you have access to the internet, as yfinance pulls data from Yahoo Finance. Some data might be incomplete due to limitations in the source.
Date Formats: The script expects start_date and end_date in YYYY-MM-DD format. Adjust dates to fit your needs or ensure historical data availability.

## 03_generate_ftd_data.py
This script aggregates Failure to Deliver (FTD) data from multiple zip files, filters it for specified stock tickers, and saves the aggregated data into a CSV file for analysis. It's designed to handle large datasets by processing each file individually and combining data into a single DataFrame.

### Getting Started
#### Prerequisites
Python 3.6+: This script uses features that might not be compatible with older Python versions.
Libraries: 
pandas for data manipulation.
zipfile for reading zip files.
os and glob for file system operations.

Ensure these libraries are installed:

`pip install pandas`

#### Configuration
Ticker List: Adjust the ticker_list to include the stock symbols you're interested in.
Date Range: Modify start_date and end_date if you need data from a different time frame. Note, this script's date range is used for naming purposes only; it doesn't filter by date within the FTD data.

#### Running the Script
To execute the script:

`python 03_generate_ftd_data.py`

#### Data Processing
Data Source: The script expects FTD data in zip files within data/input/ftd/ directory. Each zip should contain CSV files with FTD data.
File Naming Convention: Zip files should start with 'cnsfails' and end with '.zip'.
Column Filtering: Only specified columns (SETTLEMENT DATE, CUSIP, SYMBOL, QUANTITY (FAILS), DESCRIPTION, PRICE) are processed.
Ticker Filtering: Data is filtered to include only entries for tickers listed in ticker_list.

#### Output
CSV File: The processed data is saved in data/output directory. The file naming follows: gme-ftd-START_DATE-to-END_DATE.csv.
Data Cleaning: Column names are cleaned by removing spaces, parentheses, and converting to uppercase.

#### Key Functions
generate_ftd_data: Reads and filters FTD data from zip files.
generate_csv: Handles the saving of DataFrame to CSV and removal of old files.
