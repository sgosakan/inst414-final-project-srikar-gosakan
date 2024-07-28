import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_ratios(balance_sheet_df, income_statement_df):
    ratios = {}
    ratios['current_ratio'] = balance_sheet_df['total_current_assets'][0] / balance_sheet_df['total_current_liabilities'][0]
    ratios['debt_to_equity'] = balance_sheet_df['total_liabilities'][0] / balance_sheet_df['shareholders_equity'][0]
    ratios['profit_margin'] = income_statement_df['net_income'][0] / income_statement_df['total_revenue'][0]
    return ratios

def main():
    ticker = 'AAPL'
    year = '2023'
    
    # Load processed data
    balance_sheet_df = load_data(f'data/processed/{ticker}_{year}_balance_sheet.csv')
    income_statement_df = load_data(f'data/processed/{ticker}_{year}_income_statement.csv')
    
    # Calculate financial ratios
    ratios = calculate_ratios(balance_sheet_df, income_statement_df)
    
    # Store the calculated ratios
    ratios_df = pd.DataFrame([ratios])
    ratios_df.to_csv(f'data/processed/{ticker}_{year}_financial_ratios.csv', index=False)
    
    print("Financial ratios calculated and saved to data/processed/ directory.")

if __name__ == "__main__":
    main()
