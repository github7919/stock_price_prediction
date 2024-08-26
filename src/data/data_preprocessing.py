import pandas as pd
import os

def load_and_combine_data(data_dir = r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\data\raw\financial_data"):
    # Lists to store DataFrames
    historical_dfs = []
    balance_sheet_dfs = []
    income_statement_dfs = []
    cash_flow_dfs = []

    # Iterate through all files in the directory
    for filename in os.listdir(data_dir):
        if filename.endswith('_historical_with_indicators.parquet'):
            ticker = filename.split('_')[0]
            df = pd.read_parquet(os.path.join(data_dir, filename))
            df['Ticker'] = ticker
            historical_dfs.append(df)
        elif filename.endswith('_balance_sheet.parquet'):
            ticker = filename.split('_')[0]
            df = pd.read_parquet(os.path.join(data_dir, filename))
            df['Ticker'] = ticker
            balance_sheet_dfs.append(df)
        elif filename.endswith('_financials.parquet'):
            ticker = filename.split('_')[0]
            df = pd.read_parquet(os.path.join(data_dir, filename))
            df['Ticker'] = ticker
            income_statement_dfs.append(df)
        elif filename.endswith('_cash_flow.parquet'):
            ticker = filename.split('_')[0]
            df = pd.read_parquet(os.path.join(data_dir, filename))
            df['Ticker'] = ticker
            cash_flow_dfs.append(df)

    # Combine DataFrames
    combined_historical = pd.concat(historical_dfs, ignore_index=True)
    combined_balance_sheet = pd.concat(balance_sheet_dfs, ignore_index=True)
    combined_income_statement = pd.concat(income_statement_dfs, ignore_index=True)
    combined_cash_flow = pd.concat(cash_flow_dfs, ignore_index=True)

    # Set multi-index for financial statements
    for df in [combined_balance_sheet, combined_income_statement, combined_cash_flow]:
        df.set_index(['Ticker', df.columns[0]], inplace=True)
        df.index.names = ['Ticker', 'Date']

    return combined_historical, combined_balance_sheet, combined_income_statement, combined_cash_flow

# Load and combine the data
historical, balance_sheet, income_statement, cash_flow = load_and_combine_data()

# Save combined data
historical.to_parquet(r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\data\raw\financial_data\combined_historical_data.parquet")
balance_sheet.to_parquet(r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\data\raw\financial_data\combined_balance_sheet.parquet")
income_statement.to_parquet(r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\data\raw\financial_data\combined_income_statement.parquet")
cash_flow.to_parquet(r"C:\D\Coding\C++\Project Alpha\stock_price_prediction\data\raw\financial_data\combined_cash_flow.parquet")

# Display info about combined datasets
print("Combined Historical Data:")
print(historical.info())
print("\nCombined Balance Sheet:")
print(balance_sheet.info())
print("\nCombined Income Statement:")
print(income_statement.info())
print("\nCombined Cash Flow:")
print(cash_flow.info())
