import psycopg2
import csv

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
    Ticker VARCHAR(20)  
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(ticker_query)

########################################################
with open('all_stocks', 'r') as f: 
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        index, ticker = row
        cur.execute("INSERT INTO tickers (ID, Ticker) VALUES (%s, %s);", (index, ticker))

conn.commit()
cur.close()
conn.close()
