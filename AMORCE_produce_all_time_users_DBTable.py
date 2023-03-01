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

all_time_prices_query = '''
CREATE TABLE IF NOT EXISTS all_time_prices (
    Date TIMESTAMP,
    Open FLOAT,
    High FLOAT, 
    Low FLOAT, 
    Close FLOAT, 
    Volume FLOAT,
    Dividends FLOAT, 
    Stock_Splits FLOAT, 
    Ticker TEXT NOT NULL    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(all_time_prices_query)

all_time_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'Ticker']
all_time = pd.DataFrame(columns = all_time_cols)
count = 0 
for i in range(len(tick)): 
    start = time.time()    
    try:
        #Creating the df to be added to all_time_prices
        ticker = tick["0"][i]
        info = yf.Ticker(ticker).history(period='max')
        info.reset_index(inplace = True)
        info['Ticker'] = ticker
        info.rename({'Stock Splits':'Stock_Splits'},axis = 1,inplace = True)
        info['Volume'] = info['Volume'].astype(float)
        print(info) 
        
        # Append the first dataframe to the table
        all_time = pd.concat([all_time, info])

        #print(momentum_append)
    except TypeError: 
        print("Nonetype found for: " + tick["0"][i])
        continue
    except IndexError: 
        print("Couldn't find: ",tick["0"][i])
        continue
    except KeyError:
        print("Couldnt find key for: " + tick['0'][i])
        continue
    except AttributeError: 
        print("Attribute error found")
        continue


# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
