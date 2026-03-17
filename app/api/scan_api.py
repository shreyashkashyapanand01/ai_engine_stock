from fastapi import APIRouter
from app.schemas.scan_schema import ScanResponse
from app.pipelines.scan_pipeline import run_market_scan

router = APIRouter()


@router.get("/scan-market", response_model=ScanResponse)
def scan_market():

    results = run_market_scan()

    return {
        "opportunities": results
    }