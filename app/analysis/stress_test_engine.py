import logging

logger = logging.getLogger(__name__)


def run_stress_test(metrics):
    logger.info("stress_test_engine: Started running portfolio stress test")

    try:
        total_value = metrics.get("totalValue", 0)

        if total_value == 0:
            logger.warning("stress_test_engine: Total value is 0, stress test results will be neutral")
            return {
                "marketCrashImpact": "0%",
                "interestRateImpact": "0%"
            }

        market_crash = total_value * 0.85
        interest_rate = total_value * 0.95

        market_impact = round(((market_crash - total_value)/total_value)*100, 2)
        interest_impact = round(((interest_rate - total_value)/total_value)*100, 2)

        logger.info(f"stress_test_engine: Successfully finished stress test (Market Impact: {market_impact}%)")

        return {
            "marketCrashImpact": f"{market_impact}%",
            "interestRateImpact": f"{interest_impact}%"
        }

    except Exception as e:
        logger.error(f"Error in stress_test_engine.py at run_stress_test: Stress test failed - {str(e)}")
        return {
            "marketCrashImpact": "Calculation Error",
            "interestRateImpact": "Calculation Error"
        }