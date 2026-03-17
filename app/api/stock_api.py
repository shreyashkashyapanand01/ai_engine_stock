from fastapi import APIRouter
from app.schemas.stock_schema import StockResponse
from app.pipelines.stock_pipeline import run_stock_pipeline

router = APIRouter()


@router.get("/analyze-stock/{symbol}", response_model=StockResponse)
def analyze_stock(symbol: str):

    result = run_stock_pipeline(symbol)

    return result