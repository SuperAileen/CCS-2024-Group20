def set_order_price(order_type, expected_price, current_price, money):
    """
    Set the order price for a trader based on their order type, expected price,
    current price, and the amount of money they have

    Parameters:
    order_type (str): The type of order ('buy', 'sell', or 'hold')
    expected_price (float): The expected price of the asset
    current_price (float): The current market price of the asset
    money (float): The amount of money the trader has
    
    Returns:
    float: The price set for the order
    """
    if order_type == 'buy':
        order_price = np.random.uniform(0, min(money, expected_price))
        if order_price < 0:
            return 0
        else:
            return order_price
    elif order_type == 'sell':
        order_price = np.random.uniform(expected_price, current_price)
        if order_price < 0:
            return 0
        else:
            return order_price
    else:
        return 0


def set_order_price_random(order_type, current_price, money):
    if order_type == 'buy':
        return np.random.uniform(0, min(money, current_price+50))
    elif order_type == 'sell':
        return np.random.uniform(current_price, current_price-50)
    else:
        return 0