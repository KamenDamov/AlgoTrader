import numpy as np
import matplotlib.pyplot as plt

# Define stock parameters
mean_return = -0.01
volatility = 0.01
current_price = 100

# Set number of simulations and time horizon
num_simulations = 10000
time_horizon = 100 # number of trading days in a year

# Create empty matrix to store simulated prices
price_matrix = np.zeros((time_horizon, num_simulations))

# Loop over simulations
for i in range(num_simulations):
    # Generate random returns for the stock
    returns = np.random.normal(mean_return, volatility, time_horizon)
    
    # Compute price path for each day using geometric Brownian motion
    prices = [current_price]
    for j in range(1, time_horizon):
        prices.append(prices[j-1] * np.exp(returns[j]))
        
    # Add simulated prices to matrix
    price_matrix[:, i] = prices
    
# Compute mean and standard deviation of simulated prices for each day
price_means = np.mean(price_matrix, axis=1)
price_stddevs = np.std(price_matrix, axis=1)

# Plot results
plt.plot(price_means)
plt.fill_between(range(time_horizon), price_means-price_stddevs, price_means+price_stddevs, alpha=0.2)
plt.title('Simulated Prices for Added Stock')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()
print("Done")