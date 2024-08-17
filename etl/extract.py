import os
import yfinance as yf
import logging

# Configure logging
logging.basicConfig(filename='./pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create directories for storing data
os.makedirs('./data/extracted', exist_ok=True)

def extract_yahoo_finance_data(ticker):
    """
    Extract financial data from Yahoo Finance using yfinance.

    Parameters:
    ticker (str): Stock ticker symbol of the company.

    Returns:
    dict: Dictionary containing financial data DataFrames.
    """
    logging.info(f'Starting extraction for {ticker}')
    stock = yf.Ticker(ticker)
    
    try:
        financial_data = {
            'income_statement': stock.income_stmt.T,
            'quarterly_income_statement': stock.quarterly_income_stmt.T,
            'balance_sheet': stock.balance_sheet.T,
            'quarterly_balance_sheet': stock.quarterly_balance_sheet.T,
            'cash_flow': stock.cashflow.T,
            'quarterly_cash_flow': stock.quarterly_cashflow.T
        }
    except Exception as e:
        logging.error(f'Failed to extract data for {ticker}: {e}')
        return None
    
    logging.info(f'Successfully extracted data for {ticker}')
    return financial_data

def main(ticker):
    """
    Main function to extract financial data for a specific ticker.

    Parameters:
    ticker (str): Stock ticker symbol provided by the user.
    """
    try:
        financial_data = extract_yahoo_finance_data(ticker)
        for key, df in financial_data.items():
            output_path = f'./data/extracted/{ticker}_{key}.csv'
            df.to_csv(output_path, index=True)
            logging.info(f'Saved extracted data to {output_path}')
        logging.info('Data extraction complete.')
    except Exception as e:
        logging.error(f'Error in extracting data for {ticker}: {e}')

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    main(ticker)
