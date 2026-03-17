import yfinance as yf
from dotenv import load_dotenv
import os
from groq import Groq

from app.config import llm_model

load_dotenv()


llm = client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_stock_name(stock):
    
    system_prompt = """
    You are a financial ticker mapping assistant. 
    Return ONLY the Yahoo Finance ticker symbol.
    - Indian NSE stocks: Append .NS (e.g., RELIANCE.NS)
    - US stocks: Primary ticker (e.g., AAPL)
    - Priority: Indian NSE listing.
    - Format: ONLY the ticker. No prose, no bolding.
    """
    response = client.chat.completions.create(
        # model="llama-3.1-8b-instant",
        model = llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": stock} 
        ],
        temperature=0 
    )
    return(response.choices[0].message.content.strip())


def fetch_price_history(symbol: str):

    symbol = get_stock_name(symbol) # edited now
    
    if not symbol.endswith(".NS"):
        symbol = symbol + ".NS"
    ticker = yf.Ticker(symbol)

    df = ticker.history(period="6mo")
    
    return df

def fetch_latest_price(symbol: str):

    symbol = get_stock_name(symbol) #edited now
    
    ticker = yf.Ticker(symbol)

    price = ticker.history(period="1d")["Close"].iloc[-1]

    return float(price)