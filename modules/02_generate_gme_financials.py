import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import glob

#### INPUT VARIABLES ####
start_date = '2016-01-01'  # Start date of ticker data
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Pull in all data up to last close
total_shares_file_prefix = 'gme-total-shares'
total_shares_file_name = f'{total_shares_file_prefix}-{start_date}-to-{end_date}.csv'
sec_filings_file_prefix = 'gme-sec-filings'
sec_filings_file_name = f'{sec_filings_file_prefix}-{start_date}-{end_date}.csv'
quarterly_financials_file_prefix = 'gme-quarterly-financials'
quarterly_financials_file_name = f'{quarterly_financials_file_prefix}-{start_date}-to-{end_date}.csv'

#### UTILITY FUNCTIONS ####
def flatten_dict(d, parent_key='', sep='_'):
    """
    Recursively flatten a nested dictionary into a single-level dictionary.

    Args:
    d (dict): The dictionary to flatten.
    parent_key (str, optional): The string to prepend to keys that are nested. Defaults to ''.
    sep (str, optional): Separator used to concatenate parent_key and current key. Defaults to '_'.

    Returns:
    dict: Flattened dictionary where keys are concatenated with sep if nested.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def generate_csv(df, file_prefix, file_name, remove_old=True):
    """
    Save a DataFrame to CSV, optionally removing old related files.

    Args:
    df (pd.DataFrame): DataFrame to save.
    file_prefix (str): Prefix for file names when removing old files.
    file_name (str): Name of the CSV file to save.
    remove_old (bool): If True, remove existing files with the given prefix. Defaults to True.

    Returns:
    None: This function prints a message about where the data was saved.
    """
    # Determine the path where data should be saved
    data_root = 'data/output'  # Assuming 'data' is the root folder for data
   
    if not os.path.exists(data_root):
        os.makedirs(data_root)

    # Generate filename
    full_path = os.path.join(data_root, file_name)

    # Delete existing files that start with the specified prefix
    if remove_old:
        for file in glob.glob(os.path.join(data_root, f'{file_prefix}-*.csv')):
            os.remove(file)

    # Export DataFrame to CSV
    df.to_csv(full_path, index=False)

    print(f"Data exported to {full_path}")

##### FINANCIAL DATA FUNCTIONS ####

def generate_ticker_total_shares(ticker, start_date, end_date):
    """
    Retrieve and format total shares data for a ticker over a given date range.

    This function fetches the total shares outstanding for each date within
    the specified range from the given ticker object, formats it into a DataFrame,
    and ensures date is a column for clarity.

    Args:
        ticker (yf.Ticker): A yfinance Ticker object representing the stock.
        start_date (str): Start date for the data retrieval in 'YYYY-MM-DD' format.
        end_date (str): End date for the data retrieval in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame with columns 'DATE' and 'TOTAL_SHARES'.
    """
    df = ticker.get_shares_full(start=start_date, end=end_date).to_frame(name='TOTAL_SHARES')
    df = df.reset_index()
    df = df.rename(columns={'index': 'DATE'})
    return df

def generate_ticker_sec_filings(ticker):
    """
    Generate a DataFrame from SEC filings data for a given ticker.

    This function flattens the nested structure of SEC filings data, converts
    it into a DataFrame, and prepares it for analysis or storage.

    Args:
        ticker (yf.Ticker): A yfinance Ticker object from which to get SEC filings.

    Returns:
        pd.DataFrame: DataFrame where each row represents a filing with flattened attributes.
    """
    sec_filings_flat = [flatten_dict(d, sep='_') for d in ticker.sec_filings]
    df = pd.DataFrame(sec_filings_flat)
    df = df.reset_index(drop=True)
    df.columns = [col.upper() for col in df.columns]
    return df

def generate_quarterly_financials(ticker):
    """
    Aggregate and format quarterly financial statements into a single DataFrame.

    This function retrieves quarterly financial data from the balance sheet,
    income statement, and cash flow statement, concatenates them, and prepares
    it for further analysis or storage.

    Args:
        ticker (yf.Ticker): A yfinance Ticker object for retrieving financial data.

    Returns:
        pd.DataFrame: Combined DataFrame of quarterly financials with an outer join.
    """
    df_balance = ticker.quarterly_balance_sheet.reset_index()
    df_income = ticker.quarterly_income_stmt.reset_index()
    df_cashflow = ticker.quarterly_cashflow.reset_index()

    df_final = pd.concat([df_balance, df_income, df_cashflow], axis=0, join='outer')
    return df_final

def main():

    gme_financials = yf.Ticker("GME")

    df_total_shares = generate_ticker_total_shares(ticker=gme_financials, 
                                                   start_date=start_date, 
                                                   end_date=end_date)
    
    generate_csv(df=df_total_shares, 
                 file_prefix=total_shares_file_prefix, 
                 file_name=total_shares_file_name, 
                 remove_old=True)
    
    df_sec_filings = generate_ticker_sec_filings(ticker=gme_financials)

    generate_csv(df=df_sec_filings, 
                 file_prefix=sec_filings_file_prefix, 
                 file_name=sec_filings_file_name, 
                 remove_old=True)

    
    gme_quarterly_financials_df = generate_quarterly_financials(ticker=gme_financials)
    generate_csv(df=gme_quarterly_financials_df, 
                 file_prefix=quarterly_financials_file_prefix, 
                 file_name=quarterly_financials_file_name, 
                 remove_old=True)
    
if __name__ == "__main__":
    main()

