import subprocess
import logging

# Configure logging
logging.basicConfig(filename='pipeline.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    """
    Run a Python script.

    Parameters:
    script_name (str): The name of the Python script to run.
    """
    logging.info(f'Starting script: {script_name}')
    subprocess.run(['python', script_name], check=True)
    logging.info(f'Completed script: {script_name}')

def main():
    """
    Main function to run the entire ETL, analysis, and visualization pipeline.
    """
    logging.info('Starting ETL process...')
    try:
        run_script('extract.py')
        run_script('transform.py')
        run_script('load.py')
        logging.info('ETL process complete.')
    except subprocess.CalledProcessError as e:
        logging.error(f'ETL process failed: {e}')
        return
    
    logging.info('Starting analysis process...')
    try:
        run_script('model.py')
        logging.info('Analysis process complete.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Analysis process failed: {e}')
        return

    logging.info('Starting visualization process...')
    try:
        run_script('visualize.py')
        logging.info('Visualization process complete.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Visualization process failed: {e}')
        return

if __name__ == "__main__":
    main()

