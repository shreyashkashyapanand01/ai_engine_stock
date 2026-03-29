import logging
import os
from groq import Groq
from app.tools.news_tool import fetch_news
from app.config import llm_model

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
import json
import re


def safe_parse_llm_json(content: str):
    logger.info("sentiment_analyzer: Attempting to parse LLM JSON response")
    try:
        # Step 1: extract JSON block
        match = re.search(r"\{.*?\}", content, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        json_str = match.group()

        # Step 2: fix common issues
        json_str = json_str.replace("\n", " ")
        json_str = re.sub(r",\s*}", "}", json_str)  # remove trailing commas

        parsed = json.loads(json_str)

        return parsed

    except Exception as e:
        logger.error(f"JSON parsing failed: {str(e)} | Raw: {content}")
        return None

def get_news_sentiment(symbol: str):
    logger.info(f"sentiment_analyzer: Analyzing sentiment for {symbol}")

    try:
        headlines = fetch_news(symbol)

        if not headlines:
            logger.warning(f"sentiment_analyzer: no new news found for {symbol}, so returnig default values")
            return {
                "sentiment": "Neutral",
                "confidence": 0.5,
                "headlines": []
            }
            
        logger.info(f"sentiment_analyzer: news found for {symbol}, doing news sentiment analysys")

        prompt = f"""
        Analyze the sentiment of the following news headlines for stock {symbol}.

        Headlines:
        {headlines}

        Strictly Return ONLY in JSON format:
        Strictly Return ONLY valid JSON.
        Strictly Do NOT include any text before or after JSON.
        Strictly Do NOT explain anything.
        {{
            "sentiment": "Bullish | Bearish | Neutral",
            "confidence": 0 to 1
        }}
        """

        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": "You are a financial sentiment analysis AI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()  
             
        # import json
        # #parsed = json.loads(content)
        # import re
        # json_str = re.search(r"\{.*\}", content, re.DOTALL).group()
        # parsed = json.loads(json_str)
        
        parsed = safe_parse_llm_json(content)
        
        if not parsed:
            raise ValueError("Invalid LLM JSON response")
        
        logger.info(f"sentiment_analyzer: Successfully finished sentiment analysis for {symbol}")

        return {
            "sentiment": parsed.get("sentiment", "Neutral"),
            "confidence": round(float(parsed.get("confidence", 0.5)), 2),
            "headlines": headlines
        }

    except Exception as e:
        logger.error(f"sentiment_analyzer: Failed for {symbol} - {str(e)}")
        return {
            "sentiment": "Neutral",
            "confidence": 0.5,
            "headlines": []
        }