import os
import zipfile
import pandas as pd
import os
import glob

### INPUT VARIABLES ###
start_date = '2016-01-01'  # Start date of ticker data
end_date = '2024-09-30'
gme_ftd_file_prefix = 'gme-ftd-'
gme_ftd_data_file_name = f'{gme_ftd_file_prefix}-{start_date}-to-{end_date}.csv'
keep_cols = ['SETTLEMENT DATE', 'CUSIP', 'SYMBOL', 'QUANTITY (FAILS)', 'DESCRIPTION', 'PRICE']
ticker_list = ['GME', 'XRT', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']

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

#### MODULE FUNCTIONS ####
def generate_ftd_data(ticker_list):
    """
    Generate a DataFrame containing failure to deliver (FTD) data for specified tickers.

    This function reads FTD data from zip files within a specified directory. Each zip file is expected
    to contain CSV files with FTD data. The function processes these files, filters the data for the 
    provided tickers, and combines them into a single DataFrame.

    Parameters:
    ticker_list (list): A list of ticker symbols to filter the data by.

    Returns:
    pd.DataFrame: A DataFrame containing FTD data for the specified tickers. The DataFrame includes
    columns: ['SETTLEMENT DATE', 'CUSIP', 'SYMBOL', 'QUANTITY (FAILS)', 'DESCRIPTION', 'PRICE'].

    Note:
    - The function assumes the input directory structure and file naming convention. Adjust 'input_dir' 
      if the directory path changes.
    - The function uses ISO-8859-1 encoding to read CSVs. Modify if a different encoding is used.
    - Files are skipped if they do not match the expected naming convention ('cnsfails' prefix and .zip extension).
    - The function filters for tickers case-sensitively. If case-insensitive filtering is required, 
      convert both DataFrame's SYMBOL column and ticker_list to the same case before filtering.
    - The function creates a new DataFrame for each file, which might be memory-intensive for large datasets.
      Consider processing in chunks for very large datasets.

    Example:
        >>> tickers = ['GME', 'XRT']
        >>> ftd_data = generate_ftd_data(tickers)
        >>> print(ftd_data.head())
    """
    keep_cols = ['SETTLEMENT DATE', 'CUSIP', 'SYMBOL', 'QUANTITY (FAILS)', 'DESCRIPTION', 'PRICE']
    input_dir = 'data/input/ftd/'
    df_ftd_combined = pd.DataFrame()

    for filename in os.listdir(input_dir):
        if filename.endswith('.zip') and filename.startswith('cnsfails'):
            file_path = os.path.join(input_dir, filename)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    with zip_ref.open(file) as csv_file:
                        df_ftd = pd.read_csv(csv_file, sep='|', encoding='ISO-8859-1', engine='python', usecols=keep_cols)
                        df_ftd_combined = pd.concat([df_ftd_combined, df_ftd], ignore_index=True)
                        df_ftd_combined = df_ftd_combined[df_ftd_combined['SYMBOL'].isin(ticker_list)]
                        print(f"Processed {filename}")
        else:
            print(f"Skipping {filename} as it does not match the expected naming convention.")
    df_ftd_combined.columns = [col.replace(' ', '_').replace('(', '').replace(')', '').upper() for col in df_ftd_combined.columns]
    return df_ftd_combined

# Save the combined DataFrame to a single CSV file

def main():
    """
    Main function to orchestrate the data retrieval and CSV generation process.
    
    Calls functions to fetch ticker data and save it as a CSV, using predefined
    or global variables for tickers, start date, and end date.
    """
    df_ftd = generate_ftd_data(ticker_list=ticker_list)
    
    generate_csv(df=df_ftd, 
                 file_prefix=gme_ftd_file_prefix, 
                 file_name=gme_ftd_data_file_name, 
                 remove_old=True)

if __name__ == "__main__":
    main()