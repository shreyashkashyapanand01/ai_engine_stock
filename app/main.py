from fastapi import FastAPI

from app.api.stock_api import router as stock_router


app = FastAPI(
    title="AI Stock Intelligence Engine"
)

app.include_router(stock_router)