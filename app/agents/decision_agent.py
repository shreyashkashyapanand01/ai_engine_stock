from dotenv import load_dotenv
import os
from groq import Groq
from app.config import llm_model
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_decision(data: dict):

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

    response = client.chat.completions.create(
        #model="llama-3.1-8b-instant",
        model = llm_model,
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response.choices[0].message.content

    return {"summary": summary}