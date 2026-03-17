from groq import Groq
from dotenv import load_dotenv
import os
from app.tools.news_tool import fetch_news
from app.config import llm_model

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_news(symbol: str):

    headlines = fetch_news(symbol)

    if not headlines:
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

    response = client.chat.completions.create(
        #model="llama-3.1-8b-instant",
        model=llm_model,
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    return {
        "headlines": headlines,
        "analysis": result
    }