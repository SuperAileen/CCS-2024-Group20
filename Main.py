import matplotlib.pyplot as plt
import pickle
from HelpingFunctions import *
from ContagionMechanism import *
from OrderBook import *

# Initialize agent attributes at T = 0
# structure of agent data
# agents = np.zeros(N, dtype=[('type', 'U10'),# 0
#                             ('wealth', 'f8'),# 1
#                             ('money', 'f8'), # 2
#                             ('assets', 'f8'), # 3
#                             ('expected_price', 'f8'), # 4
#                             ('decision', 'U10'), # 5
#                             ('info', 'f8')]) # 6
#                             ('order price') # 7

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
simulations = 10000
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
plt.plot(list(range(110)), asset_prices[:110], label='asset price')
plt.axhline(y=120, color='r', linestyle='--', label='fundamental price 120')
plt.xlabel("Time Steps")
plt.ylabel("Global Asset Price")
plt.legend()
plt.savefig("asset_price_t_110.png")

plt.figure().set_figwidth(15)
plt.plot(list(range(len(asset_prices))), asset_prices, label='asset price')
plt.axhline(y=120, color='r', linestyle='--', label='fundamental price 120')
plt.xlabel("Time Steps")
plt.ylabel("Global Asset Price")
plt.legend()
plt.savefig("asset_price_t_10000.png")
