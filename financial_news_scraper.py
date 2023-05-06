#Extract news data from MarketWatch
#Use chatgpt for recommended stocks based on metrics

#Imports
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil import parser


#TODO
#Add for loop that iterates all stocks in db
# Produce record and push to db 
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

        headline = currNews[:-2]

        result = []
        current_word = ""

        for element in headline:
            if element.strip() == "":
                continue  # Skip empty strings and newline characters
            current_word += element.strip() + " "

        if current_word != "":
            result.append(current_word.strip())

        print(result)  
        #print(headline)
        print(date)
    #print("\n\n\n")