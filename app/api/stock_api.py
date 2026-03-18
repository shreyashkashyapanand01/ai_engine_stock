import logging
from fastapi import APIRouter
from app.schemas.stock_schema import StockResponse
from app.pipelines.stock_pipeline import run_stock_pipeline

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/analyze-stock/{symbol}", response_model=StockResponse)
def analyze_stock(symbol: str):
    logger.info(f"stock_api: Received request to analyze stock {symbol}")

    try:
        result = run_stock_pipeline(symbol)
        
        if "error" in result:
            logger.error(f"Error in stock_api.py at analyze_stock: Pipeline returned error for {symbol}")
        else:
            logger.info(f"stock_api: Successfully completed analysis request for {symbol}")
            
        return result

    except Exception:
        logger.error(f"Error in stock_api.py at analyze_stock: Unexpected crash during request for {symbol}")
        return {"symbol": symbol, "error": "Internal server error during analysis"}