import pandas as pd


def calculate_trend(df):

    short_ma = df["Close"].rolling(window=20).mean()
    long_ma = df["Close"].rolling(window=50).mean()

    if short_ma.iloc[-1] > long_ma.iloc[-1]:
        return "bullish"
    else:
        return "bearish"


def calculate_momentum(df):

    momentum = df["Close"].pct_change().rolling(10).mean().iloc[-1]

    if momentum > 0.01:
        return "strong"
    elif momentum > 0:
        return "moderate"
    else:
        return "weak"


def calculate_rsi(df, window=14):

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]


def classify_rsi(rsi):

    if rsi > 70:
        return "overbought"
    elif rsi < 30:
        return "oversold"
    else:
        return "neutral"


def calculate_volatility(df):

    volatility = df["Close"].pct_change().std()

    if volatility < 0.01:
        return "low"
    elif volatility < 0.02:
        return "medium"
    else:
        return "high"