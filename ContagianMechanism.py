import random
import networkx as nx
import numpy as np


def create_lattice_small_world_network():
    """
    Create a small-world network based on a 2D lattice with rewired edges.

    Returns:
        nx.Graph: Small-world network
    """
    n = 40  # Size of the lattice (n x n)
    k = 4   # Each node is connected to its k nearest neighbors
    p = 0.02  # Probability of rewiring each edge

    # Create a 2D square lattice
    lattice = nx.grid_2d_graph(n, n)

    # Rewire edges with probability p while preserving node degrees
    for edge in list(lattice.edges()):
        if random.random() < p:
            u, v = edge
            possible_edges = [(u, w) for w in lattice if w != v and not lattice.has_edge(v, w)]
            if possible_edges:
                new_v = random.choice(possible_edges)[1]
                lattice.remove_edge(u, v)
                lattice.add_edge(u, new_v)
    return lattice

class Network:
    
    def __init__(self, alpha, agents_dict, network):
        """
        Initialize the OrderBook with the given delta value.

        Parameters:
        - delta (float): Parameter for price adjustment.
        """
    
        self.agents_dict = agents_dict # Dictionary containing each agents and information
        self.network = network 
        self.state_counts = {'buy': [], 'sell': [], 'hold': []}
        self.info_counts = []
        self.alpha = alpha
        self.Ith = Ith
        self.trade_counts = [] # Keep track of amount of trades per simulation
        
    def propagate_info(self, agent_index):
        """
        Propagate information of an agent to its neighbors in the network.

        Parameters:
        - agent_index (int): The index of the agent in the agents dictionary.
        """
        agent = self.agents_dict[agent_index]
        agent_coord = (agent_index // 40, agent_index % 40)  # Map index to coordinates
        neighbors_coords = list(self.network.neighbors(agent_coord))
        if agent[6] >= self.Ith:  # Check if agent's information exceeds the threshold
            self.info_counts[-1] += 1
            store_info = agent[6]
            self.agents_dict[agent_index][6] = 0  # Reset agent's information
            for neighbor_coord in neighbors_coords:
                neighbor_index = neighbor_coord[0] * 40 + neighbor_coord[1]  # Map coordinates to index
                self.agents_dict[neighbor_index][5] = agent[5]   # Propagate decision to neighbor
                self.agents_dict[neighbor_index][4] = agent[4]
                self.agents_dict[neighbor_index][7] = agent[7]
                self.agents_dict[neighbor_index][6] += (self.alpha / len(neighbors_coords)) * store_info
                self.agents_dict[neighbor_index][6] = min(self.agents_dict[neighbor_index][6], np.finfo(float).max)
                if self.agents_dict[neighbor_index][6] >= self.Ith:
                    self.propagate_info(neighbor_index)  # Recursive call

    def network_cycle(self):
        """
        Update the network for one simulation cycle and collect information for future plots.
        """
        self.info_counts.append(0)  # Reset agent information threshold crossing counter
        copy_agents = self.agents_dict.copy()
        # Add global information
        for agent_id in self.agents_dict:
            self.agents_dict[agent_id][6] += np.random.uniform(0, (self.Ith - max([copy_agents[agent_id][6] for agent_id in copy_agents])))
        # Contagion mechanism
        for i, _ in enumerate(self.agents_dict):
            self.propagate_info(i)