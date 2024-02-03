# Function to calculate expected price for one fundamentalist
def ep_fundamentalist(p_t, P_F):
    """
    Calculate the expected price for a fundamentalist trader

    Parameters:
    p_t (float): The current market price of the asset
    p_f (float): The perceived fundamental price of the asset for the trader

    Returns:
    float: The expected price for the asset for a fundamentalist trader
    """
    noise = np.random.uniform(-SIGMA, SIGMA)
    # Was not too sure about using an uniform or normal distribution here
    p_f = np.random.uniform(P_F - THETA, P_F + THETA)
    ep = p_t + PHI * (p_f - p_t) + noise
    if ep < 0:
        return 0
    return ep

# Function to calculate expected price for one chartist
def ep_chartist(p_t, past_prices):
    """
    Calculate the expected price for a chartist trader

    Parameters:
    p_t (float): The current market price of the asset
    past_prices (list of float): A list of past market prices of the asset

    Returns:
    float: The expected price for the asset as calculated by a chartist trader
    """
    assert len(past_prices) == T_MAX, "past_prices must be a list of 15 values"
    chartist_T = np.random.randint(2, T_MAX)
    p_T = np.mean(past_prices[-chartist_T:]) 
    noise = np.random.uniform(-SIGMA, SIGMA)
    ep = p_t + KAPPA/(chartist_T) * (p_t - p_T) + noise
    if ep < 0:
        return 0
    return ep

# Function that determines the choice one random trader makes
def rand_trader(money, asset_quantity):
    choice = random.choice(['buy', 'sell', 'hold'])
    if choice == 'buy' and money > 0:
        return 'buy'
    elif choice == 'sell' and asset_quantity > 0:
        return 'sell'
    else:
        return 'hold'
    

    