import subprocess
import logging
import os

# Configure logging
logging.basicConfig(filename='pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_path, ticker):
    """
    Run a Python script with the provided ticker symbol.

    Parameters:
    script_path (str): The relative path to the Python script to run.
    ticker (str): Stock ticker symbol to pass to the script.
    """
    try:
        subprocess.run(['python', script_path, ticker], check=True)
        logging.info(f'Successfully ran {os.path.basename(script_path)} for ticker {ticker}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error running {os.path.basename(script_path)} for ticker {ticker}: {e}')

def main():
    """
    Main function to run the entire ETL, analysis, and visualization pipeline.
    """
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    
    scripts = [
        'etl/extract.py',
        'etl/transform.py',
        'etl/load.py',
        'analysis/model.py',
        'analysis/evaluate.py',
        'vis/visualizations.py'
    ]
    
    for script in scripts:
        run_script(script, ticker)

if __name__ == "__main__":
    main()
