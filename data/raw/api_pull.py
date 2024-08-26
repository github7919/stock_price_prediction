import yfinance as yf
import pandas as pd
import numpy as np
import os
from ta import add_all_ta_features
from ta.utils import dropna
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
#warnings.filterwarnings("ignore", category=PerformanceWarning)

def get_financial_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    
    # Get historical market data
    hist = stock.history(start=start_date, end=end_date)
    
    # Get key financial metrics
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    # Add all technical indicators
    hist = add_all_ta_features(
        hist, open="Open", high="High", low="Low", close="Close", volume="Volume"
    )
    
    # Calculate additional indicators
    indicators = pd.DataFrame(index=hist.index)
    indicators['SMA_50'] = hist['Close'].rolling(window=50).mean()
    indicators['SMA_200'] = hist['Close'].rolling(window=200).mean()
    indicators['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    
    # MACD
    indicators['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
    indicators['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
    indicators['MACD'] = indicators['EMA_12'] - indicators['EMA_26']
    indicators['Signal_Line'] = indicators['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    indicators['BB_Middle'] = hist['Close'].rolling(window=20).mean()
    indicators['BB_Upper'] = indicators['BB_Middle'] + 2 * hist['Close'].rolling(window=20).std()
    indicators['BB_Lower'] = indicators['BB_Middle'] - 2 * hist['Close'].rolling(window=20).std()
    
    # Stochastic Oscillator
    indicators['Lowest_14'] = hist['Low'].rolling(window=14).min()
    indicators['Highest_14'] = hist['High'].rolling(window=14).max()
    indicators['%K'] = (hist['Close'] - indicators['Lowest_14']) / (indicators['Highest_14'] - indicators['Lowest_14']) * 100
    indicators['%D'] = indicators['%K'].rolling(window=3).mean()
    
    # On-Balance Volume (OBV)
    indicators['OBV'] = (np.sign(hist['Close'].diff()) * hist['Volume']).fillna(0).cumsum()
    
    # Average True Range (ATR)
    tr = np.maximum(
        hist['High'] - hist['Low'],
        np.maximum(
            abs(hist['High'] - hist['Close'].shift()),
            abs(hist['Low'] - hist['Close'].shift())
        )
    )
    indicators['ATR'] = tr.rolling(window=14).mean()
    
    # Commodity Channel Index (CCI)
    tp = (hist['High'] + hist['Low'] + hist['Close']) / 3
    sma_tp = tp.rolling(window=20).mean()
    mad = lambda x: np.abs(x - x.mean()).mean()
    indicators['CCI'] = (tp - sma_tp) / (0.015 * tp.rolling(window=20).apply(mad))
    
    # Combine all data
    hist = pd.concat([hist, indicators], axis=1)
    
    # Remove NaN values
    hist = dropna(hist)
    
    return hist, financials, balance_sheet, cash_flow

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

start_date = "2010-01-01"
end_date = "2024-08-01"

# Create a directory to save the data
os.makedirs('financial_data', exist_ok=True)

# Fetch and save data for each ticker
for ticker in tickers:
    try:
        hist, financials, balance_sheet, cash_flow = get_financial_data(ticker, start_date, end_date)
        
        # Save historical data with technical indicators
        hist.to_parquet(f'financial_data/{ticker}_historical_with_indicators.parquet')
        
        # Save financial metrics
        financials.to_parquet(f'financial_data/{ticker}_financials.parquet')
        balance_sheet.to_parquet(f'financial_data/{ticker}_balance_sheet.parquet')
        cash_flow.to_parquet(f'financial_data/{ticker}_cash_flow.parquet')
        
        print(f"Data for {ticker} saved successfully.")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

print("Data collection complete.")
