import azure.functions as func
import logging
import pandas
import json
import indicators


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="calc-rsi", methods=["GET", "POST"])
def rsi(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('RSI function processed a request.')
    # Get the RSI parameters from the request
    period = req.get_json().get('rsi_length')
    # If period is not specified, default to 14
    if period is None:
        period = 14
    # Get which value from candle_open, high, low, candle_close to use
    value = req.get_json().get('rsi_value')
    # If value is not specified, default to candle_close
    if value is None:
        value = 'candle_close'
    if value not in ['candle_open', 'high', 'low', 'candle_close']:
        return func.HttpResponse(
            f"Invalid value for rsi_value: {value}",
            status_code=400
        )
    # Convert candlestick_data to a pandas dataframe
    candlestick_data = req.get_json().get('candlestick_data')
    candle_dataframe = pandas.DataFrame(json.loads(candlestick_data))
    # Confirm that the column for value is in the dataframe
    if value not in candle_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in candlestick, {value} not found",
            status_code=400
        )
    # Check for timestamp
    if 'candle_timestamp' not in candle_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in candlestick, candle_timestamp not found",
            status_code=400
        )
    # Make sure timestamp is in datetime format
    candle_dataframe['candle_timestamp'] = pandas.to_datetime(candle_dataframe['candle_timestamp'])
    # Sort by timestamp
    candle_dataframe = candle_dataframe.sort_values(by='candle_timestamp')
    # Calculate the RSI
    candle_dataframe = indicators.calc_rsi(candle_dataframe, period=period, value=value)
    # Convert the dataframe to a dictionary
    candlestick_data = candle_dataframe.to_json(orient='records')
    # Create the return payload
    payload = {
        'candlestick_data': candlestick_data,
        'rsi_length': period,
        'rsi_value': value,
    }
    # Convert the payload to JSON
    payload = json.dumps(payload)
    # Return the payload
    return func.HttpResponse(
        payload,
        status_code=200
    )

