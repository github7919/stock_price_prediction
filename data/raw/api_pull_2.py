import yfinance as yf
import pandas as pd
import os
import warnings
import time

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def filter_by_date(dataframe, start_date, end_date):
    """Filter the DataFrame by a date range."""
    if not dataframe.empty:
        dataframe = dataframe.loc[:, (dataframe.columns >= start_date) & (dataframe.columns < end_date)]
    return dataframe

def get_financial_statements(ticker, start_date, end_date, retries=3, delay=5):
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            
            # Get key financial metrics
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            if financials.empty and balance_sheet.empty and cash_flow.empty:
                raise ValueError("Financial statements are empty")
            
            # Filter by date range
            financials = filter_by_date(financials, start_date, end_date)
            balance_sheet = filter_by_date(balance_sheet, start_date, end_date)
            cash_flow = filter_by_date(cash_flow, start_date, end_date)

            return financials, balance_sheet, cash_flow
        
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {ticker}: {e}")
            time.sleep(delay)
    raise Exception(f"Failed to fetch financial statements for {ticker} after {retries} retries.")

def save_financial_data(ticker, financials, balance_sheet, cash_flow):
    # Save financial metrics if they are not empty
    if not financials.empty:
        financials.to_parquet(f'financial_data/{ticker}_financials.parquet')
    if not balance_sheet.empty:
        balance_sheet.to_parquet(f'financial_data/{ticker}_balance_sheet.parquet')
    if not cash_flow.empty:
        cash_flow.to_parquet(f'financial_data/{ticker}_cash_flow.parquet')

# List of 100 tickers from various sectors
tickers = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "INTC", "CSCO", "ADBE",
    "ORCL", "CRM", "IBM", "QCOM", "TXN", "AVGO", "AMD", "MU", "AMAT", "ADI",
    
    # Healthcare
    "JNJ", "UNH", "PFE", "ABT", "MRK", "TMO", "ABBV", "DHR", "MDT", "BMY",
    
    # Financials
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "AXP", "SCHW", "USB",
    
    # Consumer Discretionary
    "HD", "NKE", "MCD", "SBUX", "LOW", "TGT", "BKNG", "TJX", "ROST", "MAR",
    
    # Consumer Staples
    "PG", "KO", "PEP", "WMT", "COST", "EL", "CL", "GIS", "K", "HSY",
    
    # Industrials
    "BA", "HON", "UNP", "UPS", "CAT", "GE", "MMM", "LMT", "RTX", "FDX",
    
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "KMI",
    
    # Materials
    "LIN", "SHW", "APD", "ECL", "NEM", "FCX", "DOW", "DD", "PPG", "NUE",
    
    # Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "WEC", "ES",
    
    # Real Estate
    "AMT", "PLD", "CCI", "EQIX", "PSA", "DLR", "AVB", "EQR", "O", "WELL"
]

# Define the date range for filtering
start_date = "2020-01-01"
end_date = "2024-01-01"

# Create a directory to save the data
os.makedirs('financial_data', exist_ok=True)

# Fetch and save financial statements for each ticker
for ticker in tickers:
    try:
        financials, balance_sheet, cash_flow = get_financial_statements(ticker, start_date, end_date)
        save_financial_data(ticker, financials, balance_sheet, cash_flow)
        print(f"Financial data for {ticker} saved successfully.")
    except Exception as e:
        print(f"Error fetching financial data for {ticker}: {e}")

print("Financial data collection complete.")
