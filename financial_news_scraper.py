#Extract news data from MarketWatch
#Use chatgpt for recommended stocks based on metrics

#Imports
import requests
from bs4 import BeautifulSoup as bs

url = "https://www.marketwatch.com/investing/stock/aapl"
target = "marketshare"
data = requests.get(url).content
soup = bs(data, 'html.parser') 
draftNames=[]
for element in soup.select('.article__content'):
    currNews = element.text.strip().split("  ")
    #print(currNews[-1].lower())
    if "marketwatch" in currNews[-1].lower(): 
        print(currNews)
    #print("\n\n\n")