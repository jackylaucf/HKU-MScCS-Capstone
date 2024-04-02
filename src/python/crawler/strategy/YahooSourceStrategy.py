import requests

from crawler import http_utils
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice
from functools import partial


class YahooSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Yahoo Finance'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        daily_prices = []
        if self.ticker_formatter:
            ticker = self.ticker_formatter(ticker)
        url = ('https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=946944000&period2=1711843200&'
               'interval=1d&events=history&includeAdjustedClose=true').format(ticker=ticker)
        try:
            response = http_utils.get(url)
            raw_data = response.text.split('\n')
            data_header, data_contents = list(map(lambda s: s.title(), raw_data[0].split(','))), raw_data[1:]
            for row in data_contents:
                data_values = row.split(',')
                daily_prices.append(
                    DailyPrice(
                        date=data_values[data_header.index('Date')],
                        open=data_values[data_header.index('Open')],
                        high=data_values[data_header.index('High')],
                        low=data_values[data_header.index('Low')],
                        close=data_values[data_header.index('Close')],
                        adj_close=data_values[data_header.index('Adj Close')],
                        volume=data_values[data_header.index('Volume')]))
        except (requests.HTTPError, ValueError) as ex:
            print(f'Caught error when fetching daily price of {ticker} - [{ex}]')
        return ticker, daily_prices

    def get_intraday_price(self, tickers: [str]) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        raise NotImplementedError()

    @staticmethod
    def get_ticker_formatter(prefix: str = '', suffix: str = '', zfill: int = 0):
        def ticker_format(ticker: str, prefix_inner: str, suffix_inner: str, zfill_inner: int):
            return f'{prefix_inner}{ticker.zfill(zfill_inner)}{suffix_inner}'
        return partial(ticker_format, prefix_inner=prefix, suffix_inner=suffix, zfill_inner=zfill)
