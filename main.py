import pandas as pd


# Implementation of TradingView Relative Moving Average
# https://www.tradingcode.net/tradingview/relative-moving-average/
def rma(series, length):
    alpha = 1 / length
    rma = [series[:length].mean()]  # Initial RMA value is the SMA of the first `length` values
    for price in series[length:]:
        rma.append(alpha * price + (1 - alpha) * rma[-1])
    return pd.Series(rma, index=series.index[length-1:])


# Implementation of TradingView RSI Indicator
# https://www.tradingview.com/support/solutions/43000502338-relative-strength-index-rsi/
def rsi(candleCloses, length):
    delta = candleCloses.diff()

    poaitiv_delta = delta.where(delta >= 0,0)
    negative_delta = (-1)*delta.where(delta < 0,0)

    average_gain = rma(poaitiv_delta,length)
    average_loss = rma(negative_delta,length)

    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

filename = "COINBASE_BTCUSD.csv"
data = pd.read_csv(filename)
candleCloses = data['close']
data['Calculated_RSI'] = rsi(candleCloses,14)


print(data[['close', 'RSI', 'Calculated_RSI']].head(2000))