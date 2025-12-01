from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PriceBar:
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    value_traded: float | None = None
    n_trades: int | None = None
