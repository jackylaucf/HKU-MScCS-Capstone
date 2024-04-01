from dataclasses import dataclass


@dataclass
class OHLCVol:
    open: str
    high: str
    low: str
    close: str
    volume: str


@dataclass
class DailyPrice(OHLCVol):
    date: str
    adj_close: str


@dataclass
class IntradayPrice(OHLCVol):
    timestamp: str
