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

#Append new stock to all_time_users
for s in all_stocks:
    print(s)
    info = yf.Ticker(s).history(period='max')
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    info.to_sql('all_time_prices', engine, if_exists = 'append', index = False)

#Append missing stock data by querying most recent date
for t in tick: 
    maxDateQuery = 'SELECT "Date" FROM public.all_time_prices WHERE "Ticker" =  '+ t +' Order by "Date" desc LIMIT (1);'
    cur.execute(maxDateQuery)
    maxDate = [row[0] for row in cur.fetchall()]
    startDate = maxDate[0].strftime('%Y-%m-%d')
    new_period = yf.Ticker(t).history(start=startDate)
    new_period = new_period.reset_index()
    new_period['Stock_Splits'] = new_period['Stock Splits']
    new_period = new_period.drop("Stock Splits", axis=1)
    new_period['Ticker'] = t 
    print(new_period.columns)
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    new_period.to_sql('all_time_prices', engine, if_exists = 'append', index = False)
    print(new_period)