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

#Create first table with all stock info from yfinance
tick = pd.read_csv("all_stocks")
all_time_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'Ticker']
all_time = pd.DataFrame(columns = all_time_cols)
count = 0 
for i in range(len(tick)):    
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

    count += 1 
    if count == 10: 
        break

all_time.to_csv('Pour Samir')

