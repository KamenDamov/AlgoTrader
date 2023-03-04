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

#query = """
#CREATE TABLE IF NOT EXISTS users (
#    username TEXT NOT NULL,
#    email TEXT NOT NULL,
#    password TEXT NOT NULL, 
#    funds FLOAT     
#);
#"""

cur.execute(query)

conn.commit()
cur.close()
conn.close()