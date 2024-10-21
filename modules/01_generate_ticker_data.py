import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import glob

# List of Tickers to pull in (GME and its known ETFS)
ticker_list = ['GME', 'XRT', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']
start_date = '2016-01-01'  # Start date of ticker data
end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  # Pull in all data up to last close

def generate_ticker_data(ticker_list, start_date, end_date):
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

def generate_ticker_csv(df_tickers):
    # Determine the path where data should be saved
    data_root = 'data'  # Assuming 'data' is the root folder for data
    if not os.path.exists(data_root):
        os.makedirs(data_root)

    # Generate filename
    filename = f'ticker-data-{start_date}-{end_date}.csv'
    full_path = os.path.join(data_root, filename)

    # Delete existing files that start with 'ticker-data-'
    for file in glob.glob(os.path.join(data_root, 'ticker-data-*.csv')):
        os.remove(file)

    # Export DataFrame to CSV
    df_tickers.to_csv(full_path, index=False)

    print(f"Data exported to {full_path}")

def main():
    df_tickers = generate_ticker_data(ticker_list=ticker_list, 
                                      start_date=start_date,
                                      end_date=end_date)
    
    generate_ticker_csv(df_tickers)

if __name__ == "__main__":
    main()