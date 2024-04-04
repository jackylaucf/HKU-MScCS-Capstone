from dataclasses import dataclass
from datetime import datetime


@dataclass(kw_only=True)
class OHLCVol:
    open: str
    high: str
    low: str
    close: str
    volume: str = None


@dataclass(kw_only=True)
class DailyPrice(OHLCVol):
    date: str
    adj_close: str = None

    @staticmethod
    def build(data_dict, date_format: str):
        data_dict['date'] = datetime.strptime(data_dict['date'], date_format).date().isoformat()
        return DailyPrice(**data_dict)


@dataclass(kw_only=True)
class IntradayPrice(OHLCVol):
    timestamp: str
