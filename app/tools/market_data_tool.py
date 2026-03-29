# import logging
# import yfinance as yf
# from dotenv import load_dotenv
# import os
# from groq import Groq

# from app.config import llm_model

# import requests


# load_dotenv()

# logger = logging.getLogger(__name__)
# llm = client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # Instantly map known historical mergers or common user typos
# KNOWN_TICKER_FIXES = {
#     "HDFC": "HDFCBANK.NS",
#     "FB": "META",
#     "TWITTER": "DJT"
# }

# def get_stock_name(stock: str) -> str:
#     clean_stock = stock.strip().upper()
    
#     # 1. Instantly catch the HDFC merger (Bypasses search entirely!)
#     if clean_stock in KNOWN_TICKER_FIXES:
#         return KNOWN_TICKER_FIXES[clean_stock]
    
#     # 2. For all other stocks, reliably query the active Yahoo database
#     url = f"https://query2.finance.yahoo.com/v1/finance/search?q={clean_stock}&quotesCount=5&newsCount=0"
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36'
#     }
    
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         quotes = response.json().get("quotes", [])

#         if not quotes:
#             return clean_stock 

#         # Scan the top results to find the exact Indian Exchange version (.NS / .BO)
#         for q in quotes:
#             exchange = q.get("exchange", "")
#             if exchange in ["NSI", "BSE"]:
#                 return q.get("symbol", "")
                
#         # Fallback: Just return the top result Yahoo found
#         return quotes[0].get("symbol", clean_stock)
        
#     except Exception as e:
#         logger.error(f"Failed to search Yahoo API for {stock}. Using original. Error: {e}")
#         return clean_stock


# def fetch_price_history(symbol: str):

#     logger.info(f"market_data_tool: Fetching price history for {symbol}")
#     try:
#         symbol = get_stock_name(symbol) # edited now
        
#         if not symbol.endswith(".NS"):
#             symbol = symbol + ".NS"
#         ticker = yf.Ticker(symbol)

#         df = ticker.history(period="6mo")
        
#         if df.empty:
#             logger.warning(f"market_data_tool: No history found for {symbol}")
            
#         return df
#     except Exception:
#         logger.error(f"Error in market_data_tool.py at fetch_price_history: Failed to download data for {symbol}")
#         import pandas as pd
#         return pd.DataFrame()

# def fetch_latest_price(symbol: str):

#     try:
#         symbol = get_stock_name(symbol) #edited now
        
#         ticker = yf.Ticker(symbol)

#         price_df = ticker.history(period="1d")
#         if price_df.empty:
#             raise ValueError("Empty price data")
            
#         price = price_df["Close"].iloc[-1]

#         return float(price)
#     except Exception:
#         logger.error(f"Error in market_data_tool.py at fetch_latest_price: Could not get latest price for {symbol}")
#         return 0.0

import logging
import yfinance as yf
from dotenv import load_dotenv
import os
from groq import Groq

from app.config import llm_model

load_dotenv()

logger = logging.getLogger(__name__)
llm = client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_stock_name(stock):
    
    system_prompt = """
    You are a financial ticker mapping assistant. 
    Return ONLY the Yahoo Finance ticker symbol.
    - Indian NSE stocks: Append .NS (e.g., RELIANCE.NS)
    - US stocks: Primary ticker (e.g., AAPL)
    - If the current stock name which is provided do not match with any other stock, return the
        best similar naming stock. For example if i give HDFC returb HDFCBANK ,etc
    - Priority: Indian NSE listing.
    - Format: ONLY the ticker. No prose, no bolding.
    """
    try:
        response = client.chat.completions.create(
            # model="llama-3.1-8b-instant",
            model = llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": stock} 
            ],
            temperature=0 
        )
        ticker = response.choices[0].message.content.strip()
        return ticker
    except Exception:
        logger.error(f"Error in market_data_tool.py at get_stock_name: Failed to map ticker for {stock}")
        return stock


def fetch_price_history(symbol: str):

    logger.info(f"market_data_tool: Fetching price history for {symbol}")
    try:
        symbol = get_stock_name(symbol) # edited now
        
        if not symbol.endswith(".NS"):
            symbol = symbol + ".NS"
        ticker = yf.Ticker(symbol)

        df = ticker.history(period="6mo")
        
        if df.empty:
            logger.warning(f"market_data_tool: No history found for {symbol}")
            
        return df
    except Exception:
        logger.error(f"Error in market_data_tool.py at fetch_price_history: Failed to download data for {symbol}")
        import pandas as pd
        return pd.DataFrame()

def fetch_latest_price(symbol: str):

    try:
        symbol = get_stock_name(symbol) #edited now
        
        ticker = yf.Ticker(symbol)

        price_df = ticker.history(period="1d")
        if price_df.empty:
            raise ValueError("Empty price data")
            
        price = price_df["Close"].iloc[-1]

        return float(price)
    except Exception:
        logger.error(f"Error in market_data_tool.py at fetch_latest_price: Could not get latest price for {symbol}")
        return 0.0