import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    return pd.read_csv(file_path)

def plot_ratios(ratios_df, output_path):
    """
    Plots ratios from df and saves the plot to a file.

    Parameters:
    ratios_df (pd.DataFrame): A pandas DataFrame containing financial ratios.
    output_path (str): The file path to save the generated plot.

    Returns:
    None
    """
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

if __name__ == "__main__":
    main()
