import psycopg2

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
    Ticker TEXT NOT NULL    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(ticker_query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()