import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import glob

#### INPUT VARIABLES ####
ticker_list = ['GME', 'XRT', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']
start_date = '2016-01-01'  # Start date of ticker data
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Pull in all data up to last close
gme_ticker_file_prefix = 'gme-stock-data'
gme_ticker_data_file_name = f'{gme_ticker_file_prefix}-{start_date}-to-{end_date}.csv'

#### UTILITY FUNCTIONS ####
def generate_csv(df, file_prefix, file_name, remove_old=True):
    """
    Save a DataFrame to a CSV file, optionally removing old related files.

    This function performs the following tasks:
    - Creates a CSV file in the specified directory with the provided data.
    - Ensures a clean environment by removing old CSV files matching the `file_prefix` if `remove_old` is True.
    - Provides feedback on where the data was saved.

    Parameters:
    df (pd.DataFrame): DataFrame to be saved as CSV.
    file_prefix (str): The prefix used for identifying old files to remove.
    file_name (str): The name of the CSV file to be created.
    remove_old (bool): If True, removes existing files with the given prefix. Defaults to True.

    Returns:
    None: This function operates in-place, saving the DataFrame and removing files as needed.
    """
    
    # Determine the path where data should be saved
    data_root = 'data/output'  # Assuming 'data' is the root folder for data
   
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

def generate_ticker_data(ticker_list, start_date, end_date):
    """
    Generate a DataFrame containing financial data for multiple tickers.

    This function retrieves historical market data for each ticker in the provided list,
    standardizes the column names, and combines the data into a single DataFrame.

    Parameters:
    ticker_list (list): List of string ticker symbols.
    start_date (str): Start date in 'YYYY-MM-DD' format.
    end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
    pd.DataFrame: A DataFrame with all ticker data combined, where each row represents
                  a day's data for one of the tickers, and includes a 'TICKER' column 
                  to identify which ticker the row belongs to.
    """
    df_list = []
    for ticker in ticker_list:
        # Download data
        df_ticker = yf.download(ticker, start=start_date, end=end_date)
        
        # Clean and standardize column names
        df_ticker.columns = ['_'.join(col).strip() for col in df_ticker.columns.values]
        df_ticker = df_ticker.reset_index().rename_axis(None, axis=1)
        df_ticker.columns = [col.upper() for col in df_ticker.columns]
        df_ticker = df_ticker.rename(columns=lambda x: x.replace(' ', '_'))
        
        # Remove everything after the last underscore in column names
        df_ticker.columns = [col.rsplit('_', 1)[0] for col in df_ticker.columns]
        
        # Add the ticker name as a column
        df_ticker['TICKER'] = ticker
        
        # Append the processed dataframe to the list
        df_list.append(df_ticker)

    # Concatenate all dataframes in the list into one
    df_tickers = pd.concat(df_list, ignore_index=True)

    return df_tickers


def main():
    """
    Main function to orchestrate the data retrieval and CSV generation process.
    
    Calls functions to fetch ticker data and save it as a CSV, using predefined
    or global variables for tickers, start date, and end date.
    """
    df_tickers = generate_ticker_data(ticker_list=ticker_list, 
                                      start_date=start_date,
                                      end_date=end_date)
    
    generate_csv(df=df_tickers, 
                 file_prefix=gme_ticker_file_prefix, 
                 file_name=gme_ticker_data_file_name, 
                 remove_old=True)

if __name__ == "__main__":
    main()