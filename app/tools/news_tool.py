import logging
import os
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(symbol: str):
    logger.info(f"news_tool: Fetching latest news headlines for {symbol}")

    query = f'{symbol} OR "{symbol} stock" OR "{symbol} company"'

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            logger.error(f"Error in news_tool.py at fetch_news: NewsAPI returned {response.status_code} - {data.get('message', 'Unknown Error')}")
            return []

        articles = data.get("articles", [])

        headlines = []

        for article in articles:
            headlines.append(article["title"])

        logger.info(f"news_tool: Successfully retrieved {len(headlines)} headlines for {symbol}")
        return headlines

    except Exception as e:
        logger.error(f"Error in news_tool.py at fetch_news: Request failed for {symbol} - {str(e)}")
        return []