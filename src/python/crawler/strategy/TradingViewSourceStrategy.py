from bs4 import BeautifulSoup
from crawler import http_utils
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice


class TradingViewSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Trading View'

    def get_daily_price(self, ticker: str) -> [DailyPrice]:
        raise NotImplementedError()

    def get_intraday_price(self, ticker: str):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        url = 'https://www.tradingview.com/symbols/{ticker}/components'.format(ticker=self.index_ticker)
        parsed_html = BeautifulSoup(http_utils.get(url).text, 'html.parser')
        constituents = []
        for element in parsed_html.findAll('a', {'class': 'tickerName-GrtoTeat'}):
            constituents.append(element.text)
        return constituents

