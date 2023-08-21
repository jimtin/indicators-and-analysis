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
