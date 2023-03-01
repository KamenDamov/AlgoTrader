import psycopg2
import pandas as pd

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    database="financial_db",
    user="postgres",
    password="KaMendiNiO"
)

# Open a cursor to perform database operations
cur = conn.cursor()

ticker_query = '''
CREATE TABLE IF NOT EXISTS tickers (
    ID INTEGER,
    Ticker TEXT NOT NULL    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(ticker_query)

########################################################
input_data = pd.read_csv('all_stocks')

#for line in input_data.strip().split('\n'):
    # Split the line into two values: index and ticker
#    index, ticker = line.strip().split(',')

#Add ticker data to the table
#with open('./all_stocks', 'r') as f: 
#    next(f)
#    cur.copy_from(f, 'tickers', sep=',') 

conn.commit()
cur.close()
conn.close()
