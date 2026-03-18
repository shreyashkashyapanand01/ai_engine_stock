import logging
from app.tools.fundamental_tool import fetch_fundamental_data

logger = logging.getLogger(__name__)

def analyze_fundamentals(symbol: str):
    logger.info(f"fundamental_agent: Started analyzing fundamental data for {symbol}")

    try:
        data = fetch_fundamental_data(symbol)
    except Exception:
        logger.error(f"Error in fundamental_agent.py at analyze_fundamentals: Failed to fetch data for {symbol}")
        return {
            "valuation": "unknown",
            "growth": "unknown",
            "profit_margin": None,
            "debt_to_equity": None
        }

    pe = data.get("pe_ratio")
    growth = data.get("revenue_growth")
    margin = data.get("profit_margin")
    debt = data.get("debt_to_equity")

    valuation = "unknown"
    if pe:
        if pe < 15:
            valuation = "undervalued"
        elif pe < 30:
            valuation = "fairly valued"
        else:
            valuation = "overvalued"

    growth_signal = "unknown"
    if growth:
        if growth > 0.15:
            growth_signal = "strong growth"
        elif growth > 0:
            growth_signal = "moderate growth"
        else:
            growth_signal = "declining growth"

    logger.info(f"fundamental_agent: Successfully finished fundamental analysis for {symbol}")

    return {
        "valuation": valuation,
        "growth": growth_signal,
        "profit_margin": margin,
        "debt_to_equity": debt
    }