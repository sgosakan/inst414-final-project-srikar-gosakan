import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def load_data(file_path):
    """
    Load data from CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    DataFrame: Loaded data.
    """
    return pd.read_csv(file_path, index_col=0)

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
    Main function to evaluate the anomaly detection model.
    """
    ticker = 'AAPL'
    data_type = 'quarterly_income_statement'
    
    # Load processed data with anomalies
    df_with_anomalies = load_data(f'data/processed/{ticker}_{data_type}_anomalies.csv')
    
    # Evaluate anomalies
    metrics = evaluate_anomalies(df_with_anomalies)
    print(f"Anomaly Detection Evaluation Metrics: {metrics}")

if __name__ == "__main__":
    main()
