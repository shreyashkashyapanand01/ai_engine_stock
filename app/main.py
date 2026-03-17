from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.stock_api import router as stock_router
from app.api.scan_api import router as scan_router


def create_app() -> FastAPI:

    app = FastAPI(
        title="AI Trading Coach Engine",
        description="AI-powered stock analysis and market scanner",
        version="1.0.0"
    )

    #  CORS (important for frontend later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # later restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #  Register routers
    app.include_router(stock_router, prefix="")
    app.include_router(scan_router, prefix="")

    return app


app = create_app()