import pandas as pd
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, precision_score, recall_score, f1_score

def load_data(file_path):
    """
    Load data from CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    DataFrame: Loaded data.
    """
    return pd.read_csv(file_path, index_col=0)

def feature_engineering(df):
    """
    Perform feature engineering on the financial data.

    Parameters:
    df (DataFrame): Financial data.

    Returns:
    DataFrame: Enhanced financial data with additional features.
    """
    df['revenue_growth'] = df['total_revenue'].pct_change()
    df['expense_ratio'] = df['total_expenses'] / df['total_revenue']
    df['revenue_rolling_mean'] = df['total_revenue'].rolling(window=4).mean()
    df['expense_rolling_mean'] = df['total_expenses'].rolling(window=4).mean()
    df.dropna(inplace=True)  # Drop rows with NaN values resulting from rolling calculations
    return df

def forecast_revenue(df):
    """
    Forecast future revenue using ARIMA model.

    Parameters:
    df (DataFrame): Financial data.

    Returns:
    DataFrame: Forecasted revenue.
    """
    model = ARIMA(df['total_revenue'], order=(5, 1, 0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=4)  # Forecasting next 4 periods
    return forecast

def detect_anomalies(df):
    """
    Detect anomalies in the financial data using Isolation Forest.

    Parameters:
    df (DataFrame): Financial data.

    Returns:
    DataFrame: Data with anomaly scores.
    """
    model = IsolationForest(contamination=0.05)
    df['anomaly_score'] = model.fit_predict(df[['total_revenue', 'total_expenses']])
    return df

def evaluate_forecast(df, forecast):
    """
    Evaluate the forecasted revenue.

    Parameters:
    df (DataFrame): Original financial data.
    forecast (DataFrame): Forecasted revenue.

    Returns:
    dict: Dictionary containing evaluation metrics.
    """
    actual = df['total_revenue'][-len(forecast):]
    mae = mean_absolute_error(actual, forecast)
    rmse = mean_squared_error(actual, forecast, squared=False)
    return {'MAE': mae, 'RMSE': rmse}

def evaluate_anomalies(df):
    """
    Evaluate the anomaly detection model.

    Parameters:
    df (DataFrame): Financial data with anomaly scores.

    Returns:
    dict: Dictionary containing evaluation metrics.
    """
    precision = precision_score(df['true_anomalies'], df['anomaly_score'])
    recall = recall_score(df['true_anomalies'], df['anomaly_score'])
    f1 = f1_score(df['true_anomalies'], df['anomaly_score'])
    return {'Precision': precision, 'Recall': recall, 'F1-Score': f1}

def main():
    """
    Main function to run predictive models and anomaly detection.
    """
    ticker = 'AAPL'
    data_type = 'quarterly_income_statement'
    
    # Load transformed data
    df = load_data(f'data/processed/{ticker}_{data_type}.csv')
    
    # Perform feature engineering
    df = feature_engineering(df)
    
    # Forecast future revenue using ARIMA
    revenue_forecast = forecast_revenue(df)
    print("ARIMA Revenue Forecast:")
    print(revenue_forecast)
    
    # Evaluate forecasts
    forecast_metrics = evaluate_forecast(df, revenue_forecast)
    print("ARIMA Forecast Evaluation Metrics:")
    print(forecast_metrics)
    
    # Detect anomalies
    df_with_anomalies = detect_anomalies(df)
    df_with_anomalies.to_csv(f'data/processed/{ticker}_{data_type}_anomalies.csv', index=True)
    print("Anomaly detection complete. Data saved to data/processed/ directory.")

if __name__ == "__main__":
    main()
