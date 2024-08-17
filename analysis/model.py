import pandas as pd
from statsmodels.tsa.holtwinters import Holt
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging
import os

# Configure logging
logging.basicConfig(filename='./pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

def feature_engineering(df):
    """
    Feature engineer the financial data.

    Parameters:
    df (DataFrame): Financial data.

    Returns:
    DataFrame: Enhanced financial data.
    """
    logging.info('Performing feature engineering on the data.')

    df.index = pd.to_datetime(df.index)
    df = df.asfreq('QE')

    df.ffill(inplace=True)

    return df

def split_data(df, train_size=0.8):
    """
    Split data into training and validation sets.

    Parameters:
    df (DataFrame): Financial data.
    train_size (float): Proportion of data to use for training.

    Returns:
    DataFrame, DataFrame: Training and validation data.
    """
    cutoff = int(len(df) * train_size)
    training_data = df.iloc[:cutoff]
    validation_data = df.iloc[cutoff:]
    return training_data, validation_data

def train_model(training_data, column_name):
    """
    Train Holt's Linear Trend model using  training data.

    Parameters:
    training_data (DataFrame): Training data.
    column_name (str): The column forecasted.

    Returns:
    model: Fitted Holt model.
    """
    series = training_data[column_name]
    model = Holt(series).fit()
    return model

def evaluate_forecast(model, validation_data, column_name):
    """
    Evaluate forecast against validation data.

    Parameters:
    model: Fitted Holt model.
    validation_data (DataFrame): Validation data.
    column_name (str): The column forecasted.

    Returns:
    dict: Dictionary containing evaluation metrics.
    """
    # Forecast for the validation period
    forecast = model.forecast(steps=len(validation_data))

    # Actual values
    actual = validation_data[column_name]

    mae = mean_absolute_error(actual, forecast)
    rmse = mean_squared_error(actual, forecast, squared=False)

    return {'MAE': mae, 'RMSE': rmse}

def save_metrics(ticker, column_name, metrics):
    """
    Save evaluation metrics to a CSV file.

    Parameters:
    ticker (str): Stock ticker symbol.
    column_name (str): The column being evaluated.
    metrics (dict): Evaluation metrics.
    """
    output_dir = './data/outputs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f'{ticker}_evaluation_metrics.csv')
    metrics_df = pd.DataFrame([metrics], index=[column_name])
    
    if os.path.exists(output_file):
        metrics_df.to_csv(output_file, mode='a', header=False)
    else:
        metrics_df.to_csv(output_file)

def forecast_variable(df, column_name):
    """
    Forecast future values using Holt's Linear Trend model.
    
    Parameters:
    df (DataFrame): Financial data.
    column_name (str): The column to forecast.
    
    Returns:
    DataFrame: Forecasted values.
    """
    try:
        series = df[column_name]
        
        logging.info(f"{column_name.capitalize()} Series Type: {type(series)}")
        logging.info(f"{column_name.capitalize()} Series Content: {series.tolist()}")
        
        if isinstance(series, pd.Series) and len(series) > 1:
            model = Holt(series)
            model_fit = model.fit()

            forecast = model_fit.forecast(steps=4)
            
            forecast_dates = pd.date_range(start=series.index[-1], periods=5, freq='QE')[1:]
            forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=[column_name])
            
            return forecast_df
        else:
            logging.error(f"{column_name.capitalize()} data is not in the expected format or contains insufficient data points.")
            return None
    except Exception as e:
        logging.error(f"Error fitting Holt's model for {column_name}: {e}")
        return None

        
def main():
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    data_type = 'quarterly_income_statement'  
    column_name = 'total_revenue' 

    try:
        df = load_data(f'./data/loaded/{ticker}_{data_type}.csv')
        df = feature_engineering(df)

        training_data, validation_data = split_data(df, train_size=0.8)

        logging.info(f"Training data:\n{training_data}\n")
        logging.info(f"Validation data:\n{validation_data}\n")

        model = train_model(training_data, column_name)

        metrics = evaluate_forecast(model, validation_data, column_name)
        
        save_metrics(ticker, column_name, metrics)
        print(f"Evaluation Metrics:\n{metrics}\n")
        
        income_data_type = 'quarterly_income_statement'
        df_income = load_data(f'./data/loaded/{ticker}_{income_data_type}.csv')
        df_income = feature_engineering(df_income)
        
        # Forecast the total revenue using Holt's method
        revenue_forecast = forecast_variable(df_income, 'total_revenue')
        if revenue_forecast is not None:
            revenue_forecast_output_path = f'./data/outputs/{ticker}_{income_data_type}_revenue_forecast.csv'
            revenue_forecast.to_csv(revenue_forecast_output_path, index=True)
            logging.info(f'Saved forecasted revenue to {revenue_forecast_output_path}')
            print(f"Forecasted revenue:\n{revenue_forecast}")
        
        # Load and process the data for total debt
        balance_data_type = 'quarterly_balance_sheet'
        df_balance = load_data(f'./data/loaded/{ticker}_{balance_data_type}.csv')
        df_balance = feature_engineering(df_balance)
        
        # Forecast the total debt using Holt's method
        debt_forecast = forecast_variable(df_balance, 'total_debt')
        if debt_forecast is not None:
            debt_forecast_output_path = f'./data/outputs/{ticker}_{balance_data_type}_debt_forecast.csv'
            debt_forecast.to_csv(debt_forecast_output_path, index=True)
            logging.info(f'Saved forecasted debt to {debt_forecast_output_path}')
            print(f"Forecasted total_debt:\n{debt_forecast}")


        logging.info(f'Forecast evaluation complete for {ticker}.')
    except Exception as e:
        logging.error(f'Error in evaluating forecast for {ticker}: {e}')

if __name__ == "__main__":
    main()
