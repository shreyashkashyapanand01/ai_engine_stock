import logging
from dotenv import load_dotenv
import os
from groq import Groq
from app.config import llm_model

load_dotenv()

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_decision(data: dict):
    logger.info("decision_agent: Started generating AI decision summary")

    technical = data["technical"]
    news = data["news"]

    trend = technical["trend"]
    momentum = technical["momentum"]
    rsi = technical["rsi"]
    volatility = technical["volatility"]

    news_analysis = news.get("analysis", "No news sentiment available.")

    fundamental = data["fundamental"]

    valuation = fundamental["valuation"]
    growth = fundamental["growth"]
    
    prompt = f"""
You are an AI trading mentor.

Technical signals:
Trend: {trend}
Momentum: {momentum}
RSI condition: {rsi}
Volatility: {volatility}

Fundamental signals:
Valuation: {valuation}
Growth outlook: {growth}

Recent news sentiment:
{news_analysis}

Explain the overall market condition in 2 short concise sentences .

Do NOT give buy/sell signals.
Do NOT write long paragraphs.
Focus on concise and educational reasoning.
"""

    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content
        logger.info("decision_agent: Successfully generated AI decision summary")
        
        return {"summary": summary}

    except Exception:
        logger.error("Error in decision_agent.py at generate_decision: Failed to get response from Groq AI")
        return {"summary": "Decision summary currently unavailable due to an AI processing error."}