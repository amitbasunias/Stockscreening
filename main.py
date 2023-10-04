import yfinance as yf
from yahoo_fin import stock_info as si
import numpy as np
import talib

# Get a list of NASDAQ stock symbols
stocks = si.tickers_nasdaq()

min_market_cap = 1e9
max_rsi = 45


# Create a function to filter stocks based on criteria
def filter_stocks(stock):
    try:
        # Fetch historical data for 1 year
        history = stock.history(period="1y", interval="1d")
        # Check market capitalization
        market_cap = stock.info['marketCap']
        if market_cap <= min_market_cap:
            return False

        # Calculate RSI
        close_prices = history['Close']
        rsi = talib.RSI(close_prices, timeperiod=30).iloc[-1]
        if rsi >= max_rsi:
            return False
        print("got max rsi")
        # Calculate MACD
        macd, signal, _ = talib.MACD(close_prices)

        # Check for MACD crossover (current MACD > current Signal and previous MACD < previous Signal)
        if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] < signal.iloc[-2]:
            print("bingoo")
            return True

        return False
    except Exception as e:
        pass

    return False


# Scan and filter NASDAQ stocks
filtered_stocks = []

for symbol in stocks:
    stock = yf.Ticker(symbol)
    if filter_stocks(stock):
        print(symbol)
        filtered_stocks.append(symbol)

print("Filtered stocks:", filtered_stocks)
