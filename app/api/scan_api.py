import logging
from fastapi import APIRouter
from app.schemas.scan_schema import ScanResponse
from app.pipelines.scan_pipeline import run_market_scan

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/scan-market", response_model=ScanResponse)
def scan_market():
    logger.info("scan_api: Received request to scan the market")

    try:
        results = run_market_scan()
        logger.info(f"scan_api: Market scan completed successfully with {len(results)} items")
        
        return {
            "opportunities": results
        }
    except Exception:
        logger.error("Error in scan_api.py at scan_market: Failed to complete market scan request")
        return {"opportunities": [], "error": "Internal server error during market scan"}