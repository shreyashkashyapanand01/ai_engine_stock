from pydantic import BaseModel
from typing import List


class Holding(BaseModel):
    symbol: str
    quantity: int
    buy_price: float


class PortfolioAnalysisRequest(BaseModel):
    holdings: List[Holding]


class PortfolioAnalysisResponse(BaseModel):
    analysisId: str
    generatedAt: str
    portfolioHealthScore: int
    riskLevel: str
    metrics: dict
    diversification: dict
    stressTest: dict
    sentiment: dict
    summary: str
    actions: List[str]


class PortfolioAnalysisContext:
    def __init__(self, holdings):
        self.holdings = holdings
        self.metrics = {}
        self.diversification = {}
        self.stressTest = {}
        self.sentiment = {}
        self.summary = ""
        self.actions = []
        self.portfolioHealthScore = 0
        self.riskLevel = ""