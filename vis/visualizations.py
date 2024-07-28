import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def plot_ratios(ratios_df, output_path):
    ratios_df.plot(kind='bar', figsize=(10, 6))
    plt.title('Financial Ratios')
    plt.xlabel('Ratios')
    plt.ylabel('Values')
    plt.xticks(rotation=0)
    plt.savefig(output_path)
    plt.show()

def main():
    ticker = 'AAPL'
    year = '2023'
    
    # Load calculated ratios
    ratios_df = load_data(f'data/processed/{ticker}_{year}_financial_ratios.csv')
    
    # Plot and save the financial ratios
    plot_ratios(ratios_df, f'data/processed/{ticker}_{year}_financial_ratios.png')
    
    print("Financial ratios visualized and saved to data/processed/ directory.")

if __name__ == "__main__":
    main()
