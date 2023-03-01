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

momentum_query = '''
CREATE TABLE IF NOT EXISTS momentum (
    Ticker TEXT NOT NULL,
    Price FLOAT,
    y1_Price_Return FLOAT, 
    y1_percentile FLOAT, 
    m6_Price_Return FLOAT, 
    m6_percentile FLOAT,
    m3_Price_Return FLOAT, 
    m3_percentile FLOAT, 
    m1_Price_Return FLOAT, 
    m1_percentile FLOAT, 
    Weighted_Hurst_Exponent FLOAT,
    HQM_score FLOAT
);
'''

# Execute a CREATE TABLE statement to create a new table
cur.execute(momentum_query)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()