import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    """
    Load data from CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    DataFrame: Loaded data.
    """
    return pd.read_csv(file_path, index_col=0)

def plot_time_series(df, forecast, metric):
    """
    Plot actual vs. forecasted time series data.

    Parameters:
    df (DataFrame): Original financial data.
    forecast (Series): Forecasted data.
    metric (str): Financial metric to plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df[metric], label='Actual')
    plt.plot(forecast.index, forecast, label='Forecast', linestyle='--')
    plt.title(f'Actual vs. Forecasted {metric}')
    plt.xlabel('Date')
    plt.ylabel(metric.capitalize())
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_anomalies(df, metric):
    """
    Plot anomalies in the financial data using Seaborn.

    Parameters:
    df (DataFrame): Financial data with anomaly scores.
    metric (str): Financial metric to plot.
    """
    anomalies = df[df['anomaly_score'] == -1]
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=df.index, y=metric, label='Normal')
    sns.scatterplot(data=anomalies, x=anomalies.index, y=metric, color='red', label='Anomaly')
    plt.title(f'Anomalies in {metric}')
    plt.xlabel('Date')
    plt.ylabel(metric.capitalize())
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_feature_relationships(df):
    """
    Plot key financial ratios over time using Seaborn.

    Parameters:
    df (DataFrame): Financial data.
    """
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=df.index, y='revenue_growth', label='Revenue Growth')
    sns.lineplot(data=df, x=df.index, y='expense_ratio', label='Expense Ratio')
    plt.title('Key Financial Ratios Over Time')
    plt.xlabel('Date')
    plt.ylabel('Ratio')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_comparison_chart(df):
    """
    Compare the performance of different financial metrics over time using Matplotlib.

    Parameters:
    df (DataFrame): Financial data.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['total_revenue'], label='Total Revenue')
    plt.plot(df.index, df['total_expenses'], label='Total Expenses')
    plt.plot(df.index, df['net_income'], label='Net Income')
    plt.title('Revenue, Expenses, and Net Income Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Main function to create visualizations.
    """
    ticker = 'AAPL'
    data_type = 'quarterly_income_statement'
    
    # Load processed data
    df = load_data(f'data/processed/{ticker}_{data_type}.csv')

    forecast = pd.read_csv(f'data/processed/{ticker}_{data_type}_forecast.csv', index_col=0)

    plot_time_series(df, forecast['total_revenue'], 'total_revenue')
    df_with_anomalies = load_data(f'data/processed/{ticker}_{data_type}_anomalies.csv')
    plot_anomalies(df_with_anomalies, 'total_revenue')
    plot_feature_relationships(df)
    plot_comparison_chart(df)
    
if __name__ == "__main__":
    main()
