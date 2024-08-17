import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='./pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create directory for storing transformed data
os.makedirs('./data/transformed', exist_ok=True)

def process_financial_data(filepath):
    """
    Process financial data by cleaning and standardizing it.

    Parameters:
    filepath (str): Path to the raw financial data CSV file.

    Returns:
    DataFrame: Processed financial data.
    """
    logging.info(f'Processing data from file: {filepath}')
    df = pd.read_csv(filepath, index_col=0)
    
    # Example cleaning and transformation operations
    df.fillna(0, inplace=True)
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_').replace('.', '_'), inplace=True)
    
    return df

def feature_engineering(df, statement_type):
    """
    Perform feature engineering on financial data.

    Parameters:
    df (DataFrame): Financial data.
    statement_type (str): Type of financial statement (annual or quarterly).

    Returns:
    DataFrame: Financial data with new features added.
    """
    logging.info(f'Performing feature engineering for {statement_type} data.')
    
    if 'total_revenue' in df.columns:
        df['revenue_growth'] = df['total_revenue'].pct_change()
    if 'total_expenses' in df.columns:
        df['expense_ratio'] = df['total_expenses'] / df['total_revenue']
    if statement_type == 'quarterly' and 'net_income' in df.columns:
        df['net_income_margin'] = df['net_income'] / df['total_revenue']
    
    df.dropna(inplace=True)
    return df

def main(ticker):
    """
    Main function to transform financial data for a specific ticker.

    Parameters:
    ticker (str): Stock ticker symbol provided by the user.
    """
    data_types = {
        'income_statement': 'annual',
        'quarterly_income_statement': 'quarterly',
        'balance_sheet': 'annual',
        'quarterly_balance_sheet': 'quarterly',
        'cash_flow': 'annual',
        'quarterly_cash_flow': 'quarterly'
    }
    
    try:
        for data_type, statement_type in data_types.items():
            input_path = f'./data/extracted/{ticker}_{data_type}.csv'
            output_path = f'./data/transformed/{ticker}_{data_type}.csv'
            
            processed_df = process_financial_data(input_path)
            enhanced_df = feature_engineering(processed_df, statement_type)
            enhanced_df.to_csv(output_path, index=True)
            
            logging.info(f'Saved transformed data to {output_path}')
        logging.info('Data transformation complete.')
    except Exception as e:
        logging.error(f'Error in transforming data for {ticker}: {e}')

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    main(ticker)
