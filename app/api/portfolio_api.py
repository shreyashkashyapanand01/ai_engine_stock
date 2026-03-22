import logging
from fastapi import APIRouter
from app.schemas.portfolio_schema import PortfolioAnalysisRequest
from app.pipelines.portfolio_pipeline import run_portfolio_pipeline

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/portfolio-analyze")
def analyze_portfolio(request: PortfolioAnalysisRequest):
    logger.info("portfolio_api: Received portfolio analysis request")

    try:
        # Log the number of holdings for better traceability
        logger.info(f"portfolio_api: Processing portfolio with {len(request.holdings)} holdings")
        
        result = run_portfolio_pipeline(request.holdings)
        
        logger.info("portfolio_api: Successfully completed portfolio analysis request")
        return result

    except Exception as e:
        logger.error(f"Error in portfolio_api.py at analyze_portfolio: Portfolio analysis failed - {str(e)}")
        return {"error": "Portfolio analysis failed"}