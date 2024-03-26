from dataclasses import dataclass


@dataclass
class OHLCVol:
    date: str
    open: float
    high: float
    close: float
    adj_close: float
    volume: float
