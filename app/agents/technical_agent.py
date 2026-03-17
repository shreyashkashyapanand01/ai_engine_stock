from app.tools.market_data_tool import fetch_price_history
from app.tools.indicator_tool import (
    calculate_trend,
    calculate_momentum,
    calculate_rsi,
    classify_rsi,
    calculate_volatility
)


def analyze(symbol: str):

    df = fetch_price_history(symbol)

    if df.empty:
        return {
            "error": "No market data found for this symbol"
        }

    trend = calculate_trend(df)
    momentum = calculate_momentum(df)

    rsi_value = calculate_rsi(df)
    rsi_state = classify_rsi(rsi_value)

    volatility = calculate_volatility(df)

    return {
        "trend": trend,
        "momentum": momentum,
        "rsi": rsi_state,
        "volatility": volatility
    }