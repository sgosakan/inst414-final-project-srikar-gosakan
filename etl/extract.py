import os
import yfinance as yf

# Create directories for storing data
os.makedirs('data/raw', exist_ok=True)

def extract_yahoo_finance_data(ticker):
    """
    Extract financial data from Yahoo Finance using yfinance.

    Parameters:
    ticker (str): Stock ticker symbol of the company.

    Returns:
    dict: Dictionary containing financial data DataFrames.
    """
    stock = yf.Ticker(ticker)
    
    financial_data = {
        'income_statement': stock.income_stmt.T,
        'quarterly_income_statement': stock.quarterly_income_stmt.T, 
        'balance_sheet': stock.balance_sheet.T,  
        'quarterly_balance_sheet': stock.quarterly_balance_sheet.T, 
        'cash_flow': stock.cashflow.T,
        'quarterly_cash_flow': stock.quarterly_cashflow.T
    }
    
    return financial_data

def main():
    ticker = 'AAPL'
    
    try:
        financial_data = extract_yahoo_finance_data(ticker)
        
        for key, df in financial_data.items():
            df.to_csv(f'data/raw/{ticker}_{key}.csv', index=True)
        
        print("Data extraction complete")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
