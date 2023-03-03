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

<<<<<<< HEAD
query = '''

'''

cur.execute(query)
=======
cur.execute("")
>>>>>>> parent of f84b541f (push)

conn.commit()
cur.close()
conn.close()