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
    Ticker VARCHAR(10)    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(ticker_query)

########################################################
with 

for line in input_data.strip().split('\n'):
    # Split the line into two values: index and ticker
    index, ticker = line.strip().split(',')
    cur.execute("INSERT INTO tickers (index, tickers) VALUES (%s, %s);", (index, ticker))

conn.commit()
cur.close()
conn.close()
