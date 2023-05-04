#Develop script to create and update: 
#   -Moving avg
#   -RSI : A tool that helps determine whether a stock is overbought (meaning it might be due for a price drop) or oversold (meaning it might be due for a price increase).
#   -A/D Lines : A tool that helps determine whether there is more buying or selling pressure on a stock based on the relationship between price and trading volume.
#   -ADX : A tool that measures the strength of a stock’s trend, which can help identify whether the stock is trending up or down.
#   -Recommend 

#Imports 
import psycopg2
import requests
from bs4 import BeautifulSoup as bs
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    database="financial_db",
    user="postgres",
    password="KaMendiNiO"
)

# Open a cursor to perform database operations
cur = conn.cursor()

#Get the tickers as a list
cur.execute("SELECT Ticker FROM tickers")
tick = [row[0] for row in cur.fetchall()]

indicators_table = """
CREATE TABLE IF NOT EXISTS indicators (
    Ticker TEXT,
    RSI FLOAT,
    A_D FLOAT,
    ADX FLOAT,
    Last_200_MovAvg FLOAT,
    Recommendation TEXT
);
"""

# Create an empty DataFrame to store the results
results = pd.DataFrame(columns=['Ticker', 'Last_200_MovAvg', 'RSI', 'A_D', 'ADX', 'Recommendation'])
for t in tick: 
    #Produce moving avg
    df = pd.read_sql_query("SELECT * FROM all_time_prices WHERE \"Ticker\" = '"+t+"'", conn)
    print(df)

    # Calculate the 200-day moving average
    try: 
        df['MA'] = df['Close'].rolling(window=200).mean()
    except IndexError: 
        df['MA'] = df['Close'].rolling(window=len(df['Close'])).mean()
    #Compute RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    try: 
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
    except IndexError:
        avg_gain = gain.rolling(window=len(gain)).mean()
        avg_loss = loss.rolling(window=len(loss)).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    print(rsi.iloc[-1])

    #Compute A/D lines
    df['UpMove'] = df['High'] - df['High'].shift(1)
    df['DownMove'] = df['Low'].shift(1) - df['Low']
    df['UpVolume'] = df['UpMove'] * df['Volume']
    df['DownVolume'] = df['DownMove'] * df['Volume']
    df['PosDM'] = df['UpMove']
    df['NegDM'] = df['DownMove']
    df.loc[df.UpMove < df.DownMove, 'PosDM'] = 0
    df.loc[df.UpMove > df.DownMove, 'NegDM'] = 0
    df['PosDI'] = df['PosDM'].rolling(window=14).mean()
    df['NegDI'] = df['NegDM'].rolling(window=14).mean()
    df['AD'] = (df['PosDI'] - df['NegDI']) / (df['PosDI'] + df['NegDI'])
    print(df)

    # Calculate ADX
    df['ADX'] = 100 * (df['PosDI'] - df['NegDI']) / (df['PosDI'] + df['NegDI'])
    df['ADX'] = df['ADX'].rolling(window=14).mean()

    # Determine the recommendation
    if df['Close'].iloc[-1] > df['MA'].iloc[-1] and rsi.iloc[-1] > 70 and df['AD'].iloc[-1] > df['AD'].iloc[
        -2] and df['ADX'].iloc[-1] > 25:
        recommendation = 'Buy'
    elif df['Close'].iloc[-1] < df['MA'].iloc[-1] and rsi.iloc[-1] < 30 and df['AD'].iloc[-1] < df['AD'].iloc[
        -2] and df['ADX'].iloc[-1] > 25:
        recommendation = 'Sell'
    else:
        recommendation = 'Hold'

    # Append the results to the DataFrame
    results = results.append(
        {'Ticker': t, 'Last_200_MovAvg': df['MA'].iloc[-1], 'RSI': rsi.iloc[-1], 'A_D': df['AD'].iloc[-1],
         'ADX': df['ADX'].iloc[-1], 'Recommendation': recommendation}, ignore_index=True)
    
    print(results)



