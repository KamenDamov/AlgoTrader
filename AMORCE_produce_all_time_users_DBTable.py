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
import sqlalchemy
from sqlalchemy import create_engine


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
    Volatility_30_Day FLOAT, 
    Ticker TEXT NOT NULL    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(all_time_prices_query)
cur.execute("SELECT Ticker FROM tickers")
tick = [row[0] for row in cur.fetchall()]
all_time_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'Volatility_30_Day','Ticker']
all_time = pd.DataFrame(columns = all_time_cols)
count = 0 
for i in range(len(tick)): 
    start = time.time()    
    try:
        #Creating the df to be added to all_time_prices
        ticker = tick[i]
        info = yf.Ticker(ticker).history(period='max')
        info.reset_index(inplace = True)
        info['Ticker'] = ticker

        # Calculate the daily returns
        try: 
            info['Returns'] = np.log(info['Close'] / info['Close'].shift(1))
            info['Volatility'] = info['Returns'].rolling(window=30).std() * np.sqrt(252)
        except: 
            info['Returns'] = np.log(info['Close'] / info['Close'].shift(1))
            info['Volatility'] = info['Returns'].rolling(window=len(info['Returns'])).std() * np.sqrt(252)
        info.rename({'Stock Splits':'Stock_Splits'},axis = 1,inplace = True)
        info['Volume'] = info['Volume'].astype(float)
        if 'Capital Gains' in info.columns: 
            del info['Capital Gains']
        print(info)
        break
        # Append the first dataframe to the table
        #all_time = pd.concat([all_time, info])

        #print(momentum_append)
    except TypeError: 
        print("Nonetype found for: " + tick[i])
        continue
    except IndexError: 
        print("Couldn't find: ",tick[i])
        continue
    except KeyError:
        print("Couldnt find key for: " + tick[i])
        continue
    except AttributeError: 
        print("Attribute error found")
        continue

    #Push data to all_time_prices table
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    info.to_sql(name='all_time_prices', con=engine, if_exists='append', index=False)
    
    print('Done')

    # Commit the transaction
    conn.commit()
    
# Close the cursor and connection
cur.close()
conn.close()
