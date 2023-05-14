import numpy as np
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(42)

# Define the initial portfolio value and time horizon
initial_portfolio_value = 100000
time_horizon = 5  # in years

# Define the expected annual return and standard deviation of the stock portfolio
expected_return = 0.07
volatility = 0.15

# Calculate the daily return and annualized volatility
daily_return = np.log(1 + expected_return) / 252
annualized_volatility = volatility / np.sqrt(252)

# Define the number of simulations
num_simulations = 1000

# Generate the stock price scenarios using the Monte Carlo simulation
stock_prices = np.zeros((time_horizon * 252, num_simulations))
stock_prices[0] = initial_portfolio_value

for i in range(1, time_horizon * 252):
    random_returns = np.random.normal(daily_return, annualized_volatility, num_simulations)
    stock_prices[i] = stock_prices[i-1] * np.exp(random_returns)

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(stock_prices)
plt.xlabel('Time (days)')
plt.ylabel('Portfolio Value')
plt.title('Monte Carlo Simulation - Stock Portfolio')
plt.show()
print("Done")