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
    print(element.text.strip())
    #print("\n\n\n")