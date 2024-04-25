import requests
import pandas as pd
import mplfinance as mpf
from datetime import datetime

def fetch_klines(symbol, interval, start_str, end_str):
    url = 'https://api.binance.com/api/v3/klines'
    start_ms = int(datetime.strptime(start_str, '%Y-%m-%d').timestamp() * 1000)
    end_ms = int(datetime.strptime(end_str, '%Y-%m-%d').timestamp() * 1000)
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_ms,
        'endTime': end_ms,
        'limit': 1000  # Binance has a limit of 1000 rows per call
    }

    data = []
    while True:
        response = requests.get(url, params=params)
        new_klines = response.json()
        if not new_klines or new_klines == data[-1:]:
            break
        data.extend(new_klines)
        params['startTime'] = new_klines[-1][0] + 1  # increment start time to fetch subsequent data

    return pd.DataFrame(data, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])

def plot_klines(df):
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df.set_index('Open time', inplace=True)
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = df[col].astype(float)
    
    mpf.plot(df[['Open', 'High', 'Low', 'Close', 'Volume']], type='candle', volume=True, style='charles',
             title='BTC Daily K-Line Chart (2020-01-01 to 2023-06-30)', ylabel='Price (USDT)')

# Example usage:
df_klines = fetch_klines('BTCUSDT', '1d', '2020-01-01', '2023-06-30')
plot_klines(df_klines)
 