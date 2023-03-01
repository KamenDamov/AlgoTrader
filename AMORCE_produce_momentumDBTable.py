import psycopg2
import numpy as np
import pandas as pd
import math
import requests 
import matplotlib as plt
import seaborn as sns
import yfinance as yf
import pandas_datareader as web
from pandas_datareader import data
from bs4 import BeautifulSoup as bs
from scipy import stats
import psycopg2
import time

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    database="financial_db",
    user="postgres",
    password="KaMendiNiO"
)

# Open a cursor to perform database operations
cur = conn.cursor()

momentum_query = '''
CREATE TABLE IF NOT EXISTS momentum (
    Ticker TEXT NOT NULL,
    Price FLOAT,
    y1_Price_Return FLOAT, 
    y1_percentile FLOAT, 
    m6_Price_Return FLOAT, 
    m6_percentile FLOAT,
    m3_Price_Return FLOAT, 
    m3_percentile FLOAT, 
    m1_Price_Return FLOAT, 
    m1_percentile FLOAT, 
    Weighted_Hurst_Exponent FLOAT,
    HQM_score FLOAT
);
'''

#calulate the Hurst exponent of a stock
def get_hurst_exponent(time_series, max_lag):
    """Returns the Hurst Exponent of the time series"""
        
    lags = range(2, max_lag)

    # variances of the lagged differences
    tau = [np.std(np.subtract(time_series[lag:], time_series[:-lag])) for lag in lags]

    # calculate the slope of the log plot -> the Hurst Exponent
    reg = np.polyfit(np.log(lags), np.log(tau), 1)

    return reg[0]

# Execute a CREATE TABLE statement to create a new table
cur.execute(momentum_query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()