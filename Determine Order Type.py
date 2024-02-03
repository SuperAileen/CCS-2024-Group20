def determine_order_type(expected_price, p_t, TAO, money, asset_quantity):
    """
    Determine the order type of a trader based on the expected price, current price,
    sensitivity threshold, available money, and asset quantity

    Parameters:
    expected_price (float): The expected price of the asset
    p_t (float): The current market price of the asset
    TAO (int): The threshold to decide whether to hold
    money (float): The amount of money the trader has
    asset_quantity (int): The quantity of the asset the trader holds

    Returns:
    str: The order type ('buy', 'sell', or 'hold')
    """

    if expected_price > p_t + TAO:
        if money > 0:
            return "buy"        # Buy the asset (bidder)
    elif expected_price < p_t - TAO:
        if asset_quantity > 0:
            return "sell"       # Sell the asset (asker)
    else:
        return "hold"            # Hold without setting any orders