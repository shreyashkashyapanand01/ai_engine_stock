import logging
from app.schemas.trade_schema import TradeAnalysisContext
from app.analysis.metrics_calculator import calculate_metrics
from app.analysis.pattern_detector import detect_patterns
from app.agents.behaviour_agent import generate_behaviour

logger = logging.getLogger(__name__)


def run_trade_pipeline(trades: list):
    logger.info("trade_pipeline: Started trade behaviour analysis")

    context = TradeAnalysisContext(trades=trades)

    try:
        # Step-by-step logging for visibility in the pipeline
        logger.info(f"trade_pipeline: Calculating metrics for {len(trades)} trades")
        context.metrics = calculate_metrics(trades)
        
        logger.info("trade_pipeline: Detecting behavioural patterns")
        context.mistakes = detect_patterns(context.metrics)

        logger.info("trade_pipeline: Requesting AI behaviour summary")
        decision = generate_behaviour(context.metrics, context.mistakes)

        context.summary = decision["summary"]
        context.suggestions = decision["suggestions"]
        context.riskScore = decision["riskScore"]
        context.traderType = decision["traderType"]

        result = {
            "analysisId": decision["analysisId"],
            "generatedAt": decision["generatedAt"],
            "riskScore": context.riskScore,
            "traderType": context.traderType,
            "mistakes": context.mistakes,
            "metrics": context.metrics,
            "summary": context.summary,
            "suggestions": context.suggestions
        }

        logger.info(f"trade_pipeline: Successfully completed analysis for {context.traderType} trader type")
        return result

    except Exception as e:
        logger.error(f"Error in trade_pipeline.py at run_trade_pipeline: Failed to process trade analysis - {str(e)}")
        return {"error": "Trade analysis failed"}