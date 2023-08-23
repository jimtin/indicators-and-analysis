import azure.functions as func
import logging
import pandas
import json
import indicators
import analysis


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
    if value not in ['candle_open', 'high', 'low', 'candle_close', 'custom']:
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


@app.route(route="calc-ema", methods=["GET", "POST"])
def ema(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('EMA function processed a request.')
    # Get the EMA parameters from the request
    period = req.get_json().get('ema_length')
    # If period is not specified, default to 20
    if period is None:
        period = 20
    # Get which value from candle_open, high, low, candle_close to use
    value = req.get_json().get('ema_value')
    # If value is not specified, default to candle_close
    if value is None:
        value = 'candle_close'
    if value not in ['candle_open', 'high', 'low', 'candle_close', 'custom']:
        return func.HttpResponse(
            f"Invalid value for ema_value: {value}",
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
    # Check if accuracy_filter is specified
    accuracy_filter = req.get_json().get('accuracy_filter')
    if accuracy_filter is None:
        accuracy_filter = True
    else:
        accuracy_filter = bool(accuracy_filter)
    # Calculate the EMA
    candle_dataframe = indicators.calc_ema(candle_dataframe, period=period, value=value, accuracy_filter=accuracy_filter)
    # Convert the dataframe to json
    candlestick_data = candle_dataframe.to_json(orient='records')
    # Create the return payload
    payload = {
        'candlestick_data': candlestick_data,
        'ema_length': period,
        'ema_value': value,
        'accuracy_filter': accuracy_filter,
        'ema_name': f'ema_{period}'
    }
    # Convert the payload to JSON
    payload = json.dumps(payload)
    # Return the payload
    return func.HttpResponse(
        payload,
        status_code=200
    )


@app.route(route="calc-ichimoku", methods=["GET", "POST"])
def ichimoku(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Ichimoku function processed a request.')
    # Get the Ichimoku parameters from the request
    tenkan = req.get_json().get('tenkan')
    # If tenkan is not specified, default to 9
    if tenkan is None:
        tenkan = 9
    # Get the Ichimoku parameters from the request
    kijun = req.get_json().get('kijun')
    # If kijun is not specified, default to 26
    if kijun is None:
        kijun = 26
    # Get the Ichimoku parameters from the request
    senoku = req.get_json().get('senoku')
    # If senoku is not specified, default to 52
    if senoku is None:
        senoku = 52
    # Get which value from candle_open, high, low, candle_close to use
    high_value = req.get_json().get('high_value')
    # If value is not specified, default to high
    if high_value is None:
        high_value = 'high'
    if high_value not in ['candle_open', 'high', 'low', 'candle_close', 'custom']:
        return func.HttpResponse(
            f"Invalid value for high_value: {high_value}",
            status_code=400
        )
    # Get which value from candle_open, high, low, candle_close to use
    low_value = req.get_json().get('low_value')
    # If value is not specified, default to low
    if low_value is None:
        low_value = 'low'
    if low_value not in ['candle_open', 'high', 'low', 'candle_close', 'custom']:
        return func.HttpResponse(
            f"Invalid value for low_value: {low_value}",
            status_code=400
        )
    # Get which value from candle_open, high, low, candle_close to use
    close_value = req.get_json().get('close_value')
    # If value is not specified, default to candle_close
    if close_value is None:
        close_value = 'candle_close'
    if close_value not in ['candle_open', 'high', 'low', 'candle_close', 'custom']:
        return func.HttpResponse(
            f"Invalid value for close_value: {close_value}",
            status_code=400
        )
    # Convert candlestick_data to a pandas dataframe
    candlestick_data = req.get_json().get('candlestick_data')
    candle_dataframe = pandas.DataFrame(json.loads(candlestick_data))
    # Confirm that the timestamp column is in the dataframe
    if 'candle_timestamp' not in candle_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in candlestick, candle_timestamp not found",
            status_code=400
        )
    # Make sure timestamp is in datetime format
    candle_dataframe['candle_timestamp'] = pandas.to_datetime(candle_dataframe['candle_timestamp'])
    # Sort by timestamp
    candle_dataframe = candle_dataframe.sort_values(by='candle_timestamp')
    # Calculate the Ichimoku Cloud
    candle_dataframe = indicators.calc_ichimoku(candle_dataframe, tenkan=tenkan, kijun=kijun, senoku=senoku, high_value=high_value, low_value=low_value, close_value=close_value)
    # Convert the dataframe to json
    candlestick_data = candle_dataframe.to_json(orient='records')
    # Create the return payload
    payload = {
        'candlestick_data': candlestick_data,
        'tenkan': tenkan,
        'kijun': kijun,
        'senoku': senoku,
        'high_value': high_value,
        'low_value': low_value,
        'close_value': close_value,
        'isa_name': f'ISA_{tenkan}',
        'isb_name': f'ISB_{kijun}'
    }
    # Convert the payload to JSON
    payload = json.dumps(payload)
    # Return the payload
    return func.HttpResponse(
        payload,
        status_code=200
    )


@app.route(route="calc-sharpe", methods=["GET", "POST"])
def sharpe(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Sharpe function processed a request.')
    # Get the Sharpe parameters from the request
    annual_risk_free_rate = req.get_json().get('annual_risk_free_rate')
    # If annual_risk_free_rate is not specified, default to 0.033
    if annual_risk_free_rate is None:
        annual_risk_free_rate = 0.033
    # Get the start_date from the request
    start_date = req.get_json().get('start_date')
    # If start_date is not specified, return an error
    if start_date is None:
        return func.HttpResponse(
            f"Invalid request, start_date not found",
            status_code=400
        )
    # Get the end_date from the request
    end_date = req.get_json().get('end_date')
    # If end_date is not specified, return an error
    if end_date is None:
        return func.HttpResponse(
            f"Invalid request, end_date not found",
            status_code=400
        )
    # Convert trade_data to a pandas dataframe
    trade_data = req.get_json().get('trade_data')
    trade_dataframe = pandas.DataFrame(json.loads(trade_data))
    # Confirm that the timestamp column is in the dataframe
    if 'entry_time' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, entry_time not found",
            status_code=400
        )
    if 'exit_time' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, exit_time not found",
            status_code=400
        )
    # Check for entry_price and exit_price
    if 'entry_price' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, entry_price not found",
            status_code=400
        )
    if 'exit_price' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, exit_price not found",
            status_code=400
        )
    # Make sure exit_time is in datetime format
    trade_dataframe['exit_time'] = pandas.to_datetime(trade_dataframe['exit_time'], unit='ms')
    # Make sure entry_time is in datetime format
    trade_dataframe['entry_time'] = pandas.to_datetime(trade_dataframe['entry_time'], unit='ms')
    # Make sure the start_date is in datetime format
    start_date = pandas.to_datetime(start_date)
    # Make sure the end_date is in datetime format
    end_date = pandas.to_datetime(end_date)
    # Sort by timestamp
    trade_dataframe = trade_dataframe.sort_values(by='exit_time')
    # Calculate the Sharpe Ratio
    sharpe_data = analysis.calc_sharpe(
        trade_dataframe=trade_dataframe,
        start_date=start_date,
        end_date=end_date, 
        annual_risk_free_rate=annual_risk_free_rate
    )
    # Create the return payload
    payload = {
        'sharpe_data': sharpe_data,
        'annual_risk_free_rate': annual_risk_free_rate
    }
    # Convert the payload to JSON
    payload = json.dumps(payload)
    # Return the payload
    return func.HttpResponse(
        payload,
        status_code=200
    )


@app.route(route="calc-wins", methods=["GET", "POST"])
def wins(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Wins function processed a request.')
    # Check for trade_data
    trade_data = req.get_json().get('trade_data')
    if trade_data is None:
        return func.HttpResponse(
            f"Invalid request, trade_data not found",
            status_code=400
        )
    # Convert trade_data to a pandas dataframe
    trade_dataframe = pandas.DataFrame(json.loads(trade_data))
    # Confirm that the column trade_type is in the dataframe
    if 'order_type' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, trade_type not found",
            status_code=400
        )
    # Check that all the trade types are either BUY, BUY_STOP, SELL, or SELL_STOP
    trade_types = ['BUY', 'BUY_STOP', 'SELL', 'SELL_STOP']
    for trade_type in trade_dataframe['order_type']:
        if trade_type not in trade_types:
            return func.HttpResponse(
                f"Invalid trade_type in trade_data, {trade_type} not found",
                status_code=400
            )
    # Check for entry_price
    if 'entry_price' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, entry_price not found",
            status_code=400
        )
    # Check for exit_price
    if 'exit_price' not in trade_dataframe.columns:
        return func.HttpResponse(
            f"Invalid columns in trade_data, exit_price not found",
            status_code=400
        )
    # Send to calc_wins
    trade_dataframe = analysis.calc_wins(trade_dataframe)
    # Calculate the win rate
    win_rate = trade_dataframe['win'].sum() / len(trade_dataframe)
    # Round win_rate to 2 decimals
    win_rate = round(win_rate, 2)
    # Convert to string
    win_rate = str(win_rate)
    # Calculate number of wins
    wins = trade_dataframe['win'].sum()
    # Calculate number of losses
    losses = len(trade_dataframe) - wins
    # Convert losses to a string
    losses = str(losses)
    # Convert losses to a string
    wins = str(wins)
    # Create the return payload
    payload = {
        'win_rate': win_rate,
        'wins': wins,
        'losses': losses
    }
    # Convert the payload to JSON
    payload = json.dumps(payload)
    # Return the payload
    return func.HttpResponse(
        payload,
        status_code=200
    )
