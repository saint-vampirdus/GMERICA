import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import glob

#### INPUT VARIABLES ####
gme_financials = yf.Ticker("GME")
start_date = '2016-01-01'  # Start date of ticker data
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Pull in all data up to last close
total_shares_file_prefix = 'gme-total-shares'
total_shares_file_name = f'{total_shares_file_prefix}-{start_date}-to-{end_date}.csv'
sec_filings_file_prefix = 'gme-sec-filings'
sec_filings_file_name = f'{sec_filings_file_prefix}-{start_date}-{end_date}.csv'

#### UTILITY FUNCTIONS ####
def flatten_dict(d, parent_key='', sep='_'):
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
    Save the DataFrame containing ticker data to a CSV file.

    This function creates a CSV file with the ticker data, ensures a clean environment
    by removing any previous CSV files with similar naming, and provides feedback on 
    where the data is saved.

    Parameters:
    df_tickers (pd.DataFrame): DataFrame containing ticker data to be saved.

    Returns:
    None: This function saves the DataFrame to disk and prints the path.
    """
    # Determine the path where data should be saved
    data_root = 'data'  # Assuming 'data' is the root folder for data
   
    if not os.path.exists(data_root):
        os.makedirs(data_root)

    # Generate filename
    full_path = os.path.join(data_root, file_name)

    # Delete existing files that start with 'ticker-data-'
    if remove_old:
        for file in glob.glob(os.path.join(data_root, f'{file_prefix}-*.csv')):
            os.remove(file)

    # Export DataFrame to CSV
    df.to_csv(full_path, index=False)

    print(f"Data exported to {full_path}")

##### FINANCIAL DATA FUNCTIONS ####

def generate_ticker_total_shares(ticker, start_date, end_date):
    df = ticker.get_shares_full(start=start_date, end=end_date).to_frame(name='TOTAL_SHARES')
    df = df.reset_index()
    df = df.rename(columns={'index': 'DATE'})
    return df

def generate_ticker_sec_filings(ticker):
    sec_filings_flat = [flatten_dict(d, sep='_') for d in ticker.sec_filings]
    df = pd.DataFrame(sec_filings_flat)
    df = df.reset_index(drop=True)
    df.columns = [col.upper() for col in df.columns]
    return df


def main():
    """
    Main function to orchestrate the data retrieval and CSV generation process.
    
    Calls functions to fetch ticker data and save it as a CSV, using predefined
    or global variables for tickers, start date, and end date.
    """
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

if __name__ == "__main__":
    main()

