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
import sqlite3
import time

#Create db
conn = sqlite3.connect('financial_data.db')

# Create a cursor
cursor = conn.cursor()
# Create the first table
users_query = '''
CREATE TABLE users (
    Username TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    Funds FLOAT, 
    Stock_In_Portfolio TEXT NOT NULL 
);
'''

cursor.execute(users_query)

conn.commit()