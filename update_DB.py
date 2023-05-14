#Script to update all_time_price table
#1) Update the tickers: 
#   - Run scraper and verify if it exists
#2) Update all_time_prices by getting the most recent date and extract data from the missing timespan

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
import math
import pytz

#DB connection
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

#Scrape tickers and update
l = "abcdefghijklmnopqrstuvwxyz"
#Getting NSYE stocks
all_stocks = []
for i in l:
    url = "https://en.wikipedia.org/wiki/Companies_listed_on_the_New_York_Stock_Exchange_(" + i.upper() + ")"
    data = requests.get(url)
    data = data.content
    soup = bs(data, "html.parser")
    raw = []
    for element in soup.select('table tbody tr td'):
        raw.append(element.text.strip())
    clean = raw[2::3]
    all_stocks.append(clean)

#Combine all lists
final_nyse_stocks = []
for sublist in all_stocks: 
    for item in sublist: 
        if item not in tick: 
            final_nyse_stocks.append(item)
all_stocks = final_nyse_stocks

#Getting NASDAQ stocks
nasdaq = []
for i in l: 
    url = 'https://www.eoddata.com/stocklist/NASDAQ/'+i.upper()+'.htm'
    data = requests.get(url)
    data = data.content
    soup = bs(data, "html.parser")
    new = []
    for i in soup.select(".quotes tr td "): 
        new.append(i.text)
    nasdaq.extend(new[::10][:-5])

new_nas = []
for n in nasdaq: 
    if n not in tick: 
        new_nas.append(n)

all_stocks = all_stocks + new_nas

#Append newly added stocks to tickers table
for a in all_stocks: 
    cur.execute("INSERT INTO tickers (ID, Ticker) VALUES (DEFAULT, %s)", (a,))

conn.commit()

#Append new stock to all_time_users
for s in all_stocks:
    print(s)
    print("About to run info")
    #Check if data is already up to date
    info = yf.Ticker(s).history(start = '2013-01-01')
    print(len(info))
    if 'Capital Gains' in info.columns: 
            del info['Capital Gains']
    if len(info) > 0:
        info['Stock_Splits'] = info['Stock Splits']
        info = info.drop("Stock Splits", axis=1)
        info = info.reset_index()

        # Calculate the daily returns
        try: 
            info['Returns'] = np.log(info['Close'] / info['Close'].shift(1))
            info['Volatility_30_Day'] = info['Returns'].rolling(window=30).std() * np.sqrt(252)
        except: 
            info['Returns'] = np.log(info['Close'] / info['Close'].shift(1))
            info['Volatility_30_Day'] = info['Returns'].rolling(window=len(info['Returns'])).std() * np.sqrt(252)

        info['Ticker'] = s
        print(info)
        engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
        info.to_sql('all_time_prices', engine, if_exists = 'append', index = False)
        conn.commit()

#TODO REMOVE DUPLCIATES
tz = pytz.timezone('America/New_York')
#Append missing stock data by querying most recent date
for t in tick: 
    print("Testing out "+t)
    maxDateQuery = "SELECT \"Date\" FROM public.all_time_prices WHERE \"Ticker\" = '" + t + "' Order by \"Date\" desc LIMIT (1);"
    cur.execute(maxDateQuery)
    maxDate = [row[0] for row in cur.fetchall()]
    try:
        currDate = datetime.strptime(maxDate[0].strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days = 1)
    except IndexError: 
        continue
    latestDate = currDate.strftime('%Y-%m-%d')
    #Produce returns and volatility by calling the api and keeping
    # only the records from maxDate and most current 
    volatilityAndReturns = yf.Ticker(t).history(start = "2013-01-01")
    volatilityAndReturns = volatilityAndReturns.reset_index()
    print(volatilityAndReturns)
    volatilityAndReturns["Returns"] = np.log(volatilityAndReturns['Close'] / volatilityAndReturns['Close'].shift(1))
    volatilityAndReturns['Volatility_30_Day'] = volatilityAndReturns['Returns'].rolling(window=30).std() * np.sqrt(252)

    #Keep only wanted values beyond a certain date
    parsed_timestamp = datetime.strptime(str(volatilityAndReturns["Date"].iloc[-1]), '%Y-%m-%d %H:%M:%S%z')
    formatted_date = parsed_timestamp.strftime('%Y-%m-%d')
    print(maxDate, formatted_date)
    volatilityAndReturns = volatilityAndReturns[(volatilityAndReturns['Date'] >= latestDate) & (volatilityAndReturns['Date'] <= formatted_date)]
    volatilityAndReturns = volatilityAndReturns[["Returns", "Volatility_30_Day"]]
    print(volatilityAndReturns)
    try: 
        startDate = datetime.strptime(maxDate[0].strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days = 1)
    except IndexError:
        print('No stock info') 
        continue
    new_period = yf.Ticker(t).history(start=startDate)
    new_period = new_period.reset_index()
    try:        
        new_period['Stock_Splits'] = new_period['Stock Splits'] 
    except KeyError: 
        print("Stock not found")
        continue
    """
    # Calculate the daily returns
    try: 
        new_period['Returns'] = np.log(new_period['Close'] / new_period['Close'].shift(1))
        new_period['Volatility_30_Day'] = new_period['Returns'].rolling(window=30).std() * np.sqrt(252)
    except: 
        new_period['Returns'] = np.log(new_period['Close'] / new_period['Close'].shift(1))
        new_period['Volatility_30_Day'] = new_period['Returns'].rolling(window=len(new_period['Returns'])).std() * np.sqrt(252)
    """
    new_period = new_period.drop("Stock Splits", axis=1)
    new_period['Ticker'] = t 
    if 'Capital Gains' in new_period.columns: 
            del new_period['Capital Gains']
    print(new_period.columns)
    print("Before : ", new_period)
    new_period["Returns"] = volatilityAndReturns["Returns"].tolist()#.reset_index(drop=True, inplace=True)
    print(new_period["Returns"], volatilityAndReturns["Returns"])
    new_period["Volatility_30_Day"] = volatilityAndReturns["Volatility_30_Day"].tolist()#.reset_index(drop=True, inplace=True)
    print(new_period.columns)
    print("After : ", new_period)
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    new_period.to_sql('all_time_prices', engine, if_exists = 'append', index = False)
    conn.commit()
    

#Update momentum
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
    try:
        #Creating the df to be added to all_time_prices
        ticker = tick[i]
        print("Doing " + ticker)
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
    except TypeError as e: 
        print("Nonetype found for: " + tick[i])
        print(e)
        break
        continue
    except IndexError: 
        print("Couldn't find: ",tick[i])
        continue
    except KeyError:
        print("Couldnt find key for: " + tick[i])
        continue
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

#Commit the transaction
conn.commit()

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

cur.execute(indicators_table)

for t in tick: 
    print("Producing for " + t)
    #Produce moving avg
    df = pd.read_sql_query("SELECT * FROM all_time_prices WHERE \"Ticker\" = '"+t+"'", conn)
    print(df)
    if len(df) == 0: 
        continue

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

    # create the SQL query with the variable values
    update_query = """
        UPDATE indicators SET RSI = {}, A_D = {}, ADX = {}, Last_200_MovAvg = {}, Recommendation = '{}' WHERE ticker_symbol = '{}';
    """.format(0 if math.isnan(rsi.iloc[-1]) else rsi.iloc[-1], 0 if math.isnan(df['AD'].iloc[-1]) else df['AD'].iloc[-1], 0 if math.isnan(df['ADX'].iloc[-1]) else df['ADX'].iloc[-1], 0 if math.isnan(df['MA'].iloc[-1]) else df['MA'].iloc[-1], recommendation, t)
    
    cur.execute(update_query)
    conn.commit()

#Close the cursor and connection
cur.close()
conn.close()
input("Press Enter to exit...")

#TODO Remove Dupes from all_time_prices