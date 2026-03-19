import logging
from fastapi import APIRouter
from app.schemas.trade_schema import TradeAnalysisRequest
from app.pipelines.trade_pipeline import run_trade_pipeline

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/analyze-trades")
def analyze_trades(request: TradeAnalysisRequest):
    logger.info("trade_api: Received trade analysis request")

    try:
        # Convert Pydantic models to dictionaries
        trades = [t.dict() for t in request.trades]
        
        logger.info(f"trade_api: Processing {len(trades)} trades through pipeline")

        result = run_trade_pipeline(trades)

        if "error" in result:
            logger.error(f"Error in trade_api.py at analyze_trades: Pipeline returned error - {result.get('error')}")
        else:
            logger.info("trade_api: Successfully completed trade analysis request")

        return result

    except Exception as e:
        logger.error(f"Error in trade_api.py at analyze_trades: Unexpected error during request - {str(e)}")
        return {"error": "Internal server error"}