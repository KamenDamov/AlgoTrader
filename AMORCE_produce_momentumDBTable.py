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

cur.execute("SELECT Ticker FROM tickers")
tick = [row[0] for row in cur.fetchall()]
momentum_cols = ['Ticker','Price',
                'y1_Price_Return','y1_percentile', 
                'm6_Price_Return', 'm6_percentile', 
                'm3_Price_Return', 'm3_percentile',
                'm1_Price_Return','m1_percentile',
                'Weighted_Hurst_Exponent']
momentum = pd.DataFrame(columns = momentum_cols)

count = 0 
for i in range(len(tick)): 
    start = time.time()    
    try:
        #Creating the df to be added to all_time_prices
        ticker = tick[i]
        info = yf.Ticker(ticker).history(period='max')
        info.reset_index(inplace = True)
        info['Ticker'] = ticker

        info.sort_values("Date", ascending = True, inplace = True)
        info.set_index("Date", inplace = True)
        #Creating the df to be added to momentum
        y = info.truncate(before=pd.Timestamp('today') - pd.DateOffset(months=12))
        m6 = info.truncate(before=pd.Timestamp('today') - pd.DateOffset(months=6))
        m3 = info.truncate(before=pd.Timestamp('today') - pd.DateOffset(months=3))
        m1 = info.truncate(before=pd.Timestamp('today') - pd.DateOffset(months=1))

        #momentum['Ticker'] = tick['0'][i]  
        try: 
            perc_change1y = ((y.iloc[-1]['Close'] - y.iloc[0]['Close'])/y.iloc[0]["Close"])
            #momentum['1y Price Return'] = perc_change1y
            perc_change6m = ((m6.iloc[-1]['Close'] - m6.iloc[0]['Close'])/m6.iloc[0]["Close"])
            #momentum['6m Price Return'] = perc_change6m
            perc_change3m = ((m3.iloc[-1]['Close'] - m3.iloc[0]['Close'])/m3.iloc[0]["Close"])
            #momentum['3m Price Return'] = perc_change3m
            perc_change1m = ((m1.iloc[-1]['Close'] - m1.iloc[0]['Close'])/m1.iloc[0]["Close"])
            #momentum['1m Price Return'] = perc_change1m

            #momentum['Price'] = info['Close'] 
            #momentum['1y percentile'] = 0
            #momentum['6m percentile'] = 0
            #momentum['3m percentile'] = 0
            #momentum['1m percentile'] = 0
            #momentum['Weighted Hurst Exponent'] = 0
            t = [20, 100, 300, 500, 1000]
            total_hurst = 0
            weight = 0.4
            for j in range(len(t)): 
                #Use Weighted average to determine hurst exp of the stock
                hurst_exp = get_hurst_exponent(info["Close"].values, t[j])
                #print(tick["0"][i] + " Hurst exponent with " + str(t[j]) +  ' lags: ' + str(hurst_exp))
                total_hurst += hurst_exp*weight
                if j >= 2: 
                    weight = 0.1
                else: 
                    weight = 0.2
            #momentum = momentum.iloc[-1]
        except IndexError: 
            print('Index Error when producing momentum table')
            continue
        momentum_append = pd.Series([tick[i],info['Close'][-1],perc_change1y,0,perc_change6m,0,perc_change3m,0,perc_change1m,0, total_hurst],
                                index = momentum_cols)
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
    stop = time.time()
    duration = stop-start
    print(duration)
    momentum.loc[len(momentum)] = momentum_append

#Get percentiles for each stock
cols = ['y1', 'm6', 'm3', 'm1']
for c in cols: 
    for index, row in momentum.iterrows(): 
        percentile_change = stats.percentileofscore(momentum[c + '_Price_Return'], momentum[c + '_Price_Return'].loc[index])
        momentum[c + '_percentile'][index] = percentile_change 
#momentum['Shares To Buy'] = 0
    
#Calculate HQM score
#Get the mean of all 4 percentiles 
momentum['HQM_score'] = 0
from statistics import mean
for index, row in momentum.iterrows(): 
    all_periods_p = [row['y1_percentile'], row['m6_percentile'], row['m3_percentile'], row['m1_percentile']]
    momentum['HQM_score'].iloc[index] = mean(all_periods_p)

print(momentum.columns)

#PUSH TO DATABASE
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
momentum.to_sql(name='momentum', con=engine, if_exists='replace', index=False)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()