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
   DataFrame: Enhanced financial data with additional features.
   """
   logging.info('Performing feature engineering on the data.')

   df.index = pd.to_datetime(df.index)
   df = df.asfreq('QE')
   df.ffill(inplace=True)
   return df


def split_data(df, train_size=0.8, ticker='', data_type=''):
    """
    Split data into training and validation sets and save as CSV files.

    Parameters:
    df (DataFrame): Financial data.
    train_size (float): Proportion of data to use for training.
    ticker (str): Stock ticker symbol.
    data_type (str): Type of data (e.g., 'quarterly_income_statement').

    Returns:
    DataFrame, DataFrame: Training and validation data.
    """
    cutoff = int(len(df) * train_size)
    training_data = df.iloc[:cutoff]
    validation_data = df.iloc[cutoff:]

    output_dir = './data/outputs/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    training_file = os.path.join(output_dir, f'{ticker}_{data_type}_training_data.csv')
    validation_file = os.path.join(output_dir, f'{ticker}_{data_type}_validation_data.csv')
    
    training_data.to_csv(training_file)
    validation_data.to_csv(validation_file)
    
    logging.info(f"Saved training data to {training_file}")
    logging.info(f"Saved validation data to {validation_file}")
    return training_data, validation_data

def train_model(training_data, column_name):
   """
   Train Holt's Linear Trend model using training data.

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
   Evaluate the forecast against the validation data.


   Parameters:
   model: Fitted Holt model.
   validation_data (DataFrame): Validation data.
   column_name (str): The column forecasted.


   Returns:
   dict: Dictionary containing evaluation metrics.
   """
   forecast = model.forecast(steps=len(validation_data))
   actual = validation_data[column_name]
   mae = mean_absolute_error(actual, forecast)
   rmse = mean_squared_error(actual, forecast, squared=False)


   return {'MAE': mae, 'RMSE': rmse}


def save_metrics(ticker, column_name, metrics):
   """
   Save evaluation metrics to a CSV file.

   Parameters:
   ticker (str): Stock ticker symbol.
   column_name (str): The column evaluated.
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
      
def main():
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    data_type = 'quarterly_income_statement' 
    column_name = 'total_revenue' 

    try:
        df = load_data(f'./data/loaded/{ticker}_{data_type}.csv')
        df = feature_engineering(df)

        training_data, validation_data = split_data(df, train_size=0.8, ticker=ticker, data_type=data_type)

        logging.info(f"Training data:\n{training_data}\n")
        logging.info(f"Validation data:\n{validation_data}\n")

        # Train the model
        model = train_model(training_data, column_name)

        # Evaluate the forecast
        metrics = evaluate_forecast(model, validation_data, column_name)
        
        # Save the evaluation metrics
        save_metrics(ticker, column_name, metrics)
        print(f"Evaluation Metrics:\n{metrics}\n")

        logging.info(f'Forecast evaluation complete for {ticker}.')
    except Exception as e:
        logging.error(f'Error in evaluating forecast for {ticker}: {e}')


if __name__ == "__main__":
   main()



