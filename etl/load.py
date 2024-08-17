import os
import shutil
import logging

# Configure logging
logging.basicConfig(filename='./pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create directory for storing loaded data
os.makedirs('./data/loaded', exist_ok=True)

def move_transformed_data(ticker):
    """
    Move transformed data from the 'transformed' directory to the 'loaded' directory.
    """
    logging.info(f'Moving transformed data to loaded directory for ticker: {ticker}')
    source_dir = './data/transformed'
    dest_dir = './data/loaded'
    
    for file_name in os.listdir(source_dir):
        if file_name.startswith(ticker):
            full_file_name = os.path.join(source_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.move(full_file_name, dest_dir)
                logging.info(f'Moved {file_name} to {dest_dir}')
    
    logging.info('Data loading complete.')

def main(ticker):
    """
    Main function to load transformed data for a specific ticker.

    Parameters:
    ticker (str): Stock ticker symbol provided by the user.
    """
    try:
        move_transformed_data(ticker)
    except Exception as e:
        logging.error(f'Error in loading data for {ticker}: {e}')

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    main(ticker)
