# traderbot: democratizing advanced trading

## Open Source Indicators and Analysis
A series of API's exposed to simplify getting indicators and analysis. 

## References
1. [Panda's TA](https://github.com/twopirllc/pandas-ta)-> A python implementation of the widely used TA Lib. Uses TA-Lib for backend calculations where needed. 
2. [AppnologyJames YouTube](https://www.youtube.com/channel/UC1sfWAyk-48pGy58lgehKFA) -> YouTube channel of one of our founders
3. [AppnologyJames Medium](https://medium.com/@appnologyjames) -> Blog from one of our founders

## Follow Our Journey
1. [Landing Page and Sign Up](https://traderbotsignup.vercel.app/)
2. [Toy Version WIP](https://traderbotdemo.vercel.app/)
3. [Demo Video](https://www.youtube.com/watch?v=E1t8gG64pAk&t=12s)
4. [LinkedIn - James Hinton, Founder](https://www.linkedin.com/in/jameshinton84/)
5. [LinkedIn - Mitaanshu Agarwal](https://www.linkedin.com/in/mitaanshu-agarwal/)
6. [Twitter (X)](https://twitter.com/algoquant_trade)

## Indicators
### RSI: Relative Strength Index
The Relative Strength Index is a popular indicator used by traders to identify overbought or oversold conditions. 

*Find Out More*: [Relative Strength Index (RSI) Indicator Explained with Examples, Strategies and a little bit of code](https://medium.com/@appnologyjames/relative-strength-index-rsi-indicator-explained-with-examples-strategies-and-a-little-bit-of-d2973a74198a)

#### To Use
*API QUERY*
```
url: https://indicators-and-analysis.azurewebsites.net/api/calc-rsi
payload: {
    rsi_length: <length, defaults to 14>,
    rsi_value: <the value to calculate RSI on, defaults to 'candle_close'>,
    candle_timestamp: <timestamp of the candles, required>,
    candlestick_data: <data to draw from, required>
}
```
*API RETURN*
```
{
    candlestick_data: <now includes ye olde RSI>,
    rsi_length: <the length used for RSI calculation>,
    rsi_value: <the value used for the RSI atomic data>
}
```

### EMA: Exponential Moving Average
The Exponential Moving Average is a popular indicator to identify momentum changes and directions. 

*Find Out More* [How to Build a 20-EMA on MetaTrader with Python and Pandas](https://medium.com/trading-data-analysis/how-to-build-a-20-ema-on-metatrader-with-python-and-pandas-60af03d1516c)

#### To Use
*API QUERY*
```
url: https://indicators-and-analysis.azurewebsites.net/api/calc-ema
payload: {
    ema_length: <length, defaults to 20>,
    ema_value: <the value to calculate the EMA on, defaults to 'candle_close'>,
    candle_timestamp: <timestamp of the candles, required>,
    candlestick_data: <data to perform calculations on, required>,
    accuracy_filter: <eliminate the ema_length * 5 rows to allow EMA to be accurate. Defaults to True>
}
```
*API RETURN*
```
{
    candlestick_data: <original data with candlesticks added>,
    ema_length: <length of the ema>,
    ema_value: <the column of the data the ema was calculated on>,
    accuracy_filter: <the value of the accuracy filter which was used>,
    ema_name: <the name of the columns generated>
}
```

### Ichimoku Cloud
The Ichimoku Cloud is a collection of technical indicators that show support and resistance levels, as well as momentum and trend direction.

*Find Out More* [What Is the Ichimoku Cloud Technical Analysis Indicator](https://www.investopedia.com/terms/i/ichimoku-cloud.asp)

#### To Use
*API QUERY*
```
url: https://indicators-and-analysis.azurewebsites.net/api/calc-ichimoku
payload: {
    tenkan: <tenkan value>,
    kijun: <kijun value>,
    senoku: <senoku value>,
    high_value: <column of candlestick to get high value from. Default 'high'>,
    low_value: <column of candlestick to get low value from. Default 'low'>,
    close_value: <column of candlestick to get close value from. Default 'candle_close'>,
    candlestick_data: <trade_data to assess for ichimoku>
}
```
*API RETURN*
Returns the ichimoku and the ichimoku shifted down by the offset. This means you can easily check the future value of the Ichimoku against a current row. 
```
{
    'candlestick_data': candlestick_data with Ichimoku columns added,
    'tenkan': tenkan,
    'kijun': kijun,
    'senoku': senoku,
    'high_value': high_value,
    'low_value': low_value,
    'close_value': close_value,
    'isa_name': f'ISA_{tenkan}',
    'isb_name': f'ISB_{kijun}'
}
```
