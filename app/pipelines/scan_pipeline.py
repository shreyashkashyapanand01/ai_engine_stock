import logging
from app.data.universe_providers.gainer_provider import fetch_top_sector_performers
from app.pipelines.stock_pipeline import run_stock_pipeline
from app.scoring.opportunity_scorer import score_opportunity

logger = logging.getLogger(__name__)

def run_market_scan():
    logger.info("scan_pipeline: Started market scan for top performers")

    try:
        top_movers = fetch_top_sector_performers()
    except Exception:
        logger.error("Error in scan_pipeline.py at run_market_scan: Failed to fetch top movers from provider")
        return []

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
            logger.error(f"Error in scan_pipeline.py at run_market_scan: Failed to process analysis for {symbol}")
            continue

    opportunities.sort(key=lambda x: x["score"], reverse=True)

    logger.info(f"scan_pipeline: Successfully finished market scan with {len(opportunities)} opportunities found")
    return opportunities