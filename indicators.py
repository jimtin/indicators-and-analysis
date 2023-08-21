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


# Function to calculate EMA
def calc_ema(candle_dataframe, period=20, value='candle_close', accuracy_filter=True):
    """
    Function to calculate EMA using Pandas TA library.
    :param candlestick_data: Dataframe containing candlestick data
    :param period: Length of EMA, default is 20
    :param value: Which value to use, default is candle_close
    """
    # Calculate the EMA
    ema = ta.ema(close=candle_dataframe[value], length=period)
    # Concat to the original dataframe
    ema_name = f'ema_{period}'
    candle_dataframe[ema_name] = ema
    # If accuracy_filter is True, filter out the first period*5 rows
    if accuracy_filter:
        candle_dataframe = candle_dataframe.iloc[period*5:]
    return candle_dataframe
