from abc import ABC, abstractmethod
from model.market_data import DailyPrice, IntradayPrice
from typing import Callable


class SourceStrategy(ABC):
    def __init__(self, index_ticker: str, ticker_formatter: Callable[[str], str] = None):
        self.index_ticker = index_ticker
        self.ticker_formatter = ticker_formatter

    @abstractmethod
    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        pass

    @abstractmethod
    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        pass

    @abstractmethod
    def get_constituents(self) -> [str]:
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        pass
