import logging
from app.schemas.portfolio_schema import PortfolioAnalysisContext
from app.analysis.portfolio_metrics_calculator import calculate_portfolio_metrics
from app.analysis.diversification_analyzer import analyze_diversification
from app.analysis.stress_test_engine import run_stress_test
from app.agents.portfolio_agent import generate_portfolio_decision
from app.tools.market_data_adapter import get_market_data
from app.analysis.sentiment_analyzer import get_news_sentiment

logger = logging.getLogger(__name__)


def run_portfolio_pipeline(holdings):
    logger.info("portfolio_pipeline: Started portfolio analysis")

    context = PortfolioAnalysisContext(holdings)

    try:
        logger.info("portfolio_pipeline: Calculating portfolio metrics")
        context.metrics = calculate_portfolio_metrics(holdings, get_market_data)

        logger.info("portfolio_pipeline: Analyzing diversification")
        context.diversification = analyze_diversification(holdings)

        logger.info("portfolio_pipeline: Running stress test")
        context.stressTest = run_stress_test(context.metrics)

        logger.info("portfolio_pipeline: Fetching sentiment")
        for h in holdings:
            #context.sentiment[h.symbol] = get_news_sentiment(h.symbol)
            sentiment_data = get_news_sentiment(h.symbol)
            context.sentiment[h.symbol]={
                    "sentiment": sentiment_data["sentiment"],
                    "confidence": sentiment_data["confidence"]
            }

        logger.info("portfolio_pipeline: Generating AI decision")
        decision = generate_portfolio_decision(context)

        context.summary = decision["summary"]
        context.actions = decision["actions"]
        context.portfolioHealthScore = decision["portfolioHealthScore"]
        context.riskLevel = decision["riskLevel"]

        result = {
            "analysisId": decision["analysisId"],
            "generatedAt": decision["generatedAt"],
            "portfolioHealthScore": context.portfolioHealthScore,
            "riskLevel": context.riskLevel,
            "metrics": context.metrics,
            "diversification": context.diversification,
            "stressTest": context.stressTest,
            "sentiment": context.sentiment,
            "summary": context.summary,
            "actions": context.actions
        }

        logger.info("portfolio_pipeline: Successfully completed portfolio analysis")
        return result

    except Exception as e:
        logger.error(f"Error in portfolio_pipeline: {str(e)}")
        return {"error": "Portfolio analysis failed"}