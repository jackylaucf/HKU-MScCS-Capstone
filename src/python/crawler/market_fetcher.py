from crawler.strategy import SourceStrategy
from typing import NamedTuple


class FetcherStrategies(NamedTuple):
    index_price: SourceStrategy
    constituents: SourceStrategy
    constituents_price: SourceStrategy


class MarketFetcher:

    def __init__(self, index: str, strategies: FetcherStrategies):
        self.index = index
        self.strategies = strategies

    def get_constituents(self) -> [str]:
        return

    def get_index_ohlc(self) -> [dict]:
        pass

    def get_constituents_ohlc(self) -> [dict]:
        constituents = self.get_constituents()

    def export(self):
        pass

    def fetch(self):
        pass
