import os
import json
import pandas as pd

# Create directory for storing processed data
os.makedirs('data/processed', exist_ok=True)

# Function to load JSON data from file
def load_json_data(filepath):
    """
    Loads JSON data from a specified file.
    
    Parameters:
    filepath (str): The path to the JSON file to be loaded.

    Returns:
    dict or list: The data from the JSON file, parsed into a Python dictionary or list.
    """
    with open(filepath, 'r') as f:
        return json.load(f)

# Function to clean and wrangle balance sheet data
def process_balance_sheet(data):
    """
    Processes balance sheet data into a pandas DataFrame.

    Parameters:
    data (dict): A dictionary containing balance sheet data.

    Returns:
    pd.DataFrame: A pandas DataFrame with the processed balance sheet data.
    """
    df = pd.DataFrame([data])
    df.fillna(0, inplace=True)  # Handle missing values
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True) 
    return df

# Function to clean and wrangle income statement data
def process_income_statement(data):
    """
    Processes income statement data into a pandas dataframe.
    Parameters:
    data (dict): A dictionary containing income statement data.

    Returns:
    pd.DataFrame: A pandas DataFrame with the processed income statement data.
"""
    df = pd.DataFrame([data])
    df.fillna(0, inplace=True)  
    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)  
    return df

# Main function to transform and load data
def main():
    ticker = 'AAPL'
    year = '2023'
    
    # Load raw data
    balance_sheet_data = load_json_data(f'data/raw/{ticker}_{year}_balance_sheet.json')
    income_statement_data = load_json_data(f'data/raw/{ticker}_{year}_income_statement.json')
    
    # Process data
    balance_sheet_df = process_balance_sheet(balance_sheet_data)
    income_statement_df = process_income_statement(income_statement_data)
    
    # Save processed data
    balance_sheet_df.to_csv(f'data/processed/{ticker}_{year}_balance_sheet.csv', index=False)
    income_statement_df.to_csv(f'data/processed/{ticker}_{year}_income_statement.csv', index=False)


if __name__ == "__main__":
    main()
