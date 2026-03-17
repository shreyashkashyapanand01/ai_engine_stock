from app.data.universe_providers.gainer_provider import fetch_top_sector_performers
from app.pipelines.stock_pipeline import run_stock_pipeline
from app.scoring.opportunity_scorer import score_opportunity


def run_market_scan():

    top_movers = fetch_top_sector_performers()

    opportunities = []

    for stock in top_movers:

        symbol = stock["symbol"]

        try:
            result = run_stock_pipeline(symbol)

            if "error" in result:
                continue

            # AI score
            ai_score = score_opportunity(result)

            # momentum boost
            momentum_score = stock["perChange"]

            final_score = ai_score + (momentum_score / 10)

            opportunities.append({
                "symbol": symbol,
                "sector": stock["sector"],
                "score": round(final_score, 2),
                "momentum": round(momentum_score, 2),
                "summary": result["summary"]
            })

        except Exception:
            continue

    opportunities.sort(key=lambda x: x["score"], reverse=True)

    return opportunities