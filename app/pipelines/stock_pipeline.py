import logging
from app.schemas.stock_schema import StockAnalysisContext
from app.agents.technical_agent import analyze as technical_analyze
from app.agents.news_agent import analyze_news
from app.agents.fundamental_agent import analyze_fundamentals
from app.agents.decision_agent import generate_decision

logger = logging.getLogger(__name__)

def run_stock_pipeline(symbol: str):
    logger.info(f"stock_pipeline: Started analyzing {symbol}")
    
    context = StockAnalysisContext(symbol=symbol)

    context.technical = technical_analyze(symbol)

    if "error" in context.technical:
        logger.error(f"Error in stock_pipeline.py at run_stock_pipeline: Stopped for {symbol} due to a technical analysis error")
        return context.technical

    context.news = analyze_news(symbol)

    context.fundamental = analyze_fundamentals(symbol)

    try:
        decision = generate_decision({
            "technical": context.technical,
            "news": context.news,
            "fundamental": context.fundamental
        })

        context.summary = decision["summary"]
        logger.info(f"stock_pipeline: Successfully finished analysis for {symbol}")
        
    except Exception:
        logger.error(f"Error in stock_pipeline.py at run_stock_pipeline: Failed to complete the analysis for {symbol}")
        return {"error": "Decision generation failed"}

    return context.__dict__