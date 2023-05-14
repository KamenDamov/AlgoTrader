import numpy as np
import matplotlib.pyplot as plt
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

#Get the tickers as a list
#Query the stock price
#Querying AOS
cur.execute('SELECT * FROM all_time_prices where "Ticker" = \'AOS\'')
rows = cur.fetchall()
# Get the column names from the cursor's description
columns = [desc[0] for desc in cur.description]

# Create a pandas DataFrame from the fetched rows and column names
df = pd.DataFrame(rows, columns=columns) 
print(df)

# Set the random seed for reproducibility
np.random.seed(42)

# Define the initial stock price and parameters
initial_price = 100.0
drift = 0.5
volatility = 0.02
time_horizon = 1.0  # in years
num_steps = 252  # number of trading days in a year
num_simulations = 100  # number of simulations

# Calculate the daily drift and volatility
daily_drift = (drift - 0.5 * volatility ** 2) / num_steps
daily_volatility = volatility / np.sqrt(num_steps)

# Generate Brownian increments
dt = time_horizon / num_steps
increments = np.random.normal(0, daily_volatility * np.sqrt(dt), size=(num_steps, num_simulations))

# Calculate the stock price paths using Brownian motion
prices = np.zeros((num_steps + 1, num_simulations))
prices[0] = initial_price

for i in range(1, num_steps + 1):
    prices[i] = prices[i-1] * np.exp(daily_drift * dt + increments[i-1])

# Plot the stock price simulations
plt.figure(figsize=(10, 6))
for i in range(num_simulations):
    plt.plot(prices[:, i])
plt.xlabel('Time (days)')
plt.ylabel('Stock Price')
plt.title('Monte Carlo Simulation - Stock Price (Brownian Motion)')
plt.show()
