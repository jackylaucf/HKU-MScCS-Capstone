import requests

from crawler.strategy.SourceStrategy import SourceStrategy
from functools import partial


class YahooSourceStrategy(SourceStrategy):

    def get_price(self, tickers: [str]):
        if self.ticker_formatter:
            pass

    def get_constituents(self):
        raise NotImplementedError()

    @staticmethod
    def get_ticker_formatter(prefix: str = '', suffix: str = '', zfill: int = 0):
        def ticker_format(ticker: str, prefix_inner: str, suffix_inner: str, zfill_inner: int):
            return f'{prefix_inner}{ticker.zfill(zfill_inner)}{suffix_inner}'
        return partial(ticker_format, prefix_inner=prefix, suffix_inner=suffix, zfill_inner=zfill)
