import logging
from groq import Groq
from dotenv import load_dotenv
import os
from app.tools.news_tool import fetch_news
from app.config import llm_model

load_dotenv()

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_news(symbol: str):
    logger.info(f"news_agent: Started analyzing news for {symbol}")

    try:
        headlines = fetch_news(symbol)
    except Exception:
        logger.error(f"Error in news_agent.py at analyze_news: Failed to fetch news headlines for {symbol}")
        return {
            "headlines": [],
            "analysis": "Error occurred while fetching news."
        }

    if not headlines:
        logger.info(f"news_agent: No news found for {symbol}")
        return {
            "headlines": [],
            "analysis": "No recent news available for this stock."
        }

    news_text = "\n".join(headlines)

    prompt = f"""
You are a financial news analyst.

Here are recent news headlines about {symbol}:

{news_text}

Analyze the overall sentiment of the news.

Return:
1. Sentiment (positive / negative / neutral)
2. Short explanation in 1-2 sentences.
"""

    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content
        logger.info(f"news_agent: Successfully finished news analysis for {symbol}")

        return {
            "headlines": headlines,
            "analysis": result
        }
    except Exception:
        logger.error(f"Error in news_agent.py at analyze_news: AI failed to analyze news sentiment for {symbol}")
        return {
            "headlines": headlines,
            "analysis": "Sentiment analysis currently unavailable due to an AI error."
        }