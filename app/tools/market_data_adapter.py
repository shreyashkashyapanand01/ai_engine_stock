import logging
from app.tools.market_data_tool import fetch_latest_price, fetch_price_history

logger = logging.getLogger(__name__)


def get_market_data(symbol: str):
    logger.info(f"market_data_adapter: Started getting structured market data for {symbol}")

    try:
        price = fetch_latest_price(symbol)
        history = fetch_price_history(symbol)

        if history is None or history.empty:
            logger.warning(f"market_data_adapter: No price history found for {symbol}")

        logger.info(f"market_data_adapter: Successfully finished fetching market data for {symbol}")
        return {
            "price": price,
            "history": history
        }

    except Exception as e:
        logger.error(f"Error in market_data_adapter.py at get_market_data: Failed for {symbol} - {str(e)}")
        return {
            "price": 0,
            "history": None
        }