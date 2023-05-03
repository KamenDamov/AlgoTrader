#Script to remove duplicates
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
-- create a temporary table with unique values
CREATE TEMPORARY TABLE temp_table AS 
SELECT DISTINCT * FROM all_time_prices;

-- delete the original table
DROP TABLE all_time_prices;

-- rename the temporary table to the original table name
ALTER TABLE temp_table RENAME TO all_time_prices;
"""

cur.execute(query)

conn.commit()
cur.close()
conn.close()