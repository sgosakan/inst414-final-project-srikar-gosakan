import pandas as pd
import matplotlib.pyplot as plt
import os
import logging

# Configure logging
logging.basicConfig(filename='./pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

os.makedirs('./data/visualizations', exist_ok=True)

def load_data(file_path):
    """
    Load data from CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    DataFrame: Loaded data.
    """
    logging.info(f'Loading data from {file_path}')
    return pd.read_csv(file_path, index_col=0)

def plot_forecast_vs_actual(training_data, forecast_data, metric, ticker, output_path):
    """
    Plot training data forecast vs. actual values.

    Parameters:
    training_data (DataFrame): Actual training data.
    forecast_data (DataFrame): Forecasted data.
    output_path (str): Path to save the plot.
    """
    plt.figure(figsize=(10, 6))
    actual_values = training_data[metric] / 1e6
    forecasted_values = forecast_data[metric] / 1e6
    plt.plot(training_data.index, actual_values, label='Actual Total Revenue', color='blue')
    plt.plot(forecast_data.index, forecasted_values, label='Forecasted Total Revenue', linestyle='--', color='orange')
    plt.title(f"{ticker} Training Data Joined with Actual")
    plt.xlabel('Date')
    plt.ylabel('Total Revenue in Millions')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    logging.info(f'Saved Training Data Forecast vs. Actual plot to {output_path}')

def merge_data(revenue_df, debt_df):
    """
    Merge revenue and debt data into a single DataFrame.

    Parameters:
    revenue_df (DataFrame): DataFrame containing total revenue data.
    debt_df (DataFrame): DataFrame containing total debt data.

    Returns:
    DataFrame: Merged DataFrame with both revenue and debt.
    """
    merged_df = pd.merge(revenue_df, debt_df, left_index=True, right_index=True, how='inner')
    return merged_df

def plot_time_series(df, ticker, output_path):
    """
    Plot time series of total revenue and total debt.

    Parameters:
    df (DataFrame): Financial data.
    ticker (str): Stock ticker symbol.
    output_path (str): Path to save the plot.
    """
    df.sort_index(inplace=True)
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['total_revenue'], label='Total Revenue (Billions)', color='blue')
    plt.plot(df.index, df['total_debt'], label='Total Debt (Billions)', color='red')
    plt.title(f'{ticker}: Total Revenue and Total Debt Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount (Billions)')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    logging.info(f'Saved Time Series of Total Revenue and Total Debt plot to {output_path}')

def plot_historical_vs_forecast(df, forecast_df, ticker, output_path):
    """
    Plot historical and forecasted data for total revenue and total debt.

    Parameters:
    df (DataFrame): Historical financial data.
    forecast_df (DataFrame): Forecasted financial data.
    ticker (str): Stock ticker symbol.
    output_path (str): Path to save the plot.
    """
    plt.figure(figsize=(10, 6))
    
    df = df.sort_index()
    forecast_df = forecast_df.sort_index()
    
    combined_df = pd.concat([df[['total_revenue', 'total_debt']], forecast_df[['total_revenue', 'total_debt']]], axis=0)
    combined_df = combined_df.sort_index()

    # Plot historical data
    plt.plot(combined_df.index, combined_df['total_revenue'], label='Historical & Forecasted Total Revenue', color='blue')
    plt.plot(combined_df.index, combined_df['total_debt'], label='Historical & Forecasted Total Debt', color='red')
    
    plt.title(f'{ticker}: Historical vs. Forecasted Total Revenue and Total Debt')
    plt.xlabel('Date')
    plt.ylabel('Amount (Billions)')
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    logging.info(f'Saved Historical vs. Forecasted plot to {output_path}')
    
def main():
    """
    Main function to create visualizations for a specific ticker.

    Parameters:
    ticker (str): Stock ticker symbol provided by the user.
    """
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    
    try:
        # Load processed data
        training_data = load_data(f'./data/outputs/{ticker}_quarterly_income_statement_training_data.csv')
        forecast_data = load_data(f'./data/outputs/{ticker}_quarterly_income_statement_revenue_forecast.csv')
        # Load historical data from income statement and balance sheet
        revenue_df = load_data(f'./data/loaded/{ticker}_quarterly_income_statement.csv')
        debt_df = load_data(f'./data/loaded/{ticker}_quarterly_balance_sheet.csv')

        # Select only the relevant columns
        revenue_df = revenue_df[['total_revenue']]
        debt_df = debt_df[['total_debt']]

        # Merge the data
        combined_df = merge_data(revenue_df, debt_df)
        
        # Generate and save visualizations
        plot_forecast_vs_actual(training_data, forecast_data, 'total_revenue', ticker, f'./data/visualizations/{ticker}_forecast_vs_actual.png')
        plot_time_series(combined_df, ticker, f'./data/visualizations/{ticker}_revenue_debt_time_series.png')
        
        historical_revenue_df = load_data(f'./data/loaded/{ticker}_quarterly_income_statement.csv')
        historical_debt_df = load_data(f'./data/loaded/{ticker}_quarterly_balance_sheet.csv')

        # Load forecasted data
        forecast_revenue_df = load_data(f'./data/outputs/{ticker}_quarterly_income_statement_revenue_forecast.csv')
        forecast_debt_df = load_data(f'./data/outputs/{ticker}_quarterly_balance_sheet_debt_forecast.csv')

        # Select only the relevant columns
        historical_revenue_df = historical_revenue_df[['total_revenue']]
        historical_debt_df = historical_debt_df[['total_debt']]

        # Merge historical data into a single DataFrame
        historical_df = pd.merge(historical_revenue_df, historical_debt_df, left_index=True, right_index=True, how='inner')

        # Merge forecasted data into a single DataFrame
        forecast_df = pd.merge(forecast_revenue_df, forecast_debt_df, left_index=True, right_index=True, how='inner')

        # Generate and save the comparison plot
        plot_historical_vs_forecast(historical_df, forecast_df, ticker, f'./data/visualizations/{ticker}_historical_vs_forecast.png')

        logging.info('Visualization creation complete.')
    except Exception as e:
        logging.error(f'Error in creating visualizations for {ticker}: {e}')

if __name__ == "__main__":
    main()
