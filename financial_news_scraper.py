#Extract news data from MarketWatch
#Use chatgpt for recommended stocks based on metrics

#Imports
import psycopg2
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil import parser

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

#TODO
#Add for loop that iterates all stocks in db
# Produce record and push to db
#  
for t in tick:
    url = "https://www.marketwatch.com/investing/stock/" + t.lower()
    target = "marketshare"
    data = requests.get(url).content
    soup = bs(data, 'html.parser') 
    news = []
    for element in soup.select('.article__content'):
        currNews = element.text.strip().split("  ")
        #print(currNews[-1].lower())
        headline = []
        date = []
        if "marketwatch" in currNews[-1].lower(): 
            date_string = currNews[-1].split("\n")[-2]
            parsed_date = parser.parse(date_string)
            date = parsed_date.strftime("%Y-%m-%d")

            headline = currNews[:-2]

            result = []
            current_word = ""

            for element in headline:
                if element.strip() == "":
                    continue  # Skip empty strings and newline characters
                current_word += element.strip() + " "

            if current_word != "":
                result.append(current_word.strip())

            news.append((t,result[0],date))
        #print("\n\n\n")