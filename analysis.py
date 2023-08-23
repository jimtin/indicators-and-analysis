import pandas as pd


# Function to calculate the Sharpe Ratio on stocks
def calc_sharpe(trade_dataframe, start_date, end_date, annual_risk_free_rate=0.033):
    """
    Function to calculate the Sharpe Ratio on stocks
    :param trade_dataframe: Dataframe containing trade data
    :param annual_risk_free_rate: Annual risk free rate, default is 3.3%
    """
    # Break the annual risk free rate into a daily rate
    rfr = 1 + annual_risk_free_rate
    rfr = rfr**(1/365)
    daily_rfr = rfr - 1
    # Add a column to the dataframe for daily_rfr
    trade_dataframe['daily_rfr'] = daily_rfr
    # For each row, calculate the number of days from the start of dataframe, using candle_timestamp
    trade_dataframe['days_from_start'] = trade_dataframe['exit_time'] - start_date
    # Convert days_from_start to a float
    trade_dataframe['days_from_start'] = trade_dataframe['days_from_start'].dt.days
    # Multiply daily_rfr by days_from_start to get the cumulative risk free rate
    trade_dataframe['cumulative_rfr'] = trade_dataframe['daily_rfr'] * trade_dataframe['days_from_start']
    # Calculate wins and losses
    trade_dataframe = calc_wins(trade_dataframe)
    # Add a column to the dataframe for excess_return
    trade_dataframe['excess_return'] = 0
    # Create a column to the dataframe called rfr_amount
    trade_dataframe['rfr_amount'] = 0
    # Set rfr_amount to be 1000000 * cumulative_rfr
    trade_dataframe['rfr_amount'] = 1000000 * trade_dataframe['cumulative_rfr']
    # Iterate through the dataframe
    for index, row in trade_dataframe.iterrows():
        # If the trade type was a BUY or BUY_STOP
        if row['order_type'] == 'BUY' or row['order_type'] == 'BUY_STOP':
            # Calculate the excess return
            trade_dataframe.loc[index, 'excess_return'] = ((row['exit_price'] - row['entry_price'])/row['entry_price']) * 1000000 - row['rfr_amount']
            # Calculate the raw return
            trade_dataframe.loc[index, 'raw_return'] = ((row['exit_price'] - row['entry_price'])/row['entry_price']) * 1000000
        # If the trade type was a SELL or SELL_STOP
        elif row['order_type'] == 'SELL' or row['order_type'] == 'SELL_STOP':
            # Calculate the excess return
            trade_dataframe.loc[index, 'excess_return'] = ((row['entry_price'] - row['exit_price'])/row['entry_price']) * 1000000 - row['rfr_amount']
            # Calculate the raw return
            trade_dataframe.loc[index, 'raw_return'] = ((row['entry_price'] - row['exit_price'])/row['entry_price']) * 1000000
    # Sum the raw_return
    raw_return = trade_dataframe['raw_return'].sum()
    # Now summarize the dataframe
    grouped = trade_dataframe.groupby([trade_dataframe['exit_time'].dt.date]).agg(
        {
            'exit_time': 'count',
            'excess_return': 'sum',
            'rfr_amount': 'first'
        }
    )
    # Get the max number of trades in a single day based on exit_time
    max_trades = grouped['exit_time'].max()
    # Subtract raw_return from max_trades * 1000000
    roi = raw_return / (max_trades * 1000000)
    # Get the standard deviation of excess_return
    std = grouped['excess_return'].std()
    # Get the mean of excess_return
    mean = grouped['excess_return'].mean()
    # Calculate the Sharpe Ratio
    sharpe = (mean - daily_rfr) / std
    # Convert the grouped dataframe to json
    grouped = grouped.to_json(orient='index')
    # Create the return object
    return_object = {
        'roi': roi,
        'sharpe_ratio': sharpe,
        'daily_breakdown': grouped,
        'raw_return': raw_return
    }
    # Return the dataframe
    return return_object


# Function to calculate wins and losses
def calc_wins(trade_dataframe):
    """
    Function to calculate wins and losses for trades
    :param trade_dataframe: Dataframe containing trade data
    """
    # Add a column to the dataframe for win
    trade_dataframe['win'] = 0
    # Iterate through the dataframe
    for index, row in trade_dataframe.iterrows():
        # If the trade type was a BUY or BUY_STOP
        if row['order_type'] == 'BUY' or row['order_type'] == 'BUY_STOP':
            # If the trade was a win
            if row['exit_price'] > row['entry_price']:
                # Set the win column to 1
                trade_dataframe.loc[index, 'win'] = 1
        # If the trade type was a SELL or SELL_STOP
        elif row['order_type'] == 'SELL' or row['order_type'] == 'SELL_STOP':
            # If the trade was a win
            if row['exit_price'] < row['entry_price']:
                # Set the win column to 1
                trade_dataframe.loc[index, 'win'] = 1
    # Return the dataframe
    return trade_dataframe
