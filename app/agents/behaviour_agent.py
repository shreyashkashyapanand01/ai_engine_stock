import logging
from dotenv import load_dotenv
import os
from groq import Groq
from datetime import datetime
import uuid
from app.config import llm_model

load_dotenv()

logger = logging.getLogger(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_behaviour(metrics, mistakes):
    logger.info("behaviour_agent: Started generating AI behaviour analysis")

    try:
        # -------------------------
        # Risk Score (deterministic)
        # -------------------------
        risk_score = min(len(mistakes) * 20, 100)

        # -------------------------
        # Trader Type (rule-based)
        # -------------------------
        if "revenge_trading" in mistakes:
            trader_type = "emotional"
        elif "inconsistent_position_size" in mistakes:
            trader_type = "aggressive"
        else:
            trader_type = "disciplined"

        # -------------------------
        # Prepare LLM Prompt
        # -------------------------
        prompt = f"""
You are an AI trading psychologist.

Analyze the trader's behavior based on the following metrics:

Metrics:
- Win Rate: {metrics["winRate"]}
- Avg Win Hold Time: {metrics["avgWinHoldMinutes"]} minutes
- Avg Loss Hold Time: {metrics["avgLossHoldMinutes"]} minutes
- Risk Reward Ratio: {metrics["avgRiskReward"]}
- Max Drawdown: {metrics["maxDrawdown"]}
- Loss Streak Frequency: {metrics["lossStreakFrequency"]}
- Position Size Variance: {metrics["positionSizeVariance"]}

Detected behavioral mistakes:
{", ".join(mistakes) if mistakes else "None"}

Your task:
1. Write a 2-line psychological summary of the trader.
2. Provide 3 concise actionable suggestions.

Rules:
- Do NOT give buy/sell signals
- Keep it concise
- Be educational and slightly critical (like a coach)

Output format STRICTLY:
Summary: <text>
Suggestions:
- <point 1>
- <point 2>
- <point 3>
"""

        response = client.chat.completions.create(
            model=llm_model,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content.strip()

        # -------------------------
        # Parse LLM Output
        # -------------------------
        summary = ""
        suggestions = []

        lines = content.split("\n")

        for line in lines:
            if line.lower().startswith("summary"):
                summary = line.replace("Summary:", "").strip()
            elif line.strip().startswith("-"):
                suggestions.append(line.replace("-", "").strip())

        logger.info("behaviour_agent: Successfully finished AI behaviour analysis")

    except Exception as e:
        logger.error(f"Error in behaviour_agent.py at generate_behaviour: AI generation failed - {str(e)}")

        # fallback (VERY IMPORTANT)
        # (Preserving your specific fallback values)
        risk_score = 50 if 'risk_score' not in locals() else risk_score
        trader_type = "unknown" if 'trader_type' not in locals() else trader_type
        summary = "Trading behaviour analysis is currently unavailable due to AI error."
        suggestions = [
            "Maintain discipline in trade execution",
            "Follow predefined risk management rules",
            "Avoid emotional decision making"
        ]

    return {
        "analysisId": str(uuid.uuid4())[:8],
        "generatedAt": datetime.utcnow().isoformat(),
        "riskScore": risk_score,
        "traderType": trader_type,
        "summary": summary,
        "suggestions": suggestions
    }