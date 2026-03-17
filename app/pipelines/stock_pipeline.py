from app.schemas.stock_schema import StockAnalysisContext
from app.agents.technical_agent import analyze as technical_analyze
from app.agents.news_agent import analyze_news
from app.agents.fundamental_agent import analyze_fundamentals
from app.agents.decision_agent import generate_decision


def run_stock_pipeline(symbol: str):

    context = StockAnalysisContext(symbol=symbol)

    context.technical = technical_analyze(symbol)

    if "error" in context.technical:
        return context.technical

    context.news = analyze_news(symbol)

    context.fundamental = analyze_fundamentals(symbol)

    decision = generate_decision({
        "technical": context.technical,
        "news": context.news,
        "fundamental": context.fundamental
    })

    context.summary = decision["summary"]

    return context.__dict__