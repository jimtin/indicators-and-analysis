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


# Function to calculate the Ichimoku Cloudtenkan=9, kijun=26, senoku=52
def calc_ichimoku(candle_dataframe, tenkan=9, kijun=26, senoku=52, high_value='high', low_value='low', close_value='candle_close'):
    """
    Function to calculate Ichimoku Cloud using Pandas TA library.
    :param candlestick_data: Dataframe containing candlestick data
    :param tenkan: Length of Tenkan, default is 9
    :param kijun: Length of Kijun, default is 26
    :param senoku: Length of Senoku, default is 52
    :param value: Which value to use, default is candle_close
    """
    # Calculate the ichimoku cloud
    ichimoku = ta.ichimoku(
        high=candle_dataframe[high_value], 
        low=candle_dataframe[low_value], 
        close=candle_dataframe[close_value], 
        tenkan=tenkan, 
        kijun=kijun, 
        senkou=senoku
    )
    # Get the ISA name
    isa_name = f'ISA_{tenkan}'
    # Get the ISB name
    isb_name = f'ISB_{kijun}'
    # Rename the columns of ichimoku[1] to be the isa_name and isb_name with "_future" appended
    ichimoku[1].rename(columns={isa_name: f"{isa_name}_future", isb_name: f"{isb_name}_future"}, inplace=True)
    # Concat ichimoku[1] to data
    candle_dataframe = pd.concat([candle_dataframe, ichimoku[0], ichimoku[1]], axis=1)
    # Add columns for spanA and spanB
    candle_dataframe["spanA"] = 0.0
    candle_dataframe["spanB"] = 0.0
    # For spanA set it to be the value of the isa_name as long as the values are not NaN
    candle_dataframe.loc[candle_dataframe[isa_name].notnull(), "spanA"] = candle_dataframe[isa_name]
    # For spanB set it to be the value of the isb_name as long as the values are not NaN
    candle_dataframe.loc[candle_dataframe[isb_name].notnull(), "spanB"] = candle_dataframe[isb_name]
    # For spanA set it to the value of the isa_name_future as long as the values are not NaN
    candle_dataframe.loc[candle_dataframe[f"{isa_name}_future"].notnull(), "spanA"] = candle_dataframe[f"{isa_name}_future"]
    # For spanB set it to the value of the isb_name_future as long as the values are not NaN
    candle_dataframe.loc[candle_dataframe[f"{isb_name}_future"].notnull(), "spanB"] = candle_dataframe[f"{isb_name}_future"]
    # Shift all spanA values backward by kijun
    candle_dataframe["spanA_update"] = candle_dataframe["spanA"].shift(kijun*-1)
    # Shift all spanB values backward by kijun
    candle_dataframe["spanB_update"] = candle_dataframe["spanB"].shift(kijun*-1)
    # Rename spanA and spanB to spanA_unshifted and spanB_unshifted
    candle_dataframe.rename(columns={"spanA": "spanA_unshifted", "spanB": "spanB_unshifted"}, inplace=True)
    # Drop isa_name, isb_name, isa_name_future, isb_name_future columns
    candle_dataframe.drop(columns=[isa_name, isb_name, f"{isa_name}_future", f"{isb_name}_future"], inplace=True)
    # Rename spanA_update to spanA
    candle_dataframe.rename(columns={"spanA_update": "spanA_shifted"}, inplace=True)
    # Rename spanB_update to spanB
    candle_dataframe.rename(columns={"spanB_update": "spanB_shifted"}, inplace=True)
    # Drop any rows with NaN values
    candle_dataframe.dropna(inplace=True)
    return candle_dataframe
