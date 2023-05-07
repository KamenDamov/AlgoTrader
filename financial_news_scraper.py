#Extract news data from MarketWatch
#Use chatgpt for recommended stocks based on metrics

#Imports
import dateutil
import psycopg2
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil import parser
import time

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
    time.sleep(60)
    print("Producing for: " + t)
    url = "https://www.marketwatch.com/investing/stock/" + t.lower()
    target = "marketshare"
    data = requests.get(url).content
    soup = bs(data, 'html.parser') 
    news = []

    #Grab all the news from most recent date
    for element in soup.select('.article__content'):
        currNews = element.text.strip().split("  ")
        headline = []
        date = []
        source = currNews[-1].split("\n")[-1]
        try:
            date_string = currNews[-1].split("\n")[-2]
        except IndexError: 
            print("DAte string not found")
            date_string = " "
        try:
            parsed_date = parser.parse(date_string)
            date = parsed_date.strftime("%Y-%m-%d")
        except dateutil.parser._parser.ParserError:
            print("NO date")
            date = " "        
        headline = currNews[:-2]

        result = []
        current_word = ""
        for element in headline:
            if element.strip() == "":
                continue  # Skip empty strings and newline characters
            current_word += element.strip() + " "

        if current_word != "":
            result.append(current_word.strip())
        try:
            news.append((t,date,result[0],source))
        except IndexError: 
            news.append((t,date," ", source))

    allDates = []
    for i in range(len(news)):
        try:
            compare = datetime.strptime(news[i][1], "%Y-%m-%d")
            allDates.append(compare)
        except ValueError:
            continue
    try: 
        mostRecent = max(allDates).strftime("%Y-%m-%d")
    except ValueError:
        continue
    newsToKeep = []
    for i in range(len(news)): 
        if news[i][1] == mostRecent: 
            newsToKeep.append(news[i])
    print(newsToKeep)
    for news in newsToKeep:
        try: 
            print(news)
            cur.execute("INSERT INTO financial_news (ticker, date, news, source) VALUES (%s, %s, %s, %s)", (news[0], news[1], news[2], news[3]))
            conn.commit()
        except IndexError: 
            print("No news found")
            cur.execute("INSERT INTO financial_news (ticker, date, news, source) VALUES (%s, %s, %s)", (news[0], news[1], news[2], news[3]))
            conn.commit()