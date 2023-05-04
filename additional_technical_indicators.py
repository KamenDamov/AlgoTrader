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
    Last_200_MovAvg FLOAT
);
"""





