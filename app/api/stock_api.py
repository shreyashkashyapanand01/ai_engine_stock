from fastapi import APIRouter

from app.pipelines.stock_pipeline import run_stock_pipeline

router = APIRouter()


@router.get("/analyze-stock/{symbol}")
def analyze_stock(symbol: str):

    result = run_stock_pipeline(symbol)

    return result