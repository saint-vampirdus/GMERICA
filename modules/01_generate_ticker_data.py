import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of Tickers to pull in (GME and its known ETFS)
ticker_list = ['GME', 'XRT', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']
start_date = '2016-01-01' #start date of ticker data
end_date = datetime.now() - timedelta(days=1) # pull in all data up to last close

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

def main():
    df_tickers = generate_ticker_data(ticker_list=ticker_list, 
                                      start_date=start_date,
                                      end_date=end_date)
    print(df_tickers.tail())

if __name__ == "__main__":
    main()
