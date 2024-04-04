from bs4 import BeautifulSoup
from crawler import http_utils
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice


class NikkeiJPSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Nikkei JP'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        raise NotImplementedError()

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        constituents = []
        url = ('https://indexes.nikkei.co.jp/en/nkave/index/component?idx={ticker}'
               .format(ticker=self.index_ticker.lower()))
        response = http_utils.get(url)
        if response.ok:
            parsed_html = BeautifulSoup(response.text, 'html.parser')
            for table in parsed_html.find('section', {'class': 'idx-section'}).find_all('tbody'):
                for row in table.find_all('tr'):
                    constituents.append(row.find_next('td').text)
        return constituents
