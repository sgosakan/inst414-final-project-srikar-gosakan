import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def evaluate_ratios(ratios_df):
    print("Financial Ratios:")
    print(ratios_df)

def main():
    """
    Main function to load calculated financial ratios, evaluate them

    Parameters:
    None
    """
    ticker = 'AAPL'
    year = '2023'
    
    # Load calculated ratios
    ratios_df = load_data(f'data/processed/{ticker}_{year}_financial_ratios.csv')
    
    # Evaluate the financial ratios
    evaluate_ratios(ratios_df)

if __name__ == "__main__":
    main()
