#Extract news data from MarketWatch
#Use chatgpt for recommended stocks based on metrics

#Imports
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil import parser

url = "https://www.marketwatch.com/investing/stock/aapl"
target = "marketshare"
data = requests.get(url).content
soup = bs(data, 'html.parser') 
draftNames=[]
for element in soup.select('.article__content'):
    currNews = element.text.strip().split("  ")
    #print(currNews[-1].lower())
    headline = ''
    date = ''
    if "marketwatch" in currNews[-1].lower(): 
        date_string = currNews[-1].split("\n")[-2]
        parsed_date = parser.parse(date_string)
        date = parsed_date.strftime("%Y-%m-%d")

        headline = currNews
        print(headline)
        print(date)
    #print("\n\n\n")