from app.tools.fundamental_tool import fetch_fundamental_data


def analyze_fundamentals(symbol: str):

    data = fetch_fundamental_data(symbol)

    pe = data["pe_ratio"]
    growth = data["revenue_growth"]
    margin = data["profit_margin"]
    debt = data["debt_to_equity"]

    valuation = "unknown"

    if pe:
        if pe < 15:
            valuation = "undervalued"
        elif pe < 30:
            valuation = "fairly valued"
        else:
            valuation = "overvalued"

    growth_signal = "unknown"

    if growth:
        if growth > 0.15:
            growth_signal = "strong growth"
        elif growth > 0:
            growth_signal = "moderate growth"
        else:
            growth_signal = "declining growth"

    return {
        "valuation": valuation,
        "growth": growth_signal,
        "profit_margin": margin,
        "debt_to_equity": debt
    }