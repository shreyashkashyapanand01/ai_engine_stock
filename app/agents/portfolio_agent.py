import uuid
from datetime import datetime
import logging
import os
from groq import Groq
from app.config import llm_model

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_portfolio_decision(context):
    logger.info("portfolio_agent: Started generating AI portfolio decision")
    try:
        prompt = f"""
        You are an expert AI Portfolio Advisor.

        Analyze the portfolio using the following data:

        Metrics:
        {context.metrics}

        Diversification:
        {context.diversification}

        Stress Test:
        {context.stressTest}

        Sentiment:
        {context.sentiment}

        Tasks:
        1. Give a portfolio health score (0-100)
        2. Classify risk level (Low, Moderate, High)
        3. Write a professional summary (2-3 lines)
        4. Provide 3-5 actionable suggestions

        Return ONLY JSON:
        {{
            "portfolioHealthScore": number,
            "riskLevel": "Low | Moderate | High",
            "summary": "...",
            "actions": ["...", "..."]
        }}
        """

        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": "You are a professional financial advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        import json
        #parsed = json.loads(content)
        import re
        json_str = re.search(r"\{.*\}", content, re.DOTALL).group()
        parsed = json.loads(json_str)

        logger.info("portfolio_agent: Successfully finished AI portfolio decision generation")
        return {
            "analysisId": str(uuid.uuid4()),
            "generatedAt": datetime.utcnow().isoformat(),
            "portfolioHealthScore": int(parsed.get("portfolioHealthScore", 50)),
            "riskLevel": parsed.get("riskLevel", "Moderate"),
            "summary": parsed.get("summary", ""),
            "actions": parsed.get("actions", [])
        }

    except Exception as e:
        logger.error(f"portfolio_agent: Failed - {str(e)}")

        return {
            "analysisId": str(uuid.uuid4()),
            "generatedAt": datetime.utcnow().isoformat(),
            "portfolioHealthScore": 50,
            "riskLevel": "Moderate",
            "summary": "Unable to generate AI insights.",
            "actions": ["Review portfolio manually"]
        }