from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Dict, Any


@dataclass
class StockAnalysisContext:

    symbol: str

    technical: dict = field(default_factory=dict)

    news: dict = field(default_factory=dict)

    fundamental: dict = field(default_factory=dict)

    summary: str = ""
    
    