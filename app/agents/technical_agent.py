import logging
from app.tools.market_data_tool import fetch_price_history
from app.tools.indicator_tool import (
    calculate_trend,
    calculate_momentum,
    calculate_rsi,
    classify_rsi,
    calculate_volatility
)

logger = logging.getLogger(__name__)

def analyze(symbol: str):
    logger.info(f"technical_agent: Started analyzing market indicators for {symbol}")

    try:
        df = fetch_price_history(symbol)
    except Exception:
        logger.error(f"Error in technical_agent.py at analyze: Failed to fetch price history for {symbol}")
        return {"error": "Failed to retrieve market data"}

    if df.empty:
        logger.error(f"Error in technical_agent.py at analyze: Market data for {symbol} is empty")
        return {
            "error": "No market data found for this symbol"
        }

    try:
        trend = calculate_trend(df)
        momentum = calculate_momentum(df)

        rsi_value = calculate_rsi(df)
        rsi_state = classify_rsi(rsi_value)

        volatility = calculate_volatility(df)

        logger.info(f"technical_agent: Successfully finished technical analysis for {symbol}")

        return {
            "trend": trend,
            "momentum": momentum,
            "rsi": rsi_state,
            "volatility": volatility
        }
    except Exception:
        logger.error(f"Error in technical_agent.py at analyze: Calculation error while processing indicators for {symbol}")
        return {"error": "Technical calculation failure"}