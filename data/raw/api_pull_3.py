import yfinance as yf
import pandas as pd
import os
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def get_historical_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        
        # Get historical market data
        hist = stock.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"No data found for {ticker} in the specified date range.")
            return None
        
        # Calculate selected technical indicators
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
        
        # MACD
        hist['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
        hist['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
        hist['MACD'] = hist['EMA_12'] - hist['EMA_26']
        hist['Signal_Line'] = hist['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # Remove NaN values
        hist.dropna(inplace=True)
        
        return hist
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def save_data(ticker, hist, directory):
    # Save historical data with technical indicators
    if hist is not None:
        hist.to_parquet(os.path.join(directory, f'{ticker}_historical_with_indicators.parquet'))

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

# Set the date range for historical data
start_date = "2020-01-01"
end_date = "2024-01-01"

# Define the directory to save the data
directory = r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\historical_indicators"
os.makedirs(directory, exist_ok=True)

# Fetch and save data for each ticker
for ticker in tickers:
    hist = get_historical_data(ticker, start_date, end_date)
    save_data(ticker, hist, directory)
    print(f"Data for {ticker} processed.")

print("Data collection complete.")
