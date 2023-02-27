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

all_time_prices_query = '''
CREATE TABLE IF NOT EXISTS all_time_prices (
    Date TIMESTAMP,
    Open FLOAT,
    High FLOAT, 
    Low FLOAT, 
    Close FLOAT, 
    Volume FLOAT,
    Dividends FLOAT, 
    Stock_Splits FLOAT, 
    Ticker TEXT NOT NULL    
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(all_time_prices_query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
