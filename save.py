import pandas as pd
import yfinance as yf

# Define the ticker symbol
ticker = "AAPL"

# Get the stock price data
stock_data = yf.download(ticker, start="2015-01-01")

# Calculate the daily returns
daily_returns = stock_data["Close"].pct_change()

# Calculate the daily volatility
daily_volatility = daily_returns.std()
print(stock_data['Close'])
print("The daily volatility of", ticker, "is:", daily_volatility)