from abc import ABC, abstractmethod
from typing import Callable


class SourceStrategy(ABC):
    def __init__(self, index_ticker: str, ticker_formatter: Callable[[str], str] = None):
        self.index_ticker = index_ticker
        self.ticker_formatter = ticker_formatter

    @abstractmethod
    def get_price(self, tickers: [str]):
        pass

    @abstractmethod
    def get_constituents(self):
        pass
