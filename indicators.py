import pandas_ta as ta
import pandas as pd


# Function to calculate RSI
def calc_rsi(candle_dataframe, period=14, value='candle_close'):
    """
    Function to calculate RSI using Pandas TA library. https://github.com/twopirllc/pandas-ta
    :param candlestick_data: Dataframe containing candlestick data
    :param period: Length of RSI, default is 14
    :param value: Which value to use, default is candle_close
    """
    # Calculate the RSI
    rsi = ta.rsi(close=candle_dataframe[value], length=period)
    # Concat to the original dataframe
    candle_dataframe['rsi'] = rsi
    return candle_dataframe
