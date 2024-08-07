import os
import pandas as pd

os.makedirs('data/transformed', exist_ok=True)

def process_financial_data(filepath, index_col=0):
    """
    Clean and wrangle data

    Parameters:
    filepath (str): Path to the CSV file containing raw financial data.
    index_col (int): Index column for reading the CSV file.

    Returns:
    DataFrame: Processed financial data.
    """
    df = pd.read_csv(filepath, index_col=index_col)
    df.fillna(0, inplace=True) 
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_').replace('.', '_'), inplace=True) 
    return df

def standardize_column_names(df, column_mapping):
    """
    Standardize column names based on a provided mapping.

    Parameters:
    df (DataFrame): DataFrame with raw column names.
    column_mapping (dict): Mapping of old column names to new standardized column names.

    Returns:
    DataFrame: DataFrame with standardized column names.
    """
    df.rename(columns=column_mapping, inplace=True)
    return df

def feature_engineering(df, statement_type):
    """
    Perform feature engineering on the financial data.

    Parameters:
    df (DataFrame): Financial data.
    statement_type (str): Type of financial statement (e.g., 'quarterly' or 'annual').

    Returns:
    DataFrame: Enhanced financial data with additional features.
    """
    if 'total_revenue' in df.columns:
        df['revenue_growth'] = df['total_revenue'].pct_change()
    if 'total_expenses' in df.columns:
        df['expense_ratio'] = df['total_expenses'] / df['total_revenue']
    
    if statement_type == 'quarterly':
        if 'net_income' in df.columns:
            df['net_income_margin'] = df['net_income'] / df['total_revenue']
    
    return df

def main():
    ticker = 'AAPL'
    data_types = {
        'income_statement': 'annual',
        'quarterly_income_statement': 'quarterly',
        'balance_sheet': 'annual',
        'quarterly_balance_sheet': 'quarterly',
        'cash_flow': 'annual',
        'quarterly_cash_flow': 'quarterly'
    }
    
    # Example column mapping (needs to be adjusted based on actual data)
    column_mapping = {
        'total_revenue': 'total_revenue',
        'total_expenses': 'total_expenses',
        'net_income': 'net_income',
        'free_cash_flow': 'free_cash_flow',
        'repurchase_of_capital_stock': 'repurchase_of_capital_stock',
        'repayment_of_debt': 'repayment_of_debt',
        'issuance_of_debt': 'issuance_of_debt',
        'capital_expenditure': 'capital_expenditure',
        'end_cash_position': 'end_cash_position',
        'beginning_cash_position': 'beginning_cash_position'
    }
    
    for data_type, statement_type in data_types.items():
        # Process data
        processed_df = process_financial_data(f'data/raw/{ticker}_{data_type}.csv', index_col=0)
        
        standardized_df = standardize_column_names(processed_df, column_mapping)
        
        enhanced_df = feature_engineering(standardized_df, statement_type)
        
        enhanced_df.to_csv(f'data/transformed/{ticker}_{data_type}.csv', index=True)
    
    print("Data transformation and feature engineering complete. Data saved to data/transformed/ directory.")

if __name__ == "__main__":
    main()
