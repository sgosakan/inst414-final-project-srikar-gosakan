import os
import requests
from bs4 import BeautifulSoup
import json

# Create directories for storing data
os.makedirs('data/raw', exist_ok=True)

# Function to extract balance sheet data from EDGAR
def extract_edgar_data(ticker, year):
    """
    Extracts balance sheet data from a company's 10-K filing on the SEC EDGAR website.

    Parameters:
    ticker (str): The stock ticker symbol of the company.
    year (int): The year for which the 10-K filing data is required.

    Returns:
    dict: A dictionary containing the extracted balance sheet data.
    """
    base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K&dateb=&owner=exclude&count=10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    filing_details_url = None
    for link in soup.find_all('a'):
        if "Archives" in link.text:
            filing_details_url = "https://www.sec.gov" + link.get('href')
            break
    
    if not filing_details_url:
        raise Exception(f"Filing details URL not found for {ticker} {year}")

    response = requests.get(filing_details_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    document_url = None
    for link in soup.find_all('a'):
        if link.text.strip().lower().endswith(".htm"):
            document_url = "https://www.sec.gov" + link.get('href')
            break
    

    response = requests.get(document_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    
    balance_sheet_data = {}
    for table in tables:
        if 'Balance Sheets' in table.text:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip().replace(',', '').replace('$', '')
                    balance_sheet_data[key] = value
            break

    return balance_sheet_data