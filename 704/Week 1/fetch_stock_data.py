import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the tickers: AAPL, SPY, TSLA (required) + QQQ (starts with Q), MSFT, NVDA
tickers = ['AAPL', 'SPY', 'TSLA', 'QQQ', 'MSFT', 'NVDA']

# Date range: September 2024 to August 2026 (24 months)
# The last month that ended before September 2026 is August 2026
start_date = '2024-09-01'
end_date = '2026-08-31'

# Download data for all tickers
print("Downloading historical data...")
data = yf.download(tickers, start=start_date, end=end_date, progress=False)

# Get the adjusted close prices (returned as 'Close' in recent yfinance versions)
# The data has MultiIndex columns with ('Close', 'AAPL'), etc.
adj_close = data['Close']

# Get the last trading day of each month
print("Processing data to get last trading day of each month...")
last_trading_days = adj_close.resample('M').last()

# Reset index to make date a column
df = last_trading_days.reset_index()

# Rename the 'Date' column to 'date'
df = df.rename(columns={'Date': 'date'})

# Format the date column as YYYY-MM-DD
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

print(f"\nData shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nLast few rows:")
print(df.tail())

# Check for any missing values
print(f"\nMissing values per column:")
print(df.isnull().sum())

# Save to TSV file
output_file = 'historical_prices.tsv'
df.to_csv(output_file, sep='\t', index=False)
print(f"\nData saved to {output_file}")
