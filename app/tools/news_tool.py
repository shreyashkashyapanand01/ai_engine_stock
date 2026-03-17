import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news(symbol: str):

    query = f'{symbol} OR "{symbol} stock" OR "{symbol} company"'

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    if response.status_code != 200:
        print(f"Error from NewsAPI: {data.get('message', 'Unknown Error')}")
        return []

    articles = data.get("articles", [])

    headlines = []

    for article in articles:
        headlines.append(article["title"])

    return headlines