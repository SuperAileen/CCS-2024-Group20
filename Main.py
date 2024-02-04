import matplotlib.pyplot as plt
import pickle
from HelpingFunctions import *
from ContagionMechanism import *
from OrderBook import *
from Constants import *


# Initialize dictionary to hold agent information
agents_dict = {}

# Initialize past price with initial price P_0 for T_MAX time steps
past_price = [P_0 for i in range(T_MAX)]

# Initialize fundamentalist agents
for i in range(N_FUND):
    ep = ep_fundamentalist(P_0, P_F)
    agents_dict[i] = ['fund',
                      W[i],
                      M,
                      Q,
                      ep,
                      determine_order_type(ep, P_0, TAO, M, Q),
                      np.random.uniform(0, Ith),
                      0
                      ]

# Initialize chartist agents
for i in range(N_FUND, N_FUND + N_CHART):
    ep = ep_chartist(P_0, past_price)
    agents_dict[i] = ['chart',
                      W[i],
                      M,
                      Q,
                      ep,
                      determine_order_type(ep, P_0, TAO, M, Q),
                      np.random.uniform(0, Ith),
                      0
                      ]

# Set order price for each agent based on their decision
for agent_id in agents_dict:
    decision = agents_dict[agent_id][5]
    order_price = set_order_price(decision, agents_dict[agent_id][4], P_0, agents_dict[agent_id][2])
    agents_dict[agent_id][7] = order_price

# Create network structure
network = create_lattice_small_world_network()

# Initialize OrderBook and Network objects
ob = OrderBook(DELTA, agents_dict)
nw = Network(ALPHA, ob.agents_dict, network)

# Run network cycle for a specified number of times
for cycle in range(10000):
    print("i", cycle)
    nw.network_cycle()

# Plot the size of information avalanches over time
plt.plot(range(len(nw.info_counts)), nw.info_counts)
plt.xlabel("Time Steps")
plt.ylabel("Size of Info Avalanche")
plt.title("Time Series of Info Avalanches")
plt.savefig("Avalanche.png")

# Save the Network object to a file
with open('nw_object.pkl', 'wb') as file:
    pickle.dump(nw, file)

# Simulation 1 cycle
# ob = OrderBook(DELTA, agents_dict)
current_market_price = P_0
simulations = 9000
asset_prices = []

# Run the simulation for a specified number of times
for sim in range(simulations):
    ob.agents_dict = nw.agents_dict  # Send Network agents_dict to Orderbook
    
    # Place bids or asks based on agents' decisions
    for agent_id in ob.agents_dict:
        decision = ob.agents_dict[agent_id][5]
        order_price = ob.agents_dict[agent_id][7]
        if decision == "buy":
            ob.place_bid(agent_id, order_price)
        elif decision == "sell":
            ob.place_ask(agent_id, order_price)
    
    # Set aggregate price and update past price
    current_market_price = ob.set_aggregate_price(current_market_price)
    asset_prices.append(current_market_price)
    past_price.pop(0)
    past_price.append(current_market_price)

    # Update fundamentalist and chartist agents' expected prices and decisions
    for agent_id in range(N_FUND):
        ep = ep_fundamentalist(current_market_price, P_F)
        ob.agents_dict[agent_id][4] = ep
        ob.agents_dict[agent_id][5] = determine_order_type(ep,
                                                          current_market_price,
                                                          TAO, ob.agents_dict[agent_id][2],
                                                          ob.agents_dict[agent_id][3])
    for agent_id in range(N_FUND, N_FUND + N_CHART):
        ep = ep_chartist(current_market_price, past_price)
        ob.agents_dict[agent_id][4] = ep
        ob.agents_dict[agent_id][5] = determine_order_type(ep,
                                                           current_market_price,
                                                           TAO, ob.agents_dict[agent_id][2],
                                                           ob.agents_dict[agent_id][3])

    # Update the network and run a network cycle
    nw = Network(ALPHA, ob.agents_dict, network)
    nw.network_cycle()

# Plot asset prices at different time steps

plt.figure().set_figwidth(15)
plt.plot(list(range(len(asset_prices))), asset_prices, label='asset price')
plt.axhline(y=120, color='r', linestyle='--', label='fundamental price 120')
plt.xlabel("Time Steps")
plt.ylabel("Asset Price")
plt.legend()
plt.savefig("Asset Price 9000 Timestep.png")







# Calculate and Plot the return distribution
asset_prices_subset = asset_prices

# Calculate returns rt
rt = np.log(asset_prices_subset[1:]) - np.log(asset_prices_subset[:-1])

# Calculate average return and standard deviation
r_avg = np.mean(rt)
r_stdev = np.std(rt)

# Calculate normalized returns r^NORM
r_norm = (rt - r_avg) / r_stdev
r_norm_filtered = r_norm[(r_norm > -3) & (r_norm < 3)]

# Plot the asset price time series
plt.figure().set_figwidth(15)
plt.plot(asset_prices_subset, color='steelblue')
plt.axhline(y=120, color='r', linestyle='--')
plt.title('Asset Price Time Series (First 2000 Points)')
plt.xlabel('Time Steps')
plt.ylabel('Asset Price')
plt.show()

# Plot the normalized returns time series
plt.figure().set_figwidth(15)
plt.plot(r_norm, color='black')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('Normalized Returns (First 2000 Points)')
plt.xlabel('Time Steps')
plt.ylabel('Normalized Returns')
plt.show()

# Calculate the probability density function (PDF) of the normalized returns
counts, bin_edges = np.histogram(r_norm, bins=200, density=True)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Plot the PDF of the normalized returns
plt.figure(figsize=(10, 6))
plt.scatter(bin_centers, counts, label='OB-CFP Model', color='blue')

# Definition of the q-Gaussian function
def q_gaussian(x, A, B, q):
    return A * np.power(1 - (1 - q) * B * np.power(x, 2), 1 / (1 - q))

# Parameters for the q-Gaussian
A = 0.98
B = 7
q_list = np.arange(1.3, 2.0, 0.1)  # Including q=2.0 as per the plot in the provided image

# Plot the q-Gaussian
for q in q_list:
    plt.plot(bin_centers, q_gaussian(bin_centers, A, B, q), label=f'q-Gaussian q={q:.1f}')

# Set x-axis and y-axis limits
plt.xlim(-10, 10)
plt.ylim(10**-3, 10**0.4) 
plt.yscale('log')
plt.xlabel('Normalized Returns')
plt.ylabel('Probability Density')
plt.legend()
plt.show()


# Plot the evolution of asset, money, and wealth distribution

fig, axs = plt.subplots(4, 3, figsize=(15, 20)) 


# Colors for different plots
colors = ['red', 'blue', 'green']

# Iterate through each timestep and each data type to plot
for i, (t, data_dict) in enumerate(data_at_timesteps.items()):
    axs[i, 0].hist(data_dict['asset_quantities'], bins=30, color=colors[0])
    axs[i, 1].hist(data_dict['monies'], bins=30, color=colors[1])
    axs[i, 2].hist(data_dict['total_wealths'], bins=30, color=colors[2])
    
    # Set titles and axis labels for each subplot
    axs[i, 0].set_title(f'Asset Quantity at t={t}')
    axs[i, 1].set_title(f'Money at t={t}')
    axs[i, 2].set_title(f'Total Wealth at t={t}')
    
# Adjust spacing between subplots
plt.tight_layout()
plt.show()


