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

query = """
-- Add foreign key constraint to the all_time_prices table
ALTER TABLE all_time_prices
ADD CONSTRAINT Prices_Ticker_id_fkey
FOREIGN KEY (Ticker)
REFERENCES tickers(ticker);


-- Add foreign key constraint to the momentum table
ALTER TABLE momentum
ADD CONSTRAINT Prices_Ticker_id_fkey
FOREIGN KEY (Ticker)
REFERENCES tickers(ticker);

-- Add foreign key constraint to the indicators table
ALTER TABLE indicators
ADD CONSTRAINT Prices_Ticker_id_fkey
FOREIGN KEY (ticker)
REFERENCES tickers(ticker);
"""

cur.execute(query)
cur.close()
conn.close()
